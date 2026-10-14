#!/usr/bin/env python3
"""Independent STL checks. Parses the file bytes. Does not import bpy."""

from __future__ import annotations

import argparse
import struct
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

AREA_EPS = 1e-8
WELD_Q = 1e-4
RAY_K = 2500
WALL_MIN = 1.6


class Report:
    def __init__(self):
        self.lines = []
        self.failed = False

    def add(self, ok, name, detail):
        tag = "[PASS]" if ok else "[FAIL]"
        if not ok:
            self.failed = True
        line = f"{tag} {name} {detail}"
        self.lines.append(line)
        print(line, flush=True)

    def note(self, name, detail):
        line = f"[INFO] {name} {detail}"
        self.lines.append(line)
        print(line, flush=True)


def read_stl(path: Path):
    data = path.read_bytes()
    if len(data) < 84:
        raise SystemExit(f"file too small: {len(data)} bytes")
    header = data[:80]
    count = struct.unpack_from("<I", data, 80)[0]
    expected = 84 + 50 * count
    return data, header, count, expected, len(data)


def parse_triangles(data, count):
    record = np.dtype([("n", "<f4", (3,)), ("v", "<f4", (3, 3)), ("attr", "<u2")])
    arr = np.frombuffer(data, dtype=record, count=count, offset=84)
    return arr["n"].astype(np.float64), arr["v"].astype(np.float64)


def signed_volume(tri):
    v0, v1, v2 = tri[:, 0], tri[:, 1], tri[:, 2]
    return float(np.sum(np.einsum("ij,ij->i", v0, np.cross(v1 - v0, v2 - v0))) / 6.0)


def weld_vertices(tri, q=WELD_Q):
    pts = tri.reshape(-1, 3)
    keys = np.round(pts / q).astype(np.int64)
    _uniq, inv = np.unique(keys, axis=0, return_inverse=True)
    welded = np.zeros((len(_uniq), 3), dtype=np.float64)
    np.add.at(welded, inv, pts)
    welded /= np.bincount(inv).astype(np.float64)[:, None]
    return welded, inv.reshape(-1, 3), len(pts), len(welded)


def moller_trumbore(orig, direction, v0, v1, v2):
    eps = 1e-12
    e1 = v1 - v0
    e2 = v2 - v0
    pvec = np.cross(direction, e2)
    det = np.dot(e1, pvec)
    if abs(det) < eps:
        return None
    inv = 1.0 / det
    tvec = orig - v0
    u = np.dot(tvec, pvec) * inv
    if u < 0.0 or u > 1.0:
        return None
    qvec = np.cross(tvec, e1)
    v = np.dot(direction, qvec) * inv
    if v < 0.0 or u + v > 1.0:
        return None
    t = np.dot(e2, qvec) * inv
    if t <= 1e-6:
        return None
    return t


def build_hash(tri, cell):
    bb0 = tri.reshape(-1, 3).min(axis=0)
    buckets = defaultdict(list)
    tmin = tri.min(axis=1)
    tmax = tri.max(axis=1)
    ijk0 = np.floor((tmin - bb0) / cell).astype(np.int32)
    ijk1 = np.floor((tmax - bb0) / cell).astype(np.int32)
    for i in range(len(tri)):
        a, b = ijk0[i], ijk1[i]
        for x in range(int(a[0]), int(b[0]) + 1):
            for y in range(int(a[1]), int(b[1]) + 1):
                for z in range(int(a[2]), int(b[2]) + 1):
                    buckets[(x, y, z)].append(i)
    return buckets, bb0, cell


