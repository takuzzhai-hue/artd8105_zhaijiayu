"""Rebuild the GyroidLattice Geometry Nodes group in the open Blender file.

Run from Blender's Scripting workspace, or:
  blender --python build_gn.py
"""
import math as pymath
import bpy

GROUP = "GyroidLattice"
OBJECT = "Gyroid_GN"


def mathn(nodes, op, loc):
    n = nodes.new("ShaderNodeMath")
    n.operation = op
    n.location = loc
    return n


def N(nodes, bid, loc, **kw):
    n = nodes.new(bid)
    n.location = loc
    for k, v in kw.items():
        setattr(n, k, v)
    return n


def build():
    for name in list(bpy.data.objects.keys()):
        if name == OBJECT:
            bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
    for name in list(bpy.data.node_groups.keys()):
        if name == GROUP:
            bpy.data.node_groups.remove(bpy.data.node_groups[name])

    ng = bpy.data.node_groups.new(GROUP, "GeometryNodeTree")
    iface = ng.interface
    iface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    s_size = iface.new_socket(name="Size", in_out="INPUT", socket_type="NodeSocketFloat")
    s_size.default_value = 56.0
    s_size.min_value = 20.0
    s_size.max_value = 100.0
    s_size.subtype = "DISTANCE"
    s_period = iface.new_socket(name="Period", in_out="INPUT", socket_type="NodeSocketFloat")
    s_period.default_value = 28.0
    s_period.min_value = 10.0
    s_period.max_value = 50.0
    s_period.subtype = "DISTANCE"
    s_wall = iface.new_socket(name="Wall", in_out="INPUT", socket_type="NodeSocketFloat")
    s_wall.default_value = 2.2
    s_wall.min_value = 1.2
    s_wall.max_value = 5.0
    s_wall.subtype = "DISTANCE"
    s_res = iface.new_socket(name="Resolution", in_out="INPUT", socket_type="NodeSocketInt")
    s_res.default_value = 96
    s_res.min_value = 24
    s_res.max_value = 160
    s_smooth = iface.new_socket(name="Smooth", in_out="INPUT", socket_type="NodeSocketInt")
    s_smooth.default_value = 18
    s_smooth.min_value = 0
    s_smooth.max_value = 40
    s_twist = iface.new_socket(name="Twist", in_out="INPUT", socket_type="NodeSocketFloat")
    s_twist.default_value = 0.0
    s_twist.min_value = 0.0
    s_twist.max_value = 6.0

    nodes = ng.nodes
    links = ng.links
    nodes.clear()
    gi = nodes.new("NodeGroupInput")
    gi.location = (-1800, 0)
    go = nodes.new("NodeGroupOutput")
    go.location = (1600, 0)

    half = mathn(nodes, "MULTIPLY", (-1500, 200))
    half.inputs[1].default_value = 0.5
    links.new(gi.outputs["Size"], half.inputs[0])
    neg = mathn(nodes, "MULTIPLY", (-1320, 280))
    neg.inputs[1].default_value = -1.0
    links.new(half.outputs[0], neg.inputs[0])
    comb_min = N(nodes, "ShaderNodeCombineXYZ", (-1140, 260))
    links.new(neg.outputs[0], comb_min.inputs["X"])
    links.new(neg.outputs[0], comb_min.inputs["Y"])
    comb_max = N(nodes, "ShaderNodeCombineXYZ", (-1140, 80))
    links.new(half.outputs[0], comb_max.inputs["X"])
    links.new(half.outputs[0], comb_max.inputs["Y"])
    links.new(gi.outputs["Size"], comb_max.inputs["Z"])

    pos = N(nodes, "GeometryNodeInputPosition", (-1500, -200))
    sep0 = N(nodes, "ShaderNodeSeparateXYZ", (-1320, -200))
    links.new(pos.outputs["Position"], sep0.inputs[0])
    d2r = mathn(nodes, "MULTIPLY", (-1140, -360))
    d2r.inputs[1].default_value = pymath.pi / 180.0
    links.new(gi.outputs["Twist"], d2r.inputs[0])
    ang = mathn(nodes, "MULTIPLY", (-960, -320))
    links.new(d2r.outputs[0], ang.inputs[0])
    links.new(sep0.outputs["Z"], ang.inputs[1])
    vrot = N(nodes, "ShaderNodeVectorRotate", (-780, -160), rotation_type="AXIS_ANGLE")
    vrot.inputs["Axis"].default_value = (0, 0, 1)
    links.new(pos.outputs["Position"], vrot.inputs["Vector"])
    links.new(ang.outputs[0], vrot.inputs["Angle"])
    sep = N(nodes, "ShaderNodeSeparateXYZ", (-560, -160))
    links.new(vrot.outputs["Vector"], sep.inputs[0])

    twpi = mathn(nodes, "DIVIDE", (-1500, -520))
    twpi.inputs[0].default_value = 2.0 * pymath.pi
    links.new(gi.outputs["Period"], twpi.inputs[1])
    X = mathn(nodes, "MULTIPLY", (-380, -40))
    links.new(sep.outputs["X"], X.inputs[0])
    links.new(twpi.outputs[0], X.inputs[1])
    Y = mathn(nodes, "MULTIPLY", (-380, -180))
    links.new(sep.outputs["Y"], Y.inputs[0])
    links.new(twpi.outputs[0], Y.inputs[1])
    Z = mathn(nodes, "MULTIPLY", (-380, -320))
    links.new(sep.outputs["Z"], Z.inputs[0])
    links.new(twpi.outputs[0], Z.inputs[1])

    def trig(op, src, loc):
        n = mathn(nodes, op, loc)
        links.new(src.outputs[0], n.inputs[0])
        return n

    sX = trig("SINE", X, (-200, 40))
    cX = trig("COSINE", X, (-200, -40))
    sY = trig("SINE", Y, (-200, -140))
    cY = trig("COSINE", Y, (-200, -220))
    sZ = trig("SINE", Z, (-200, -320))
    cZ = trig("COSINE", Z, (-200, -400))

    m1 = mathn(nodes, "MULTIPLY", (0, 20))
    links.new(sX.outputs[0], m1.inputs[0])
    links.new(cY.outputs[0], m1.inputs[1])
    m2 = mathn(nodes, "MULTIPLY", (0, -120))
    links.new(sY.outputs[0], m2.inputs[0])
    links.new(cZ.outputs[0], m2.inputs[1])
    m3 = mathn(nodes, "MULTIPLY", (0, -260))
    links.new(sZ.outputs[0], m3.inputs[0])
    links.new(cX.outputs[0], m3.inputs[1])
    a12 = mathn(nodes, "ADD", (180, -40))
    links.new(m1.outputs[0], a12.inputs[0])
    links.new(m2.outputs[0], a12.inputs[1])
    gy = mathn(nodes, "ADD", (360, -80))
    links.new(a12.outputs[0], gy.inputs[0])
    links.new(m3.outputs[0], gy.inputs[1])
    absg = mathn(nodes, "ABSOLUTE", (540, -80))
    links.new(gy.outputs[0], absg.inputs[0])

    scale = mathn(nodes, "MULTIPLY", (180, -420))
    scale.inputs[1].default_value = 0.612
    links.new(twpi.outputs[0], scale.inputs[0])
    tf = mathn(nodes, "MULTIPLY", (360, -420))
    links.new(gi.outputs["Wall"], tf.inputs[0])
    links.new(scale.outputs[0], tf.inputs[1])
    dens = mathn(nodes, "SUBTRACT", (540, -200))
    links.new(tf.outputs[0], dens.inputs[0])
    links.new(absg.outputs[0], dens.inputs[1])

    vcube = N(nodes, "GeometryNodeVolumeCube", (760, 80))
    links.new(dens.outputs[0], vcube.inputs["Density"])
    vcube.inputs["Background"].default_value = 0.0
    links.new(comb_min.outputs[0], vcube.inputs["Min"])
    links.new(comb_max.outputs[0], vcube.inputs["Max"])
    links.new(gi.outputs["Resolution"], vcube.inputs["Resolution X"])
    links.new(gi.outputs["Resolution"], vcube.inputs["Resolution Y"])
    links.new(gi.outputs["Resolution"], vcube.inputs["Resolution Z"])

    v2m = N(nodes, "GeometryNodeVolumeToMesh", (980, 80))
    v2m.inputs["Threshold"].default_value = 0.0
    v2m.inputs["Adaptivity"].default_value = 0.08
    links.new(vcube.outputs["Volume"], v2m.inputs["Volume"])

    blur = N(nodes, "GeometryNodeBlurAttribute", (980, -180), data_type="FLOAT_VECTOR")
    pos2 = N(nodes, "GeometryNodeInputPosition", (760, -180))
    links.new(pos2.outputs["Position"], blur.inputs["Value"])
    links.new(gi.outputs["Smooth"], blur.inputs["Iterations"])
    setp = N(nodes, "GeometryNodeSetPosition", (1180, 40))
    links.new(v2m.outputs["Mesh"], setp.inputs["Geometry"])
    links.new(blur.outputs["Value"], setp.inputs["Position"])

    mat = bpy.data.materials.get("GyroidMat")
    if mat is None:
        mat = bpy.data.materials.new("GyroidMat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.72, 0.74, 0.76, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.45
    setm = N(nodes, "GeometryNodeSetMaterial", (1360, 40))
    setm.inputs["Material"].default_value = mat
    links.new(setp.outputs["Geometry"], setm.inputs["Geometry"])
    links.new(setm.outputs["Geometry"], go.inputs["Geometry"])

    me = bpy.data.meshes.new("Gyroid_GN_mesh")
    obj = bpy.data.objects.new(OBJECT, me)
    coll = bpy.context.scene.collection
    for c in bpy.data.collections:
        if c.name == "Collection":
            coll = c
            break
    coll.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new("Gyroid", "NODES")
    mod.node_group = ng
    return obj


if __name__ == "__main__":
    build()
