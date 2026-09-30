# Detailed wire shopping cart (v1), exported as separately movable parts (GLB).
# Run: Blender -b --factory-startup --python cart_wire.py -- <out.glb>
import bpy, sys, math
from mathutils import Vector

out = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "cart_wire.glb"
bpy.ops.wm.read_factory_settings(use_empty=True)
col = bpy.context.scene.collection
lerp = lambda a, b, t: a + (b - a) * t


def wires(name, polylines, r, cyclic=(), res=2):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = r; cu.bevel_resolution = res; cu.use_fill_caps = True
    for i, pts in enumerate(polylines):
        s = cu.splines.new("POLY"); s.points.add(len(pts) - 1)
        for j, p in enumerate(pts):
            s.points[j].co = (p[0], p[1], p[2], 1)
        s.use_cyclic_u = i in cyclic
    ob = bpy.data.objects.new(name, cu); col.objects.link(ob); return ob


def smooth_curve(name, pts, r, res=12):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"
    cu.bevel_depth = r; cu.bevel_resolution = 3; cu.use_fill_caps = True
    s = cu.splines.new("BEZIER"); s.bezier_points.add(len(pts) - 1)
    for j, p in enumerate(pts):
        bp = s.bezier_points[j]; bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    s.resolution_u = res
    ob = bpy.data.objects.new(name, cu); col.objects.link(ob); return ob


def to_mesh(obs, name):
    bpy.ops.object.select_all(action="DESELECT")
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.convert(target="MESH")
    if len(obs) > 1: bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active; ob.name = ob.data.name = name
    bpy.ops.object.shade_smooth(); bpy.ops.object.select_all(action="DESELECT"); return ob