def ray_first_hit(orig, direction, tri, normals, source_normal, buckets, bb0, cell, skip, tmax=24.0):
    origin = np.asarray(orig, dtype=np.float64)
    direct = np.asarray(direction, dtype=np.float64)
    length = np.linalg.norm(direct)
    if length < 1e-15:
        return None
    direct = direct / length
    best = None
    voxel = np.floor((origin - bb0) / cell).astype(np.int64)
    step = np.sign(direct).astype(np.int64)
    next_t = np.empty(3, dtype=np.float64)
    delta = np.empty(3, dtype=np.float64)
    for axis in range(3):
        if abs(direct[axis]) > 1e-15:
            inv = 1.0 / direct[axis]
            if step[axis] > 0:
                next_t[axis] = ((voxel[axis] + 1) * cell + bb0[axis] - origin[axis]) * inv
            else:
                next_t[axis] = (voxel[axis] * cell + bb0[axis] - origin[axis]) * inv
            delta[axis] = abs(cell * inv)
        else:
            next_t[axis] = 1e15
            delta[axis] = 1e15
    traveled = 0.0
    seen = set()
    for _ in range(128):
        key = (int(voxel[0]), int(voxel[1]), int(voxel[2]))
        for index in buckets.get(key, ()):
            if index == skip or index in seen:
                continue
            seen.add(index)
            if np.dot(source_normal, normals[index]) > -0.25:
                continue
            hit = moller_trumbore(origin, direct, tri[index, 0], tri[index, 1], tri[index, 2])
            if hit is None or hit > tmax or hit < 0.2:
                continue
            if best is None or hit < best:
                best = hit
        if best is not None and traveled >= best:
            break
        axis = int(np.argmin(next_t))
        traveled = float(next_t[axis])
        if traveled > tmax:
            break
        voxel[axis] += int(step[axis])
        next_t[axis] += float(delta[axis])
    return best


def wall_samples(tri, k=RAY_K, seed=1):
    rng = np.random.default_rng(seed)
    v0, v1, v2 = tri[:, 0], tri[:, 1], tri[:, 2]
    normals = np.cross(v1 - v0, v2 - v0)
    length = np.maximum(np.linalg.norm(normals, axis=1, keepdims=True), 1e-20)
    normals = normals / length
    centroids = (v0 + v1 + v2) / 3.0
    count = len(tri)
    k = min(k, count)
    chosen = rng.choice(count, size=k, replace=False)
    cell = 3.0
    buckets, grid0, cell = build_hash(tri, cell)
    distances = []
    misses = 0
    for index in chosen:
        origin = centroids[index] - normals[index] * 2e-3
        hit = ray_first_hit(
            origin,
            -normals[index],
            tri,
            normals,
            normals[index],
            buckets,
            grid0,
            cell,
            skip=int(index),
        )
        if hit is None:
            misses += 1
        else:
            distances.append(hit)
    return np.asarray(distances, dtype=np.float64), misses, k


def union_find_components(faces, n_verts):
    parent = np.arange(n_verts, dtype=np.int32)
    rank = np.zeros(n_verts, dtype=np.int8)

    def find(a):
        a = int(a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = int(parent[a])
        return a

    edges = np.vstack((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]))
    edges.sort(axis=1)
    edges = np.unique(edges, axis=0)
    for i in range(len(edges)):
        ra = find(edges[i, 0])
        rb = find(edges[i, 1])
        if ra == rb:
            continue
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] = rank[ra] + 1
    roots = np.fromiter((find(i) for i in range(n_verts)), dtype=np.int32, count=n_verts)
    _uniq, counts = np.unique(roots[faces[:, 0]], return_counts=True)
    return int(len(counts)), [int(c) for c in counts], len(edges)


