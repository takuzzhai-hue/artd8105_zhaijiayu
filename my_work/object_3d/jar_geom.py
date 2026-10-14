"""Hand-kneaded jar. One stitched shell. Python standard library only.

The wall moves as one sheet of clay: outer and inner share the same knead,
twist, bend and lip wave, and stay `wall` apart. A hard floor keeps a hole
open. Topology is fixed: outer skin, outer base, inner skin, inner floor, lip.
"""

from __future__ import annotations

import math

TWO_PI = 2.0 * math.pi

# Numbers the Geometry Nodes sliders start at. The node tree in build_nodes.py
# has to stay in step with deformed() below.
DEFAULTS = {
    "height": 160.0,
    "r_foot": 28.0,
    "r_belly": 52.0,
    "r_neck": 34.0,
    "r_rim": 46.0,
    "belly_t": 0.40,
    "neck_t": 0.68,
    "wall": 4.0,
    "bottom": 3.6,
    "min_wall": 1.6,
    "min_hole": 14.0,
    "fold_n": 3.0,
    "fold_depth": 9.0,
    "fold_soft": 0.65,
    "waist": 4.5,
    "seed": 2.0,
    "thumb_deg": 50.0,
    "thumb_sigma": 30.0,
    "thumb1_deg": 30.0,
    "thumb1_t": 0.46,
    "thumb1_amp": -6.0,
    "thumb2_deg": 145.0,
    "thumb2_t": 0.34,
    "thumb2_amp": -4.5,
    "thumb3_deg": 255.0,
    "thumb3_t": 0.58,
    "thumb3_amp": 4.5,
    "twist": 120.0,
    "bend": 22.0,
    "bend_deg": 32.0,
    "rim_wave": 10.0,
    "rim_lobes": 3.0,
    "rim_band": 28.0,
    "n_theta": 144,
    "n_z": 100,
    "n_rad": 6,
    "n_rim": 3,
}

PARAM_KEYS = (
    "height",
    "r_foot",
    "r_belly",
    "r_neck",
    "r_rim",
    "belly_t",
    "neck_t",
    "wall",
    "bottom",
    "min_wall",
    "min_hole",
    "fold_n",
    "fold_depth",
    "fold_soft",
    "waist",
    "seed",
    "thumb_deg",
    "thumb_sigma",
    "thumb1_deg",
    "thumb1_t",
    "thumb1_amp",
    "thumb2_deg",
    "thumb2_t",
    "thumb2_amp",
    "thumb3_deg",
    "thumb3_t",
    "thumb3_amp",
    "twist",
    "bend",
    "bend_deg",
    "rim_wave",
    "rim_lobes",
    "rim_band",
    "n_theta",
    "n_z",
    "n_rad",
    "n_rim",
)


