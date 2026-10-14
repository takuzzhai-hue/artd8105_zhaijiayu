"""Geometry Nodes sliders for the kneaded jar.

The graph repeats deformed() in jar_geom.py. Slider defaults come from DEFAULTS
there. Dragging a slider moves the same vertices; it does not rebuild the stitch.
"""

from __future__ import annotations

import math

import bpy

from jar_geom import DEFAULTS

GROUP = "揉搓弯折"

# panel, socket name, defaults key, min, max, hover text
SLIDERS = (
    ("形体", "高度", "height", 100.0, 220.0, "罐子多高，毫米"),
    ("形体", "脚半径", "r_foot", 16.0, 50.0, "底脚的半径"),
    ("形体", "腹半径", "r_belly", 30.0, 70.0, "肚子最宽处的半径"),
    ("形体", "腹的位置", "belly_t", 0.2, 0.6, "肚子在多高。0 是底，1 是口"),
    ("形体", "颈半径", "r_neck", 16.0, 55.0, "脖子收进去之后的半径"),
    ("形体", "颈的位置", "neck_t", 0.5, 0.9, "脖子在多高"),
    ("形体", "口半径", "r_rim", 20.0, 70.0, "口沿张开到多大"),
    ("揉搓", "褶数", "fold_n", 2.0, 8.0, "绕一圈有几道手指褶"),
    ("揉搓", "褶深", "fold_depth", 0.0, 14.0, "褶有多深，毫米。再加大会被内腔下限夹住"),
    ("揉搓", "杂乱", "fold_soft", 0.0, 1.2, "第二道不同步的褶。0 是整齐的"),
    ("揉搓", "收腰", "waist", 0.0, 12.0, "脖子下方再勒进去多少，毫米"),
    ("揉搓", "种子", "seed", 0.0, 20.0, "整圈褶和三个拇指一起换位置"),
    ("揉搓", "拇指宽度", "thumb_deg", 20.0, 90.0, "一个拇指有多宽，度"),
    ("揉搓", "拇指高低", "thumb_sigma", 12.0, 50.0, "一个拇指在高度上有多长，毫米"),
    ("拇指", "拇指1角度", "thumb1_deg", 0.0, 360.0, "第一处按压绕罐子的位置"),
    ("拇指", "拇指1高度", "thumb1_t", 0.15, 0.9, "第一处按压在多高"),
    ("拇指", "拇指1深浅", "thumb1_amp", -12.0, 12.0, "负是按进去，正是挤出来"),
    ("拇指", "拇指2角度", "thumb2_deg", 0.0, 360.0, "第二处按压绕罐子的位置"),
    ("拇指", "拇指2高度", "thumb2_t", 0.15, 0.9, "第二处按压在多高"),
    ("拇指", "拇指2深浅", "thumb2_amp", -12.0, 12.0, "负是按进去，正是挤出来"),
    ("拇指", "拇指3角度", "thumb3_deg", 0.0, 360.0, "第三处按压绕罐子的位置"),
    ("拇指", "拇指3高度", "thumb3_t", 0.15, 0.9, "第三处按压在多高"),
    ("拇指", "拇指3深浅", "thumb3_amp", -12.0, 12.0, "负是按进去，正是挤出来"),
    ("弯折", "扭转", "twist", -180.0, 180.0, "从底到口一共转多少度"),
    ("弯折", "弯折", "bend", -40.0, 40.0, "口被推开中轴多少毫米"),
    ("弯折", "弯折方向", "bend_deg", 0.0, 360.0, "往哪一边推"),
    ("口沿", "口沿起伏", "rim_wave", 0.0, 20.0, "口沿高低差，毫米"),
    ("口沿", "口沿瓣数", "rim_lobes", 2.0, 7.0, "口沿起伏几下"),
    ("口沿", "口沿过渡", "rim_band", 8.0, 40.0, "起伏从口沿往下影响多深，毫米"),
    ("泥", "壁厚", "wall", 2.0, 8.0, "内外壁相差多少毫米"),
    ("泥", "内腔最小半径", "min_hole", 8.0, 24.0, "揉再深，洞也不会比这个更小"),
)