def check_file(path, report_path=None, samples=RAY_K):
    path = Path(path)
    if report_path is None:
        report_path = path.parent / "verification_report.md"
    report = Report()
    data, header, count, expected, nbytes = read_stl(path)
    header_text = header.split(b"\0", 1)[0]
    report.add(len(header) == 80, "Header", f"80 bytes  text={header_text!r}")
    report.add(count > 0, "Triangle count field", f"uint32 count={count}")
    report.add(
        nbytes == expected,
        "File size",
        f"filesize={nbytes} expected={expected} (= 84 + 50*{count})",
    )
    if nbytes != expected:
        _write(report, report_path)
        return False, report.lines

    stored_n, tri = parse_triangles(data, count)
    report.add(True, "Triangle count", f"triangles={count}")

    bb0 = tri.reshape(-1, 3).min(axis=0)
    bb1 = tri.reshape(-1, 3).max(axis=0)
    size = bb1 - bb0
    report.add(
        True,
        "Bounding box",
        f"min={[round(v, 4) for v in bb0.tolist()]} max={[round(v, 4) for v in bb1.tolist()]}",
    )
    report.add(True, "Dimensions", f"size={[round(v, 4) for v in size.tolist()]} mm")

    volume = signed_volume(tri)
    report.add(volume > 0, "Signed volume", f"{volume:.4f} mm³  (must be > 0)")

    verts, faces, n_raw, n_weld = weld_vertices(tri)
    report.note("Vertex welding", f"welded_vertices={n_weld} from {n_raw}  q={WELD_Q} mm")

    areas = 0.5 * np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1)
    n_degen = int(np.sum(areas < AREA_EPS))
    report.add(n_degen == 0, "Degenerate triangles", f"count={n_degen}")

    undirected = np.vstack(
        (
            np.sort(faces[:, [0, 1]], axis=1),
            np.sort(faces[:, [1, 2]], axis=1),
            np.sort(faces[:, [2, 0]], axis=1),
        )
    )
    _uniq, counts = np.unique(undirected, axis=0, return_counts=True)
    n_boundary = int(np.sum(counts == 1))
    n_nonmanifold = int(np.sum(counts >= 3))
    n_two = int(np.sum(counts == 2))
    report.add(n_boundary == 0, "Boundary edges", f"count={n_boundary} (must be 0)")
    report.add(n_nonmanifold == 0, "Non-manifold edges", f"count={n_nonmanifold} (must be 0)")
    report.add(n_two == len(_uniq), "Each edge used twice", f"unique_edges={len(_uniq)} twice={n_two}")

    a = np.concatenate((faces[:, 0], faces[:, 1], faces[:, 2])).astype(np.int64)
    b = np.concatenate((faces[:, 1], faces[:, 2], faces[:, 0])).astype(np.int64)
    n_verts = len(verts)
    key = np.minimum(a, b) * np.int64(n_verts) + np.maximum(a, b)
    sign = np.where(a < b, 1.0, -1.0)
    _keys, inverse = np.unique(key, return_inverse=True)
    sign_sum = np.bincount(inverse, weights=sign)
    use = np.bincount(inverse)
    n_inconsistent = int(np.sum((use == 2) & (np.abs(sign_sum) > 1e-9)))
    report.add(
        n_inconsistent == 0,
        "Opposite winding on shared edges",
        f"disagreeing edges={n_inconsistent} (must be 0)",
    )

    n_cc, tri_counts, n_edges = union_find_components(faces, n_verts)
    report.add(
        n_cc == 1,
        "Shells (union-find)",
        f"count={n_cc} (must be 1)  triangles per shell={tri_counts}",
    )

    chi = n_weld - n_edges + count
    report.add(chi == 2, "Euler V-E+F", f"V={n_weld} E={n_edges} F={count}  χ={chi} (must be 2)")

    distances, misses, k = wall_samples(tri, k=samples)
    if len(distances) == 0:
        report.add(False, "Wall thickness", "no ray hits")
    else:
        th_min = float(distances.min())
        p1 = float(np.percentile(distances, 1))
        report.add(
            th_min >= WALL_MIN,
            "Wall thickness (ray)",
            f"K={k} hits={len(distances)} misses={misses}  "
            f"min={th_min:.3f} p1={p1:.3f} median={float(np.median(distances)):.3f} mm  "
            f"(min must be ≥ {WALL_MIN} mm). Sample of centroids, not a global proof.",
        )

    summary = "ALL PASS" if not report.failed else "FAILED"
    report.lines.append(f"SUMMARY {summary}")
    print(f"SUMMARY {summary}", flush=True)
    _write(report, Path(report_path))
    return (not report.failed), report.lines


def _write(report, report_path):
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    body = "# STL check\n\n```\n" + "\n".join(report.lines) + "\n```\n"
    report_path.write_text(body, encoding="utf-8")
    print(f"wrote {report_path}", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Parse an STL from bytes and re-check it. No bpy.")
    parser.add_argument("stl", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--samples", type=int, default=RAY_K)
    args = parser.parse_args(argv)
    ok, _lines = check_file(args.stl, report_path=args.report, samples=args.samples)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