def clamp(value, lo, hi):
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def smoothstep(x, a, b):
    if b <= a:
        return 1.0 if x >= b else 0.0
    t = clamp((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def wrap_angle(dtheta):
    while dtheta > math.pi:
        dtheta -= TWO_PI
    while dtheta < -math.pi:
        dtheta += TWO_PI
    return dtheta


def _cos_blend(t, t0, t1, r0, r1):
    u = 0.0 if t1 <= t0 else clamp((t - t0) / (t1 - t0), 0.0, 1.0)
    s = 0.5 - 0.5 * math.cos(math.pi * u)
    return r0 + (r1 - r0) * s


def R0(z, p):
    """Jar curve through foot, belly, neck, rim."""
    h = float(p["height"])
    if h <= 0.0:
        raise ValueError("height must be > 0")
    t = clamp(z / h, 0.0, 1.0)
    belly_t = float(p["belly_t"])
    neck_t = float(p["neck_t"])
    if not (0.0 < belly_t < neck_t < 1.0):
        raise ValueError("need 0 < belly position < neck position < 1")
    if t <= belly_t:
        return _cos_blend(t, 0.0, belly_t, p["r_foot"], p["r_belly"])
    if t <= neck_t:
        return _cos_blend(t, belly_t, neck_t, p["r_belly"], p["r_neck"])
    return _cos_blend(t, neck_t, 1.0, p["r_neck"], p["r_rim"])


def knead(th, z, p):
    """Soft folds, three thumbs, and a cinched waist. `th` is already twisted."""
    h = float(p["height"])
    t = clamp(z / h, 0.0, 1.0)
    env = smoothstep(t, 0.04, 0.14)
    n = float(p["fold_n"])
    soft = float(p["fold_soft"])
    if soft < 0.0:
        soft = 0.0
    wave = math.cos(n * th) + soft * math.cos((n + 2.0) * th + 1.15)
    acc = float(p["fold_depth"]) * wave / (1.0 + soft)
    sig_th = math.radians(max(float(p["thumb_deg"]), 1.0))
    sig_z = max(float(p["thumb_sigma"]), 1.0)
    seed = float(p["seed"])
    for deg, zt, amp in (
        (p["thumb1_deg"], p["thumb1_t"], p["thumb1_amp"]),
        (p["thumb2_deg"], p["thumb2_t"], p["thumb2_amp"]),
        (p["thumb3_deg"], p["thumb3_t"], p["thumb3_amp"]),
    ):
        center = math.radians(float(deg)) + seed * 0.9
        dth = wrap_angle(th - center) / sig_th
        dz = (z - float(zt) * h) / sig_z
        acc += float(amp) * math.exp(-0.5 * (dth * dth + dz * dz))
    neck = float(p["neck_t"])
    d = (t - (neck - 0.05)) / 0.09
    acc -= float(p["waist"]) * math.exp(-0.5 * d * d)
    return acc * env


def rim_lift(th, z, p):
    h = float(p["height"])
    band = float(p["rim_band"])
    w = smoothstep(z, h - band, h)
    n = float(p["rim_lobes"])
    wave = math.sin(n * th + 0.4) + 0.45 * math.sin((n + 1.0) * th)
    return float(p["rim_wave"]) * wave / 1.45 * w


def deformed(theta, z, p):
    """Radius pair, twisted angle, lifted z, and the sideways push."""
    h = float(p["height"])
    t = clamp(z / h, 0.0, 1.0)
    th = theta + math.radians(float(p["twist"])) * t + float(p["seed"]) * 0.55
    r_mid = R0(z, p) + knead(th, z, p)
    floor = float(p["min_hole"]) + float(p["wall"])
    if r_mid < floor:
        r_mid = floor
    ang = math.radians(float(p["bend_deg"]))
    lean = float(p["bend"]) * t * t
    return (
        r_mid,
        r_mid - float(p["wall"]),
        th,
        z + rim_lift(th, z, p),
        lean * math.cos(ang),
        lean * math.sin(ang),
    )


def point(r, th, z, bx, by):
    return (bx + r * math.cos(th), by + r * math.sin(th), z)


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _scale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _length(a):
    return math.sqrt(_dot(a, a))


def outer_xyz(theta, z, p):
    """Outside of the clay, before the wall is given a thickness."""
    _r_out, _r_in, th, z2, bx, by = deformed(theta, z, p)
    return point(_r_out, th, z2, bx, by), th, bx, by


def surface_pair(theta, z, p):
    """Outer point, and the inner point wall-thickness back along the normal.

    Radial subtraction makes a steep fold thinner than the wall. Moving along
    the normal keeps the sheet about `wall` thick, which is what a pinch does
    to clay.
    """
    h = float(p["height"])
    zc = clamp(z, 0.0, h)
    origin, th, _bx, _by = outer_xyz(theta, zc, p)
    dth = 0.02
    dz = 0.8
    if zc + dz <= h:
        z_step = zc + dz
        z_sign = 1.0
    else:
        z_step = zc - dz
        z_sign = -1.0
    step_th, _th2, _bx2, _by2 = outer_xyz(theta + dth, zc, p)
    step_z, _th3, _bx3, _by3 = outer_xyz(theta, z_step, p)
    tang_th = _sub(step_th, origin)
    tang_z = _scale(_sub(step_z, origin), z_sign)
    normal = _cross(tang_th, tang_z)
    length = _length(normal)
    if length < 1e-8:
        normal = (math.cos(th), math.sin(th), 0.0)
    else:
        normal = _scale(normal, 1.0 / length)
    outward = (math.cos(th), math.sin(th), 0.0)
    if _dot(normal, outward) < 0.0:
        normal = _scale(normal, -1.0)
    wall = float(p["wall"])
    return origin, _sub(origin, _scale(normal, wall))


def add_vert(verts, attrs, xyz, theta, z, mode, frac):
    verts.append(xyz)
    attrs["theta"].append(float(theta))
    attrs["z"].append(float(z))
    attrs["mode"].append(float(mode))
    attrs["frac"].append(float(frac))
    return len(verts) - 1


def add_tri(faces, a, b, c):
    if a == b or b == c or c == a:
        return
    faces.append((a, b, c))


def add_quad(faces, a, b, c, d):
    add_tri(faces, a, b, c)
    add_tri(faces, a, c, d)


def _lerp(a, b, f):
    return (a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]), a[2] + f * (b[2] - a[2]))


def _put(verts, attrs, p, radius, theta, z, mode, frac):
    if mode == 0:
        outer, inner = surface_pair(theta, z, p)
        xyz = _lerp(inner, outer, frac)
    elif mode == 1:
        r_out, _r_in, th, z2, bx, by = deformed(theta, z, p)
        xyz = point(frac * r_out, th, z2, bx, by)
    else:
        _outer, inner = surface_pair(theta, z, p)
        _r_out, _r_in, _th, z2, bx, by = deformed(theta, z, p)
        xyz = (
            bx + frac * (inner[0] - bx),
            by + frac * (inner[1] - by),
            z2 + frac * (inner[2] - z2),
        )
    return add_vert(verts, attrs, xyz, theta, z, mode, frac)