class Graph:
    def __init__(self, ng):
        self.nodes = ng.nodes
        self.links = ng.links
        self.x = 0
        self.y = 0
        self.frame = None

    def section(self, label, x, y):
        frame = self.nodes.new("NodeFrame")
        frame.label = label
        frame.label_size = 28
        self.frame = frame
        self.x = x
        self.y = y

    def _place(self, node):
        node.location = (self.x, self.y)
        node.parent = self.frame
        self.y -= 90
        if self.y < -2400:
            self.y = 400
            self.x += 220
        return node

    def plug(self, socket, value):
        if isinstance(value, (int, float)):
            socket.default_value = float(value)
        else:
            self.links.new(value, socket)

    def math(self, op, a, b=None):
        node = self._place(self.nodes.new("ShaderNodeMath"))
        node.operation = op
        self.plug(node.inputs[0], a)
        if b is not None:
            self.plug(node.inputs[1], b)
        return node.outputs[0]

    def clamp01(self, value):
        return self.math("MINIMUM", self.math("MAXIMUM", value, 0.0), 1.0)

    def smoothstep(self, x, a, b):
        u = self.clamp01(self.math("DIVIDE", self.math("SUBTRACT", x, a), self.math("SUBTRACT", b, a)))
        uu = self.math("MULTIPLY", u, u)
        return self.math("MULTIPLY", uu, self.math("SUBTRACT", 3.0, self.math("MULTIPLY", 2.0, u)))

    def compare(self, op, a, b):
        node = self._place(self.nodes.new("FunctionNodeCompare"))
        node.data_type = "FLOAT"
        node.operation = op
        self.plug(node.inputs[0], a)
        self.plug(node.inputs[1], b)
        return node.outputs["Result"]

    def switch(self, cond, if_false, if_true):
        node = self._place(self.nodes.new("GeometryNodeSwitch"))
        node.input_type = "FLOAT"
        self.plug(node.inputs["Switch"], cond)
        self.plug(node.inputs["False"], if_false)
        self.plug(node.inputs["True"], if_true)
        return node.outputs["Output"]

    def bool_and(self, a, b):
        node = self._place(self.nodes.new("FunctionNodeBooleanMath"))
        node.operation = "AND"
        self.plug(node.inputs[0], a)
        self.plug(node.inputs[1], b)
        return node.outputs[0]

    def attr(self, name):
        node = self._place(self.nodes.new("GeometryNodeInputNamedAttribute"))
        node.data_type = "FLOAT"
        node.inputs["Name"].default_value = name
        return node.outputs["Attribute"]

    def cos_blend(self, t, t0, t1, r0, r1):
        u = self.clamp01(self.math("DIVIDE", self.math("SUBTRACT", t, t0), self.math("SUBTRACT", t1, t0)))
        cosine = self.math("COSINE", self.math("MULTIPLY", u, math.pi))
        s = self.math("SUBTRACT", 0.5, self.math("MULTIPLY", 0.5, cosine))
        return self.math("ADD", r0, self.math("MULTIPLY", self.math("SUBTRACT", r1, r0), s))

    def thumb(self, th, z, height, seed, sig_th, sig_z, deg, zt, amp):
        center = self.math("ADD", self.math("RADIANS", deg), self.math("MULTIPLY", seed, 0.9))
        delta = self.math("SUBTRACT", th, center)
        wrapped = self.math("ARCTAN2", self.math("SINE", delta), self.math("COSINE", delta))
        dth = self.math("DIVIDE", wrapped, sig_th)
        dz = self.math("DIVIDE", self.math("SUBTRACT", z, self.math("MULTIPLY", zt, height)), sig_z)
        power = self.math(
            "MULTIPLY",
            -0.5,
            self.math("ADD", self.math("MULTIPLY", dth, dth), self.math("MULTIPLY", dz, dz)),
        )
        bell = self.math("EXPONENT", power)
        return self.math("MULTIPLY", amp, bell)


def _socket(iface, panel, name, key, lo, hi, text):
    sock = iface.new_socket(name=name, in_out="INPUT", socket_type="NodeSocketFloat", parent=panel)
    sock.default_value = float(DEFAULTS[key])
    sock.min_value = lo
    sock.max_value = hi
    sock.description = text
    return sock


