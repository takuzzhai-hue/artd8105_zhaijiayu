#!/usr/bin/env python3
"""3×3 parameter sweep. Same camera, scale, and light for every cell."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from generate import default_flat, generate


def set_axis(flat, name, value):
    if name == "period":
        flat["period_x"] = flat["period_y"] = flat["period_z"] = float(value)
    elif name == "period_x":
        flat["period_x"] = float(value)
    elif name == "period_z":
        flat["period_z"] = float(value)
    elif name == "twist":
        flat["twist_mode"] = "linear"
        flat["twist_deg_per_mm"] = float(value)
    elif name == "bend_x":
        flat["bend_x"] = float(value)
    elif name == "wall_thickness":
        flat["wall_thickness"] = float(value)
    elif name == "level_offset":
        flat["level_offset"] = float(value)
    elif name == "taper_x":
        flat["taper_x"] = float(value)
    elif name == "family":
        flat["family"] = str(value)
    else:
        raise SystemExit(f"unknown sweep axis {name}")


def default_values(name):
    table = {
        "period": [16, 24, 36],
        "period_x": [14, 24, 42],
        "period_z": [14, 24, 42],
        "twist": [-1.0, 0.0, 1.5],
        "bend_x": [-0.6, 0.0, 0.6],
        "wall_thickness": [1.4, 1.8, 2.6],
        "level_offset": [-0.25, 0.0, 0.25],
        "taper_x": [-0.5, 0.0, 0.5],
        "family": ["gyroid", "diamond", "primitive"],
    }
    if name not in table:
        raise SystemExit(f"unknown sweep axis {name}. Known: {', '.join(table)}")
    return table[name]


def rotate_view(pts, elev=22.0, azim=38.0):
    e = np.deg2rad(elev)
    a = np.deg2rad(azim)
    rz = np.array(
        [[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]],
        dtype=np.float64,
    )
    rx = np.array(
        [[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]],
        dtype=np.float64,
    )
    return pts @ rz.T @ rx.T


def shaded_preview(verts, faces, n=240, span=120.0):
    tri = verts[faces]
    center = tri.mean(axis=1)
    normal = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    normal /= np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-20)
    mid = verts.mean(axis=0)
    viewed = rotate_view(center - mid)
    normals = rotate_view(normal)
    light = np.array([0.35, -0.25, 0.90], dtype=np.float64)
    light /= np.linalg.norm(light)
    shade = np.clip(normals @ light, 0.08, 1.0)
    shade = 0.18 + 0.72 * shade
    x, y, z = viewed[:, 0], viewed[:, 1], viewed[:, 2]
    half = span * 0.5
    xi = np.clip(((x + half) / span * (n - 1)).astype(np.int32), 0, n - 1)
    yi = np.clip(((y + half) / span * (n - 1)).astype(np.int32), 0, n - 1)
    depth = np.full((n, n), -np.inf, dtype=np.float64)
    image = np.ones((n, n), dtype=np.float64)
    order = np.argsort(z)
    depth[yi[order], xi[order]] = z[order]
    image[yi[order], xi[order]] = shade[order]
    image[depth == -np.inf] = 1.0
    return image


def label_of(name, value):
    if name == "family":
        return f"{name} = {value}"
    return f"{name} = {float(value):.3g}"


def main():
    parser = argparse.ArgumentParser(description="Render a 3×3 parameter comparison.")
    parser.add_argument("--x", default="period")
    parser.add_argument("--y", default="twist")
    parser.add_argument("--x-values", default=None, help="comma-separated")
    parser.add_argument("--y-values", default=None)
    parser.add_argument("--res", type=int, default=128)
    parser.add_argument("--out", type=Path, default=Path("output/sweep.png"))
    args = parser.parse_args()
    xs = [v.strip() for v in args.x_values.split(",")] if args.x_values else default_values(args.x)
    ys = [v.strip() for v in args.y_values.split(",")] if args.y_values else default_values(args.y)
    if len(xs) != 3 or len(ys) != 3:
        raise SystemExit("need exactly 3 values on each axis")

    fig, axes = plt.subplots(3, 3, figsize=(11.2, 11.6), dpi=160)
    fig.patch.set_facecolor("white")
    for row, y_value in enumerate(ys):
        for col, x_value in enumerate(xs):
            flat = default_flat()
            flat["preview_resolution"] = args.res
            set_axis(flat, args.x, x_value)
            set_axis(flat, args.y, y_value)
            print(f"cell {row},{col}  {args.x}={x_value}  {args.y}={y_value}", flush=True)
            result = generate(flat, preview=True, quiet=True)
            image = shaded_preview(result["verts"], result["faces"])
            ax = axes[row, col]
            ax.imshow(image, cmap="gray", vmin=0, vmax=1, origin="lower")
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color("#d5d2cc")
            ax.set_xlabel(f"{label_of(args.x, x_value)}\n{label_of(args.y, y_value)}", fontsize=8, color="#2a2a2a")
    fig.suptitle(f"{args.y}  ×  {args.x}", fontsize=12, color="#2a2a2a")
    fig.tight_layout()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=160)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