def build_jar(params=None):
    p = dict(DEFAULTS)
    if params:
        p.update(params)
    h = float(p["height"])
    bottom = float(p["bottom"])
    wall = float(p["wall"])
    min_wall = float(p["min_wall"])
    n_th = int(p["n_theta"])
    n_z = int(p["n_z"])
    n_rad = int(p["n_rad"])
    n_rim = int(p["n_rim"])
    if n_th < 12 or n_z < 8 or n_rad < 2 or n_rim < 1:
        raise ValueError("grid is too coarse")
    if not (0.0 < bottom < h):
        raise ValueError("bottom thickness must sit inside the height")
    if wall <= min_wall:
        raise ValueError("wall must be thicker than min_wall")
    if bottom < min_wall:
        raise ValueError("bottom is thinner than min_wall")
    R0(0.0, p)

    z_outer = [i * h / n_z for i in range(n_z + 1)]
    i_bottom = min(range(n_z + 1), key=lambda i: abs(z_outer[i] - bottom))
    if i_bottom <= 0:
        i_bottom = 1
    if i_bottom >= n_z:
        i_bottom = n_z - 1
    z_outer[i_bottom] = bottom
    thetas = [k * TWO_PI / n_th for k in range(n_th)]

    verts = []
    faces = []
    attrs = {"theta": [], "z": [], "mode": [], "frac": []}

    ow = [[0] * n_th for _ in range(n_z + 1)]
    for iz, z in enumerate(z_outer):
        for it, th in enumerate(thetas):
            ow[iz][it] = _put(verts, attrs, p, None, th, z, 0, 1.0)

    iw = [[None] * n_th for _ in range(n_z + 1)]
    for iz in range(i_bottom, n_z + 1):
        z = z_outer[iz]
        for it, th in enumerate(thetas):
            iw[iz][it] = _put(verts, attrs, p, None, th, z, 0, 0.0)

    for iz in range(n_z):
        for it in range(n_th):
            it2 = (it + 1) % n_th
            add_quad(faces, ow[iz][it], ow[iz][it2], ow[iz + 1][it2], ow[iz + 1][it])

    for iz in range(i_bottom, n_z):
        for it in range(n_th):
            it2 = (it + 1) % n_th
            add_quad(faces, iw[iz][it], iw[iz + 1][it], iw[iz + 1][it2], iw[iz][it2])

    add_vert(verts, attrs, (0.0, 0.0, 0.0), 0.0, 0.0, 1, 0.0)
    # center was placed at origin; bend at z=0 is 0, so that is correct.
    # Re-place properly in case bend is ever non-zero at z=0.
    r_out, r_in, th, z2, bx, by = deformed(0.0, 0.0, p)
    verts[-1] = point(0.0, th, z2, bx, by)
    ob_center = len(verts) - 1

    rings_out = []
    for ir in range(1, n_rad):
        frac = ir / n_rad
        row = []
        for it, th0 in enumerate(thetas):
            row.append(_put(verts, attrs, p, None, th0, 0.0, 1, frac))
        rings_out.append(row)
    rings_out.append([ow[0][it] for it in range(n_th)])
    first = rings_out[0]
    for it in range(n_th):
        it2 = (it + 1) % n_th
        add_tri(faces, ob_center, first[it2], first[it])
    for ir in range(len(rings_out) - 1):
        a = rings_out[ir]
        b = rings_out[ir + 1]
        for it in range(n_th):
            it2 = (it + 1) % n_th
            add_quad(faces, a[it], a[it2], b[it2], b[it])

    r_out, r_in, th, z2, bx, by = deformed(0.0, bottom, p)
    ib_center = add_vert(verts, attrs, point(0.0, th, z2, bx, by), 0.0, bottom, 2, 0.0)
    rings_in = []
    for ir in range(1, n_rad):
        frac = ir / n_rad
        row = []
        for it, th0 in enumerate(thetas):
            row.append(_put(verts, attrs, p, None, th0, bottom, 2, frac))
        rings_in.append(row)
    rings_in.append([iw[i_bottom][it] for it in range(n_th)])
    first = rings_in[0]
    for it in range(n_th):
        it2 = (it + 1) % n_th
        add_tri(faces, ib_center, first[it], first[it2])
    for ir in range(len(rings_in) - 1):
        a = rings_in[ir]
        b = rings_in[ir + 1]
        for it in range(n_th):
            it2 = (it + 1) % n_th
            add_quad(faces, a[it], b[it], b[it2], a[it2])

    rim = [[iw[n_z][it] for it in range(n_th)]]
    for s in range(1, n_rim):
        frac = s / n_rim
        row = []
        for it, th0 in enumerate(thetas):
            row.append(_put(verts, attrs, p, None, th0, h, 0, frac))
        rim.append(row)
    rim.append([ow[n_z][it] for it in range(n_th)])
    for ir in range(len(rim) - 1):
        a = rim[ir]
        b = rim[ir + 1]
        for it in range(n_th):
            it2 = (it + 1) % n_th
            add_quad(faces, a[it], b[it], b[it2], a[it2])

    min_radial = None
    min_normal = bottom
    clamped = 0
    samples = 0
    floor = float(p["min_hole"]) + wall
    for iz, z in enumerate(z_outer):
        if iz < i_bottom:
            continue
        for th in thetas:
            t = z / h
            th_tw = th + math.radians(float(p["twist"])) * t + float(p["seed"]) * 0.55
            raw = R0(z, p) + knead(th_tw, z, p)
            if raw < floor - 1e-6:
                clamped += 1
            samples += 1
            outer, inner = surface_pair(th, z, p)
            dist = _length(_sub(outer, inner))
            if min_radial is None or dist < min_radial:
                min_radial = dist
            if dist < min_normal:
                min_normal = dist

    profile = []
    for t, name in ((0.0, "foot"), (p["belly_t"], "belly"), (p["neck_t"], "neck"), (1.0, "rim")):
        z = t * h
        profile.append({"name": name, "t": t, "z": z, "R0": R0(z, p)})

    info = {
        "params": p,
        "attrs": attrs,
        "n_verts": len(verts),
        "n_faces": len(faces),
        "i_bottom": i_bottom,
        "min_radial_wall": min_radial,
        "min_normal_wall": min_normal,
        "clamped_samples": clamped,
        "samples": samples,
        "profile": profile,
    }
    return verts, faces, info