def _vector(g, op, a, b=None):
    node = g._place(g.nodes.new("ShaderNodeVectorMath"))
    node.operation = op
    g.plug(node.inputs[0], a)
    if b is not None:
        g.plug(node.inputs[1], b)
    return node


SURFACE = "外表"


def _build_surface():
    """Outer surface as a function of one theta and one z. Called three times."""
    old = bpy.data.node_groups.get(SURFACE)
    if old is not None:
        bpy.data.node_groups.remove(old)
    ng = bpy.data.node_groups.new(SURFACE, "GeometryNodeTree")
    iface = ng.interface
    iface.new_socket(name="theta", in_out="INPUT", socket_type="NodeSocketFloat")
    iface.new_socket(name="z", in_out="INPUT", socket_type="NodeSocketFloat")
    for _panel, socket_name, key, _lo, _hi, _text in SLIDERS:
        sock = iface.new_socket(name=socket_name, in_out="INPUT", socket_type="NodeSocketFloat")
        sock.default_value = float(DEFAULTS[key])
    iface.new_socket(name="外表", in_out="OUTPUT", socket_type="NodeSocketVector")
    iface.new_socket(name="轴点", in_out="OUTPUT", socket_type="NodeSocketVector")
    iface.new_socket(name="角度", in_out="OUTPUT", socket_type="NodeSocketFloat")

    g = Graph(ng)
    gi = ng.nodes.new("NodeGroupInput")
    go = ng.nodes.new("NodeGroupOutput")
    gi.location = (-400, 0)
    go.location = (3600, 200)

    def inn(name):
        return gi.outputs[name]

    g.section("母线", 0, 400)
    theta = inn("theta")
    z = inn("z")
    height = inn("高度")
    t = g.clamp01(g.math("DIVIDE", z, height))
    belly_t = inn("腹的位置")
    neck_t = inn("颈的位置")
    low = g.cos_blend(t, 0.0, belly_t, inn("脚半径"), inn("腹半径"))
    mid = g.cos_blend(t, belly_t, neck_t, inn("腹半径"), inn("颈半径"))
    high = g.cos_blend(t, neck_t, 1.0, inn("颈半径"), inn("口半径"))
    r0 = g.switch(g.compare("LESS_THAN", t, neck_t), high, mid)
    r0 = g.switch(g.compare("LESS_THAN", t, belly_t), r0, low)

    g.section("揉搓", 900, 400)
    seed = inn("种子")
    th = g.math(
        "ADD",
        g.math("ADD", theta, g.math("MULTIPLY", g.math("RADIANS", inn("扭转")), t)),
        g.math("MULTIPLY", seed, 0.55),
    )
    env = g.smoothstep(t, 0.04, 0.14)
    fold_n = inn("褶数")
    soft = inn("杂乱")
    wave = g.math(
        "ADD",
        g.math("COSINE", g.math("MULTIPLY", fold_n, th)),
        g.math(
            "MULTIPLY",
            soft,
            g.math("COSINE", g.math("ADD", g.math("MULTIPLY", g.math("ADD", fold_n, 2.0), th), 1.15)),
        ),
    )
    fold = g.math("MULTIPLY", inn("褶深"), g.math("DIVIDE", wave, g.math("ADD", 1.0, soft)))
    sig_th = g.math("RADIANS", inn("拇指宽度"))
    sig_z = inn("拇指高低")
    acc = fold
    for label in (1, 2, 3):
        acc = g.math(
            "ADD",
            acc,
            g.thumb(
                th, z, height, seed, sig_th, sig_z,
                inn(f"拇指{label}角度"),
                inn(f"拇指{label}高度"),
                inn(f"拇指{label}深浅"),
            ),
        )
    waist_mu = g.math("SUBTRACT", neck_t, 0.05)
    waist_d = g.math("DIVIDE", g.math("SUBTRACT", t, waist_mu), 0.09)
    waist = g.math(
        "MULTIPLY",
        inn("收腰"),
        g.math("EXPONENT", g.math("MULTIPLY", -0.5, g.math("MULTIPLY", waist_d, waist_d))),
    )
    knead = g.math("MULTIPLY", env, g.math("SUBTRACT", acc, waist))

    g.section("弯折和口沿", 2000, 400)
    radius = g.math("MAXIMUM", g.math("ADD", r0, knead), g.math("ADD", inn("内腔最小半径"), inn("壁厚")))
    n_lobe = inn("口沿瓣数")
    lip = g.math(
        "ADD",
        g.math("SINE", g.math("ADD", g.math("MULTIPLY", n_lobe, th), 0.4)),
        g.math("MULTIPLY", 0.45, g.math("SINE", g.math("MULTIPLY", g.math("ADD", n_lobe, 1.0), th))),
    )
    lift = g.math(
        "MULTIPLY",
        g.math("DIVIDE", g.math("MULTIPLY", inn("口沿起伏"), lip), 1.45),
        g.smoothstep(z, g.math("SUBTRACT", height, inn("口沿过渡")), height),
    )
    z2 = g.math("ADD", z, lift)
    lean = g.math("MULTIPLY", inn("弯折"), g.math("MULTIPLY", t, t))
    bend_deg = g.math("RADIANS", inn("弯折方向"))
    bx = g.math("MULTIPLY", lean, g.math("COSINE", bend_deg))
    by = g.math("MULTIPLY", lean, g.math("SINE", bend_deg))
    px = g.math("ADD", bx, g.math("MULTIPLY", radius, g.math("COSINE", th)))
    py = g.math("ADD", by, g.math("MULTIPLY", radius, g.math("SINE", th)))

    outer = g._place(ng.nodes.new("ShaderNodeCombineXYZ"))
    g.plug(outer.inputs["X"], px)
    g.plug(outer.inputs["Y"], py)
    g.plug(outer.inputs["Z"], z2)
    axis = g._place(ng.nodes.new("ShaderNodeCombineXYZ"))
    g.plug(axis.inputs["X"], bx)
    g.plug(axis.inputs["Y"], by)
    g.plug(axis.inputs["Z"], z2)
    g.links.new(outer.outputs["Vector"], go.inputs["外表"])
    g.links.new(axis.outputs["Vector"], go.inputs["轴点"])
    g.links.new(th, go.inputs["角度"])
    return ng


