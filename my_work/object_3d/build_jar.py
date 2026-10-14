"""Create the jar mesh in the open Blender file.

Run from Blender's Scripting workspace, or via the Blender MCP connection.
"""
from __future__ import annotations

import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from build_nodes import attach  # noqa: E402
from jar_geom import DEFAULTS, build_jar  # noqa: E402


OBJECT = "Jar"
BLEND = ROOT / "jar.blend"


def build(params=None):
    params = dict(DEFAULTS if params is None else params)
    verts, faces, info = build_jar(params)

    for name in (OBJECT, "Cube", "Gyroid_GN", "object"):
        old = bpy.data.objects.get(name)
        if old is None:
            continue
        old_mesh = old.data if old.type == "MESH" else None
        bpy.data.objects.remove(old, do_unlink=True)
        if old_mesh is not None and old_mesh.users == 0:
            bpy.data.meshes.remove(old_mesh)

    mesh = bpy.data.meshes.new("JarMesh")
    mesh.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    mesh.update()
    for name, values in info["attrs"].items():
        attr = mesh.attributes.new(name, "FLOAT", "POINT")
        attr.data.foreach_set("value", values)
    if hasattr(mesh, "shade_smooth"):
        mesh.shade_smooth()
    else:
        for poly in mesh.polygons:
            poly.use_smooth = True
    obj = bpy.data.objects.new(OBJECT, mesh)
    coll = bpy.context.scene.collection
    for c in bpy.data.collections:
        if c.name == "Collection":
            coll = c
            break
    coll.objects.link(obj)

    obj["rule"] = "kneaded sheet: folds, thumbs, twist, bend, wavy lip. Inner follows."
    for key, value in params.items():
        if isinstance(value, (int, float)):
            obj[key] = value

    _ng, _mod = attach(obj)

    mat = bpy.data.materials.get("JarMat")
    if mat is None:
        mat = bpy.data.materials.new("JarMat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.86, 0.83, 0.78, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.72
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"

    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    screen = getattr(bpy.context, "screen", None)
    if screen is not None:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                region = next(r for r in area.regions if r.type == "WINDOW")
                with bpy.context.temp_override(area=area, region=region):
                    bpy.ops.view3d.view_selected()
                break

    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    return {
        "object": obj.name,
        "verts": info["n_verts"],
        "faces": info["n_faces"],
        "min_radial": info["min_radial_wall"],
        "blend": str(BLEND),
    }


if __name__ == "__main__":
    print(build())