def signed_volume(verts, faces):
    acc = 0.0
    for a, b, c in faces:
        x0, y0, z0 = verts[a]
        x1, y1, z1 = verts[b]
        x2, y2, z2 = verts[c]
        acc += (
            x0 * (y1 * z2 - y2 * z1)
            + x1 * (y2 * z0 - y0 * z2)
            + x2 * (y0 * z1 - y1 * z0)
        )
    return acc / 6.0


def edge_key(a, b):
    return (a, b) if a < b else (b, a)


def mesh_check(verts, faces, min_wall, min_measured):
    n_v = len(verts)
    n_f = len(faces)
    failures = []
    undirected = {}
    directed = {}
    for a, b, c in faces:
        for u, v in ((a, b), (b, c), (c, a)):
            directed[(u, v)] = directed.get((u, v), 0) + 1
            k = edge_key(u, v)
            undirected[k] = undirected.get(k, 0) + 1
    n_e = len(undirected)
    n_boundary = sum(1 for c in undirected.values() if c == 1)
    n_nonmanifold = sum(1 for c in undirected.values() if c != 2)
    n_bad_orient = 0
    for (u, v), count in undirected.items():
        if count != 2:
            continue
        if directed.get((u, v), 0) != 1 or directed.get((v, u), 0) != 1:
            n_bad_orient += 1

    parent = list(range(n_v))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    seen = [False] * n_v
    for a, b, c in faces:
        union(a, b)
        union(b, c)
        seen[a] = seen[b] = seen[c] = True
    roots = set()
    for i, used in enumerate(seen):
        if used:
            roots.add(find(i))
    n_cc = len(roots)
    chi = n_v - n_e + n_f
    vol = signed_volume(verts, faces)

    if n_boundary != 0:
        failures.append(f"boundary edges={n_boundary} (must be 0)")
    if n_nonmanifold != 0:
        failures.append(f"non-manifold edges={n_nonmanifold} (must be 0)")
    if n_bad_orient != 0:
        failures.append(f"edges not shared by two opposite faces={n_bad_orient}")
    if n_cc != 1:
        failures.append(f"connected components={n_cc} (must be 1)")
    if chi != 2:
        failures.append(f"V-E+F={chi} (must be 2)")
    if vol <= 0.0:
        failures.append(f"signed volume={vol:.6f} (must be > 0)")
    if min_measured is None or min_measured < min_wall - 1e-6:
        failures.append(f"thinnest wall={min_measured} mm (must be ≥ {min_wall} mm)")

    stats = {
        "V": n_v,
        "E": n_e,
        "F": n_f,
        "chi": chi,
        "boundary": n_boundary,
        "nonmanifold": n_nonmanifold,
        "bad_orient": n_bad_orient,
        "components": n_cc,
        "volume": vol,
        "min_wall_required": min_wall,
        "min_wall_measured": min_measured,
    }
    return (len(failures) == 0), failures, stats