def _call_surface(g, surf, gi, theta, z):
    node = g._place(g.nodes.new("GeometryNodeGroup"))
    node.node_tree = surf
    node.label = "外表"
    g.plug(node.inputs["theta"], theta)
    g.plug(node.inputs["z"], z)
    for _panel, name, _key, _lo, _hi, _text in SLIDERS:
        g.plug(node.inputs[name], gi.outputs[name])
    return node


def build_node_group():
    old = bpy.data.node_groups.get(GROUP)
    if old is not None:
        bpy.data.node_groups.remove(old)

    ng = bpy.data.node_groups.new(GROUP, "GeometryNodeTree")
    iface = ng.interface
    iface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    iface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    panels = {}
    for panel_name, _socket_name, _key, _lo, _hi, _text in SLIDERS:
        if panel_name not in panels:
            panels[panel_name] = iface.new_panel(panel_name)
    for panel_name, socket_name, key, lo, hi, text in SLIDERS:
        _socket(iface, panels[panel_name], socket_name, key, lo, hi, text)

    surf = _build_surface()
    g = Graph(ng)
    gi = g._place(ng.nodes.new("NodeGroupInput"))
    go = g._place(ng.nodes.new("NodeGroupOutput"))
    gi.location = (-200, 0)
    go.location = (1800, 200)

    g.section("采样三个邻点", 0, 200)
    theta = g.attr("theta")
    z = g.attr("z")
    mode = g.attr("mode")
    frac = g.attr("frac")
    height = gi.outputs["高度"]
    here = _call_surface(g, surf, gi, theta, z)
    step_th = _call_surface(g, surf, gi, g.math("ADD", theta, 0.02), z)
    can_up = g.compare("LESS_EQUAL", g.math("ADD", z, 0.8), height)
    z_step = g.switch(can_up, g.math("SUBTRACT", z, 0.8), g.math("ADD", z, 0.8))
    step_z = _call_surface(g, surf, gi, theta, z_step)

    g.section("沿法线留出壁厚", 700, 200)
    outer = here.outputs["外表"]
    tang_th = _vector(g, "SUBTRACT", step_th.outputs["外表"], outer).outputs["Vector"]
    delta_z = _vector(g, "SUBTRACT", step_z.outputs["外表"], outer).outputs["Vector"]
    tang_down = _vector(g, "SCALE", delta_z)
    g.plug(tang_down.inputs["Scale"], -1.0)
    tang_z = g._place(g.nodes.new("GeometryNodeSwitch"))
    tang_z.input_type = "VECTOR"
    g.plug(tang_z.inputs["Switch"], can_up)
    g.plug(tang_z.inputs["False"], tang_down.outputs["Vector"])
    g.plug(tang_z.inputs["True"], delta_z)
    normal = _vector(g, "CROSS_PRODUCT", tang_th, tang_z.outputs["Output"])
    normal = _vector(g, "NORMALIZE", normal.outputs["Vector"])
    radial = g._place(g.nodes.new("ShaderNodeCombineXYZ"))
    g.plug(radial.inputs["X"], g.math("COSINE", here.outputs["角度"]))
    g.plug(radial.inputs["Y"], g.math("SINE", here.outputs["角度"]))
    g.plug(radial.inputs["Z"], 0.0)
    facing = _vector(g, "DOT_PRODUCT", normal.outputs["Vector"], radial.outputs["Vector"])
    flipped = _vector(g, "SCALE", normal.outputs["Vector"])
    g.plug(flipped.inputs["Scale"], -1.0)
    outward = g._place(g.nodes.new("GeometryNodeSwitch"))
    outward.input_type = "VECTOR"
    g.plug(outward.inputs["Switch"], g.compare("LESS_THAN", facing.outputs["Value"], 0.0))
    g.plug(outward.inputs["False"], normal.outputs["Vector"])
    g.plug(outward.inputs["True"], flipped.outputs["Vector"])
    inset = _vector(g, "SCALE", outward.outputs["Output"])
    g.plug(inset.inputs["Scale"], gi.outputs["壁厚"])
    inner = _vector(g, "SUBTRACT", outer, inset.outputs["Vector"]).outputs["Vector"]

    g.section("底盘、壁、口沿", 1300, 200)

    def mix(a, b, factor):
        span = _vector(g, "SUBTRACT", b, a).outputs["Vector"]
        scaled = _vector(g, "SCALE", span)
        g.plug(scaled.inputs["Scale"], factor)
        return _vector(g, "ADD", a, scaled.outputs["Vector"]).outputs["Vector"]

    on_wall = mix(inner, outer, frac)
    on_outer_disk = mix(here.outputs["轴点"], outer, frac)
    on_inner_disk = mix(here.outputs["轴点"], inner, frac)
    outer_disk = g.bool_and(g.compare("GREATER_THAN", mode, 0.5), g.compare("LESS_THAN", mode, 1.5))
    inner_disk = g.compare("GREATER_THAN", mode, 1.5)
    picked = g._place(g.nodes.new("GeometryNodeSwitch"))
    picked.input_type = "VECTOR"
    g.plug(picked.inputs["Switch"], outer_disk)
    g.plug(picked.inputs["False"], on_wall)
    g.plug(picked.inputs["True"], on_outer_disk)
    picked2 = g._place(g.nodes.new("GeometryNodeSwitch"))
    picked2.input_type = "VECTOR"
    g.plug(picked2.inputs["Switch"], inner_disk)
    g.plug(picked2.inputs["False"], picked.outputs["Output"])
    g.plug(picked2.inputs["True"], on_inner_disk)

    setpos = g._place(g.nodes.new("GeometryNodeSetPosition"))
    g.links.new(gi.outputs["Geometry"], setpos.inputs["Geometry"])
    g.links.new(picked2.outputs["Output"], setpos.inputs["Position"])
    g.links.new(setpos.outputs["Geometry"], go.inputs["Geometry"])
    return ng


def attach(obj):
    ng = build_node_group()
    for mod in list(obj.modifiers):
        if mod.type == "NODES":
            obj.modifiers.remove(mod)
    mod = obj.modifiers.new(GROUP, "NODES")
    mod.node_group = ng
    mod.show_expanded = True
    return ng, mod
