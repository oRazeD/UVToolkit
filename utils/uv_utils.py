import numpy as np
from time import time
from math import atan, cos, sin, pi
from collections import deque, defaultdict

import bpy
import bmesh


AXIS_U = 0
AXIS_V = 1
NEGATIVE = 0
POSITIVE = 1


def debug_time(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(f"{func.__name__.upper()}: {(time() - start): .4f} sec")
        return result
    return wrapper


def calc_length_sorted_uv_edges(uv, uv_edge_loop):
    uv_edges_length = []

    steps = len(uv_edge_loop) - 1
    for idx in range(steps):
        first_uv_vert_co = uv_edge_loop[idx][0][uv].uv
        second_uv_vert_co = uv_edge_loop[idx + 1][0][uv].uv
        edge_length = (first_uv_vert_co - second_uv_vert_co).length
        uv_edges_length.append(edge_length)
    return uv_edges_length


def get_uv_edges(uv, loops):
    uv_edges = set()

    def get_uv_edge():
        for l in loops:
            next_loop = l.link_loop_next
            if next_loop in loops:
                yield (l[uv].uv[:], next_loop[uv].uv[:])

    for uv_edge in get_uv_edge():
        if (uv_edge[1], uv_edge[0]) not in uv_edges:
            uv_edges.add(uv_edge)
    return uv_edges


def get_sorted_uv_edge_loops(uv, loops):
    def collect_linked_uv_verts(uv_vert):
        def get_other_uv_vert(uv_vert, uv_edge):
            for v in uv_edge:
                if v != uv_vert:
                    other_uv_vert = v
                    return other_uv_vert

        def get_uv_edge(uv_vert):
            for uv_edge in uv_edges:
                if uv_vert in uv_edge:
                    return uv_edge

        while True:
            uv_edge = get_uv_edge(uv_vert)
            if uv_edge:
                uv_vert = get_other_uv_vert(uv_vert, uv_edge)
                uv_edges.discard(uv_edge)
                yield uv_vert
            else:
                break

    def get_sorted_uv_edge_loop():
        init_uv_edge = uv_edges.pop()

        first_uv_vert = init_uv_edge[0]
        second_uv_vert = init_uv_edge[1]
        # Walk on both sides of the loop.
        # <--o--o-->
        sorted_uv_verts_co = deque([first_uv_vert, second_uv_vert])

        for uv_vert in collect_linked_uv_verts(first_uv_vert):
            sorted_uv_verts_co.appendleft(uv_vert)
        for uv_vert in collect_linked_uv_verts(second_uv_vert):
            sorted_uv_verts_co.append(uv_vert)
        # Grab loops from uv coordinates
        sorted_uv_verts = []
        for uv_vert_co in sorted_uv_verts_co:
            uv_vert = [l for l in loops if l[uv].uv[:] == uv_vert_co]
            sorted_uv_verts.append(uv_vert)
        return sorted_uv_verts

    uv_edges = get_uv_edges(uv, loops)
    sorted_uv_edge_loops = []

    if not uv_edges:
        return

    while len(uv_edges) != 0:
        sorted_uv_edge_loop = get_sorted_uv_edge_loop()
        if sorted_uv_edge_loop:
            sorted_uv_edge_loops.append(sorted_uv_edge_loop)
    return sorted_uv_edge_loops


def deselect_all_loops_uv(uv, bm):
    for f in bm.faces:
        for l in f.loops:
            l[uv].select = False


def select_all_faces(bm):
    for f in bm.faces:
        f.select = True


def deselect_all_faces(bm):
    for f in bm.faces:
        f.select = False


def create_list_of_selected_faces(bm):
    return [f for f in bm.faces if f.select]


def create_list_of_loops_from_uv_selection(uv, faces):
    return [l for f in faces for l in f.loops if l[uv].select]


def create_set_of_loops_from_uv_selection(uv, faces):
    return {l for f in faces for l in f.loops if l[uv].select}


def verts_from_uv_selection(uv, faces):
    return {l.vert for f in faces for l in f.loops if l[uv].select}


def clear_all_seams(bm):
    for e in bm.edges:
        e.seam = False


def store_all_seams(bm):
    return [e for e in bm.edge if e.seam]


def get_bbox(uv, faces):
    """
    Return lower left point and top right point.
    """
    if isinstance(faces, list):
        initial_point = faces[0].loops[0][uv].uv
    else:
        for face in faces:
            break
        initial_point = face.loops[0][uv].uv

    u_min, v_min = initial_point
    u_max, v_max = initial_point

    for f in faces:
        for l in f.loops:
            u, v = l[uv].uv[0], l[uv].uv[1]
            if u < u_min:
                u_min = u
            if u_max < u:
                u_max = u
            if v < v_min:
                v_min = v
            if v_max < v:
                v_max = v
    return (u_min, v_min), (u_max, v_max)


def get_bbox_size(bbox):
    u1, v1 = bbox[0][0], bbox[0][1]
    u2, v2 = bbox[1][0], bbox[1][1]
    bbox_width = u2 - u1
    bbox_height = v2 - v1
    return bbox_width, bbox_height


def calc_bbox_center(bbox):
    u1, v1 = bbox[0][0], bbox[0][1]
    u2, v2 = bbox[1][0], bbox[1][1]
    return ((u2 - u1) / 2 + u1, (v2 - v1) / 2 + v1)


def get_udim_co(point):
    """
    Return udim coordinates by a point coordinate.
    """
    point_u, point_v = point[0], point[1]

    u1, v1 = point_u // 1, point_v // 1
    u2, v2 = u1 + 1, v1 + 1
    return (((u1, v1)), ((u2, v2)))


def calc_slope(context, point_a, point_b):
    u1, v1 = point_a[0], point_a[1]
    u2, v2 = point_b[0], point_b[1]
    acitve_img = get_non_square_acitve_img(context)
    if acitve_img:
        width, height = acitve_img.size
        if u1 > u2:
            pivot_u = (u1 - u2) / 2
        else:
            pivot_u = (u2 - u1) / 2
        if v1 > v2:
            pivot_v = (v1 - v2) / 2
        else:
            pivot_v = (v2 - v1) / 2
        pivot = (pivot_u, pivot_v)

        if width > height:
            scale = scale_matrix((width / height, 1), pivot)
        else:
            scale = scale_matrix((1 / (height / width), 1), pivot)
        point_a = scale.dot(np.array([u1, v1, 1]))[:2]
        point_b = scale.dot(np.array([u2, v2, 1]))[:2]
        u1, v1 = point_a[0], point_a[1]
        u2, v2 = point_b[0], point_b[1]
    if u2 - u1 == 0:
        return 0
    else:
        return atan((v2 - v1) / (u2 - u1))


def min_angle_to_axis(slope):
    """
    Returns the angle to the nearest axis.
    """
    if 0 < slope:
        if slope < pi / 2 - slope:
            angle = slope * -1
        else:
            angle = pi / 2 - slope
    elif slope < 0:
        if slope < pi / -2 - slope:
            angle = (pi / -2 - slope)
        else:
            angle = slope * -1
    else:
        angle = 0
    return angle


def find_nearest_axis(slope, point_a, point_b):
    u1, v1 = point_a[0], point_a[1]
    u2, v2 = point_b[0], point_b[1]

    if slope == 0:
        if v1 == v2:
            axis = AXIS_U
        if u1 == u2:
            axis = AXIS_V
    else:
        if pi / 2 - abs(slope) > abs(slope):
            axis = AXIS_U
        else:
            axis = AXIS_V
    return axis


def get_direction(axis, point_a, point_b):
    u1, v1 = point_a[0], point_a[1]
    u2, v2 = point_b[0], point_b[1]

    if axis == AXIS_U:
        if u1 < u2:
            direction = POSITIVE
        else:
            direction = NEGATIVE
    if axis == AXIS_V:
        if v1 < v2:
            direction = POSITIVE
        else:
            direction = NEGATIVE
    return direction


def translate_matrix(u, v):
    return np.array([
        [1, 0, u],
        [0, 1, v],
        [0, 0, 1]])


def rotation_matrix(angle, pivot):
    cos_a = float(f'{cos(angle):.6f}')
    sin_a = float(f'{sin(angle):.6f}')
    u, v = pivot
    return np.array([
        [(cos_a), (sin_a * -1), (u * (1 - cos_a) + v * sin_a)],
        [(sin_a), (cos_a), (v * (1 - cos_a) - u * sin_a)],
        [0, 0, 1]])


def universal_rotation_matrix(context, angle, pivot):
    """
    Rotate on non square active image
    """
    acitve_img = get_non_square_acitve_img(context)
    rotation = rotation_matrix(angle, pivot)
    if acitve_img:
        width, height = acitve_img.size
        if width > height:
            scale_1 = scale_matrix((width / height, 1), pivot)
            scale_2 = scale_matrix((1 / (width / height), 1), pivot)
        else:
            scale_1 = scale_matrix((1 / (height / width), 1), pivot)
            scale_2 = scale_matrix((height / width, 1), pivot)
        rotate_scale = np.dot(rotation, scale_1)
        convolution = np.dot(scale_2, rotate_scale)
        return convolution
    return rotation


def scale_matrix(factor, pivot):
    pivot_u, pivot_v = pivot
    factor_u, factor_v = factor
    return np.array([
        [factor_u, 0, pivot_u * (1 - factor_u)],
        [0, factor_v, pivot_v * (1 - factor_v)],
        [0, 0, 1]])


def get_non_square_acitve_img(context):
    for area in context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            acitve_img = area.spaces.active.image
    if acitve_img:
        width, height = acitve_img.size
        if height != 0:
            if width / height != 1:
                return acitve_img


def get_objects_seams(context):
    store_initial_seams = defaultdict(list)
    objects_seams = defaultdict(set)
    store_initial_selection = defaultdict(set)
    store_face_selection = defaultdict(set)
    store_verts_selection = defaultdict(set)
    store_edges_selection = defaultdict(set)

    scene = context.scene
    current_uv_select_mode = scene.tool_settings.uv_select_mode
    scene.tool_settings.uv_select_mode = 'VERTEX'

    for ob in context.objects_in_mode_unique_data:
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        uv = bm.loops.layers.uv.verify()
        for e in bm.edges:
            if e.seam:
                store_initial_seams[ob].append(e.index)
                e.seam = False
            if e.select:
                store_edges_selection[ob].add(e.index)
        for v in bm.verts:
            if v.select:
                store_verts_selection[ob].add(v.index)
        for f in bm.faces:
            if f.select:
                store_face_selection[ob].add(f.index)
            for l in f.loops:
                if l[uv].select:
                    store_initial_selection[ob].add(l.index)
                l[uv].select = True
            f.select = True

    bpy.ops.uv.seams_from_islands(mark_seams=True)

    for ob in context.objects_in_mode_unique_data:
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        for e in bm.edges:
            if e.seam:
                objects_seams[ob].add(e.index)
                e.seam = False

    for ob in context.objects_in_mode_unique_data:
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        uv = bm.loops.layers.uv.verify()
        bm.edges.ensure_lookup_table()
        for edge_idx in store_initial_seams[ob]:
            bm.edges[edge_idx].seam = True

        for f in bm.faces:
            for l in f.loops:
                if l.index in store_initial_selection[ob]:
                    continue
                l[uv].select = False

        for f in bm.faces:
            if f.index in store_face_selection[ob]:
                continue
            f.select = False
        for v in bm.verts:
            if v.index in store_verts_selection[ob]:
                v.select = True
        for e in bm.edges:
            if e.index in store_edges_selection[ob]:
                e.select = True

    scene.tool_settings.uv_select_mode = current_uv_select_mode

    return objects_seams


def get_islands(uv, bm, seams, has_selected_faces=False, islands_with_hidden_faces=True):
    if has_selected_faces:
        faces = {f for f in bm.faces for l in f.loops if l[uv].select}
    else:
        faces = set(bm.faces)
    while len(faces) != 0:
        init_face = faces.pop()
        island = {init_face}
        stack = [init_face]
        while len(stack) != 0:
            face = stack.pop()
            for e in face.edges:
                if e.index not in seams:
                    for f in e.link_faces:
                        if f != face and f not in island:
                            stack.append(f)
                            island.add(f)
        for f in island:
            faces.discard(f)

        if islands_with_hidden_faces is False:
            island_has_a_hidden_faces = False
            for face in island:
                if face.select is False:
                    island_has_a_hidden_faces = True
                    # print(">>>>>")
                    # print("has_a_hidden_faces")
                    break
            if island_has_a_hidden_faces:
                continue
        yield island


def collect_island_params(uv, faces):
    number_faces = len(faces)
    number_loops = 0
    vert_on_seams = 0

    for f in faces:
        for vert in f.verts:
            vert_uv = {l[uv].uv[:] for l in vert.link_loops}
            if len(vert_uv) != 1:
                vert_on_seams += 1
            for l in f.loops:
                number_loops += 1
    return number_faces, vert_on_seams, number_loops
