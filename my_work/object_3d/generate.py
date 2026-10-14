#!/usr/bin/env python3
"""Build the parametric jar, self-check the indexed mesh, then write a binary STL.

The STL is written only after the mesh check passes. A failure exits with status 1
and leaves the previous file untouched.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
import time
import zipfile
from pathlib import Path

import numpy as np

from jar_geom import DEFAULTS, PARAM_KEYS, build_jar, mesh_check

ROOT = Path(__file__).resolve().parent


def write_binary_stl(path, verts, faces):
    v = np.asarray(verts, dtype=np.float64)
    f = np.asarray(faces, dtype=np.int64)
    tri = v[f].astype(np.float32)
    v0, v1, v2 = tri[:, 0], tri[:, 1], tri[:, 2]
    normals = np.cross(v1 - v0, v2 - v0)
    length = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = (normals / np.maximum(length, 1e-20)).astype(np.float32)
    record = np.dtype([("n", "<f4", (3,)), ("v", "<f4", (3, 3)), ("attr", "<u2")])
    data = np.empty(len(faces), dtype=record)
    data["n"] = normals
    data["v"] = tri
    data["attr"] = 0
    header = b"parametric jar / ARTD8105"
    header = header[:80].ljust(80, b"\0")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.write(header)
        handle.write(struct.pack("<I", int(len(faces))))
        handle.write(data.tobytes())


def write_3mf(path, verts, faces):
    """3MF with the unit stored as millimetres, so a slicer does not rescale it."""
    chunks = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        '<model unit="millimeter" xml:lang="en-US" ',
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n',
        "<metadata name=\"Title\">kneaded jar</metadata>\n",
        "<metadata name=\"Application\">ARTD8105 jar</metadata>\n",
        "<resources>\n",
        '<object id="1" type="model" name="Jar">\n',
        "<mesh>\n<vertices>\n",
    ]
    for x, y, z in verts:
        chunks.append(f'<vertex x="{x:.5f}" y="{y:.5f}" z="{z:.5f}"/>\n')
    chunks.append("</vertices>\n<triangles>\n")
    for a, b, c in faces:
        chunks.append(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>\n')
    chunks.append("</triangles>\n</mesh>\n</object>\n</resources>\n")
    chunks.append('<build>\n<item objectid="1"/>\n</build>\n</model>\n')
    model = "".join(chunks).encode("utf-8")
    types = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
        '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
        "</Types>\n"
    ).encode("utf-8")
    rels = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
        "</Relationships>\n"
    ).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("3D/3dmodel.model", model)


def build_parser():
    p = argparse.ArgumentParser(description="Kneaded jar. Fixed topology, no boolean.")
    for key in PARAM_KEYS:
        default = DEFAULTS[key]
        kind = int if isinstance(default, int) else float
        p.add_argument("--" + key.replace("_", "-"), type=kind, default=default, dest=key)
    p.add_argument("--out-dir", type=Path, default=ROOT / "output")
    return p


def params_from_args(args):
    return {key: getattr(args, key) for key in PARAM_KEYS}


def generate(params, out_dir):
    t0 = time.time()
    verts, faces, info = build_jar(params)
    measured = info["min_normal_wall"]
    ok, failures, stats = mesh_check(verts, faces, params["min_wall"], measured)
    print(
        f"mesh V={stats['V']} E={stats['E']} F={stats['F']} χ={stats['chi']}  "
        f"volume={stats['volume']:.1f} mm³  "
        f"min_wall={measured:.3f} mm",
        flush=True,
    )
    for row in info["profile"]:
        print(f"  R0  t={row['t']:.2f}  z={row['z']:.1f}  r={row['R0']:.2f} mm", flush=True)
    if not ok:
        for line in failures:
            print(f"SELF-CHECK FAIL: {line}", file=sys.stderr)
        raise SystemExit(1)

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stl_path = out_dir / "object.stl"
    write_binary_stl(stl_path, verts, faces)
    mf_path = out_dir / "jar.3mf"
    write_3mf(mf_path, verts, faces)
    arr = np.asarray(verts)
    bb0 = arr.min(axis=0)
    bb1 = arr.max(axis=0)
    size = bb1 - bb0
    record = {
        "rule": "The wall is kneaded, twisted and bent as one sheet. Inner stays wall-thick.",
        "params": params,
        "triangles": int(len(faces)),
        "vertices": int(len(verts)),
        "euler": stats,
        "min_radial_wall_mm": info["min_radial_wall"],
        "min_normal_wall_mm": info["min_normal_wall"],
        "profile": info["profile"],
        "bbox_min_mm": bb0.tolist(),
        "bbox_max_mm": bb1.tolist(),
        "dimensions_mm": size.tolist(),
        "self_check": "PASS",
        "elapsed_s": time.time() - t0,
    }
    with (out_dir / "params.json").open("w", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2)
    print(f"wrote {stl_path}", flush=True)
    print(f"wrote {mf_path}", flush=True)
    print(
        f"bbox {size.tolist()} mm   "
        f"diameter={max(size[0], size[1]):.2f}   height={size[2]:.2f}",
        flush=True,
    )
    return record


def main(argv=None):
    args = build_parser().parse_args(argv)
    generate(params_from_args(args), args.out_dir)


if __name__ == "__main__":
    main()