def cyl(name, r, depth, loc, rot=(0, 0, 0), verts=32, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    ob = bpy.context.active_object; ob.name = name
    if bevel:
        m = ob.modifiers.new("b", "BEVEL"); m.width = bevel; m.segments = 3; m.limit_method = "ANGLE"
    bpy.ops.object.shade_smooth(); return ob


def cube(name, size, loc, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object; ob.name = name; ob.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        m = ob.modifiers.new("b", "BEVEL"); m.width = bevel; m.segments = 3
    return ob


def apply_mods(ob):
    bpy.ops.object.select_all(action="DESELECT"); ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    for m in list(ob.modifiers): bpy.ops.object.modifier_apply(modifier=m.name)


def join(obs, name):
    for o in obs: apply_mods(o)
    bpy.ops.object.select_all(action="DESELECT")
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]; bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active; ob.name = ob.data.name = name
    bpy.ops.object.select_all(action="DESELECT"); return ob


TOP = [Vector((-0.42, -0.27, 0.98)), Vector((0.42, -0.27, 0.98)), Vector((0.42, 0.27, 0.98)), Vector((-0.42, 0.27, 0.98))]
BOT = [Vector((-0.37, -0.22, 0.58)), Vector((0.30, -0.22, 0.58)), Vector((0.30, 0.22, 0.58)), Vector((-0.37, 0.22, 0.58))]
vert = []
for i in range(4):
    a, b, c, d = TOP[i], TOP[(i + 1) % 4], BOT[(i + 1) % 4], BOT[i]
    n = 24 if i % 2 == 0 else 15
    for k in range(1, n):
        t = k / n; vert.append([lerp(a, b, t), lerp(d, c, t)])
rings = [[lerp(BOT[i], TOP[i], k / 7) for i in range(4)] for k in range(1, 7)]
bottom = [[lerp(BOT[0], BOT[1], k / 17), lerp(BOT[3], BOT[2], k / 17)] for k in range(18)]
bottom += [[lerp(BOT[0], BOT[3], k / 11), lerp(BOT[1], BOT[2], k / 11)] for k in range(1, 11)]
corners = [[BOT[i], TOP[i]] for i in range(4)]
to_mesh([wires("bv", vert, 0.0024), wires("br", rings, 0.0026, cyclic=range(len(rings))), wires("bb", bottom, 0.0024),
         wires("bc", corners, 0.0045), wires("bl", [BOT], 0.0045, cyclic=[0])], "Basket")
to_mesh([wires("r1", [TOP], 0.0075, cyclic=[0], res=3), wires("r2", [[p + Vector((0, 0, -0.03)) for p in TOP]], 0.004, cyclic=[0])], "Rim")

seat = [[Vector((-0.405, lerp(-0.2, 0.2, k / 8), 0.95)), Vector((-0.405, lerp(-0.2, 0.2, k / 8), 0.78))] for k in range(9)]
seat += [[Vector((-0.405, -0.2, lerp(0.78, 0.95, k / 3))), Vector((-0.405, 0.2, lerp(0.78, 0.95, k / 3)))] for k in range(4)]
to_mesh([wires("seat", seat, 0.003)], "Seat")

hl = [smooth_curve("h" + str(s), [(-0.42, 0.25 * s, 0.975), (-0.47, 0.25 * s, 1.03), (-0.53, 0.25 * s, 1.075), (-0.56, 0.22 * s, 1.09)], 0.011) for s in (-1, 1)]
to_mesh(hl + [wires("hb", [[Vector((-0.56, -0.22, 1.09)), Vector((-0.56, 0.22, 1.09))]], 0.011, res=4)], "Handle")
g = cyl("Grip", 0.02, 0.4, (-0.56, 0, 1.09), rot=(math.pi / 2, 0, 0), verts=40, bevel=0.006)
caps = [cyl("gc", 0.023, 0.018, (-0.56, 0.205 * s, 1.09), rot=(math.pi / 2, 0, 0), verts=40, bevel=0.005) for s in (-1, 1)]
join([g] + caps, "Grip")

def rounded(pts, r, n=8):
    """Polyline with every interior corner replaced by a quarter-ish arc of radius r."""
    pts = [Vector(p) for p in pts]; out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, p, b = pts[i - 1], pts[i], pts[i + 1]
        t1, t2 = p + (a - p).normalized() * r, p + (b - p).normalized() * r
        for k in range(n + 1):
            t = k / n; out.append(t1 * (1 - t) ** 2 + p * 2 * t * (1 - t) + t2 * t * t)
    out.append(pts[-1]); return out


# frame: straight tubes only, one per side: rear post down, big rounded corner, floor rail forward to the front wheel
XR, XF, ZF, YF = -0.405, 0.30, 0.125, 0.235
fp = [wires("f", [rounded([(XR, YF * s, 0.97), (XR, YF * s, ZF), (XF, YF * s, ZF)], 0.21, 16) for s in (-1, 1)], 0.012, res=3)]
fp.append(wires("fx", [[Vector((XR, -YF, 0.2)), Vector((XR, YF, 0.2))], [Vector((XF, -YF, ZF)), Vector((XF, YF, ZF))],
                       [Vector((XR, -YF, 0.55)), Vector((XR, YF, 0.55))]], 0.01))
to_mesh(fp, "Frame")

tl = [[Vector((lerp(-0.36, 0.3, k / 18), -0.2, 0.2)), Vector((lerp(-0.36, 0.3, k / 18), 0.2, 0.2))] for k in range(19)]
tl += [[Vector((-0.36, lerp(-0.2, 0.2, k / 5), 0.2)), Vector((0.3, lerp(-0.2, 0.2, k / 5), 0.2))] for k in range(6)]
to_mesh([wires("t", tl, 0.0026), wires("tb", [[Vector((-0.36, -0.2, 0.205)), Vector((0.3, -0.2, 0.205)), Vector((0.3, 0.2, 0.205)), Vector((-0.36, 0.2, 0.205))]], 0.005, cyclic=[0])], "Tray")

wp = []
for (x, y) in [(XR, -YF), (XR, YF), (XF, -YF), (XF, YF)]:
    wp.append(cube("pl", (0.07, 0.06, 0.008), (x, y, 0.118), bevel=0.002))
    wp.append(cyl("sw", 0.014, 0.02, (x, y, 0.106), verts=24))
    for s in (-1, 1): wp.append(cube("fk", (0.05, 0.005, 0.07), (x + 0.01, y + 0.02 * s, 0.075), bevel=0.0015))
    wp.append(cyl("tire", 0.05, 0.028, (x + 0.015, y, 0.05), rot=(math.pi / 2, 0, 0), verts=48, bevel=0.008))
    wp.append(cyl("hub", 0.022, 0.034, (x + 0.015, y, 0.05), rot=(math.pi / 2, 0, 0), verts=32, bevel=0.003))
    wp.append(cyl("ax", 0.005, 0.048, (x + 0.015, y, 0.05), rot=(math.pi / 2, 0, 0), verts=12))
join(wp, "Wheels")
apply_mods(cube("Plate", (0.006, 0.16, 0.035), (-0.545, 0, 1.05), bevel=0.002))

# big 3D question mark standing in the basket
cu = bpy.data.curves.new("Q", "FONT"); cu.body = "?"
cu.font = bpy.data.fonts.load("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")
cu.size = 1.0; cu.extrude = 0.0074; cu.bevel_depth = 0.0077; cu.bevel_resolution = 3; cu.align_x = "CENTER"; cu.resolution_u = 10
qo = bpy.data.objects.new("Question", cu); col.objects.link(qo)
qo.rotation_euler = (math.pi / 2, 0, 0)
bpy.context.view_layer.update()
q = to_mesh([qo], "Question")
bpy.ops.object.select_all(action="DESELECT"); q.select_set(True); bpy.context.view_layer.objects.active = q
bpy.ops.object.transform_apply(rotation=True)
bb = [q.matrix_world @ Vector(c) for c in q.bound_box]
zmin = min(v.z for v in bb); cx = sum(v.x for v in bb) / 8; cy = sum(v.y for v in bb) / 8
h = max(v.z for v in bb) - zmin; k = 0.546 / h
q.scale = (k, k, k); bpy.ops.object.transform_apply(scale=True)
q.location = (-cx * k - 0.03, -cy * k, 0.62 - zmin * k)
bpy.ops.object.transform_apply(location=True)
bpy.ops.object.shade_smooth()

bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_apply=True, export_yup=True, export_materials="NONE")
print("TOTAL_TRIS", sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type == "MESH"))
