import numpy as np
from math import sqrt

import bmesh
from bpy.types import Operator
from bpy.props import BoolProperty

from ..utils.uv_utils import (
    get_objects_seams,
    get_islands,
    calc_slope,
    min_angle_to_axis,
    universal_rotation_matrix,
)


TOP = 0
BOTTOM = 1
RIGHT = 2
LEFT = 3


class Straighten(Operator):
    bl_idname = "uv.toolkit_straighten"
    bl_label = "Straighten UVs"
    bl_description = "Align the selected faces"
    bl_options = {'UNDO', 'REGISTER'}

    reshape_all: BoolProperty(
        name="Reshape All",
        default=False
    )
    gridify: BoolProperty(
        name="Gridify",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def straighten(self, bm, uv, seams, context):

        def get_parallel_edge(edge, face):
            edge_vert_0, edge_vert_1 = edge.verts

            for e in face.edges:
                if edge_vert_0 not in e.verts and edge_vert_1 not in e.verts:
                    return e

        def calc_average_edges_length(faces, seams):
            # Calculate factor
            if len(faces) < 4:
                max_faces = len(faces)
            else:
                max_faces = 4

            sum_edges_length = 0
            sum_uv_edges_length = 0
            number_of_edges = 0
            for idx, f in enumerate(faces, 1):
                for l in f.loops:
                    current_loop = l
                    edge = l.edge
                    for next_loop in edge.other_vert(l.vert).link_loops:
                        if next_loop in f.loops:
                            break

                    u1, v1 = current_loop[uv].uv
                    u2, v2 = next_loop[uv].uv
                    uv_edge_length = sqrt((u1 - u2) * (u1 - u2) + (v1 - v2) * (v1 - v2))

                    sum_edges_length += edge.calc_length()
                    sum_uv_edges_length += uv_edge_length
                    number_of_edges += 1

                if idx == max_faces:
                    break

            edges = {e for f in faces for e in f.edges}
            edges_length = {}

            if self.gridify:
                edge_length = sum_uv_edges_length / number_of_edges

                for e in edges:
                    edges_length[e] = edge_length
            else:
                while edges:
                    init_edge = edges.pop()
                    # print(init_edge.index)
                    visited_faces = set()
                    edges_ring = [init_edge]
                    stack = [init_edge]

                    while stack:
                        edge = stack.pop()
                        for f in edge.link_faces:
                            if f in faces and f not in visited_faces:
                                next_edge = get_parallel_edge(edge, f)
                                stack.append(next_edge)
                                visited_faces.add(f)
                                edges_ring.append(next_edge)

                    for e in edges_ring:
                        edges.discard(e)
                    # print("------")
                    sum_edges_ring_length = 0
                    for number_of_edges, e in enumerate(edges_ring, 1):
                        sum_edges_ring_length += e.calc_length()
                        # print(e.index, e.calc_length())
                    avg_edges_ring_length = sum_edges_ring_length / number_of_edges
                    # print("number of edges", number_of_edges)
                    # print("sum edges - ", sum_edges_ring_length)
                    # print("avg length - ", avg_edges_ring_length)
                    if sum_edges_length > sum_uv_edges_length:
                        factor = sum_edges_length / sum_uv_edges_length
                        avg_edge_length = avg_edges_ring_length / factor
                        # print(1)
                    else:
                        factor = sum_uv_edges_length / sum_edges_length
                        avg_edge_length = avg_edges_ring_length * factor
                        # print(2)

                    for e in edges_ring:
                        edges_length[e] = avg_edge_length
            return edges_length

        def get_uv_vert(loop):
            uv_co = loop[uv].uv
            return [l for l in loop.vert.link_loops if l[uv].uv == uv_co]

        def align_initial_face(init_face, uv_coords, edges_length, edges_direction):
            l0 = init_face.loops[0]
            l1 = init_face.loops[1]
            l2 = init_face.loops[2]
            l3 = init_face.loops[3]

            epsilon = 0.00001
            slope = calc_slope(context, l0[uv].uv, l1[uv].uv)

            angle = min_angle_to_axis(slope)
            pivot = l0[uv].uv.to_tuple(6)
            rotation = universal_rotation_matrix(context, angle, pivot)

            for l in init_face.loops:
                uv_vert = get_uv_vert(l)
                for l in uv_vert:
                    u, v = l[uv].uv
                    uv_coords[l] = rotation.dot(np.array([u, v, 1]))[:2]

            l0_U, l0_V = uv_coords[l0]
            l1_U, l1_V = uv_coords[l1]
            l2_U, l2_V = uv_coords[l2]
            l3_U, l3_V = uv_coords[l3]

            uv_vert_1 = get_uv_vert(l1)
            uv_vert_2 = get_uv_vert(l2)
            uv_vert_3 = get_uv_vert(l3)
            # print("++++++++++")
            if abs(l0_V - l1_V) < epsilon:
                # print("AXIS U")
                if l0_V > l3_V:
                    edges_direction[l0.edge] = TOP
                    edges_direction[l2.edge] = BOTTOM
                    # print("l0_V > l3_V")
                    if l0_U > l1_U:
                        # print("l0_U > l1_U")
                        edges_direction[l1.edge] = LEFT
                        edges_direction[l3.edge] = RIGHT

                        edge_length = edges_length[l0.edge]
                        for l in uv_vert_1:
                            u, v = uv_coords[l]
                            uv_coords[l] = l0_U - edge_length, v
                        l1_U, l1_V = uv_coords[l1]

                        edge_length = edges_length[l1.edge]
                        for l in uv_vert_2:
                            u, v = uv_coords[l]
                            uv_coords[l] = l1_U, l1_V - edge_length
                        l2_U, l2_V = uv_coords[l2]

                    else:
                        # print("l0_U < l1_U")
                        edges_direction[l1.edge] = RIGHT
                        edges_direction[l3.edge] = LEFT

                        edge_length = edges_length[l0.edge]
                        for l in uv_vert_1:
                            u, v = uv_coords[l]
                            uv_coords[l] = l0_U + edge_length, v
                        l1_U, l1_V = uv_coords[l1]

                        edge_length = edges_length[l1.edge]
                        for l in uv_vert_2:
                            u, v = uv_coords[l]
                            uv_coords[l] = l1_U, l1_V - edge_length
                        l2_U, l2_V = uv_coords[l2]

                else:
                    # print("l0_V < l3_V")
                    edges_direction[l0.edge] = BOTTOM
                    edges_direction[l2.edge] = TOP
                    if l0_U > l1_U:
                        # print("l0_U > l1_U")
                        edges_direction[l1.edge] = LEFT
                        edges_direction[l3.edge] = RIGHT

                        edge_length = edges_length[l0.edge]
                        for l in uv_vert_1:
                            u, v = uv_coords[l]
                            uv_coords[l] = l0_U - edge_length, v
                        l1_U, l1_V = uv_coords[l1]

                        edge_length = edges_length[l1.edge]
                        for l in uv_vert_2:
                            u, v = uv_coords[l]
                            uv_coords[l] = l1_U, l1_V + edge_length
                        l2_U, l2_V = uv_coords[l2]

                    else:
                        # print("l0_U < l1_U")
                        edges_direction[l1.edge] = RIGHT
                        edges_direction[l3.edge] = LEFT

                        edge_length = edges_length[l0.edge]
                        for l in uv_vert_1:
                            u, v = uv_coords[l]
                            uv_coords[l] = l0_U + edge_length, v
                        l1_U, l1_V = uv_coords[l1]

                        edge_length = edges_length[l1.edge]
                        for l in uv_vert_2:
                            u, v = uv_coords[l]
                            uv_coords[l] = l1_U, l1_V + edge_length
                        l2_U, l2_V = uv_coords[l2]

                for l in uv_vert_3:
                    u, v = uv_coords[l]
                    uv_coords[l] = l0_U, l2_V

            if abs(l0_U - l1_U) < epsilon:
                # print("AXIS V")
                if l0_V > l1_V:
                    # print("l0_V > l1_V")
                    edges_direction[l1.edge] = BOTTOM
                    edges_direction[l3.edge] = TOP

                    if l0_U > l3_U:
                        # print("l0_U > l3_U")
                        edges_direction[l0.edge] = RIGHT
                        edges_direction[l2.edge] = LEFT

                        edge_length = edges_length[l0.edge]
                        for l in uv_vert_1:
                            u, v = uv_coords[l]
                            uv_coords[l] = u, l0_V - edge_length
                        l1_U, l1_V = uv_coords[l1]

                        edge_length = edges_length[l1.edge]
                        for l in uv_vert_2:
                            u, v = uv_coords[l]
                            uv_coords[l] = l1_U - edge_length, l1_V
                        l2_U, l2_V = uv_coords[l2]
                    else:
                        # print("l0_U < l3_U")
                        edges_direction[l0.edge] = LEFT
                        edges_direction[l2.edge] = RIGHT

                        edge_length = edges_length[l0.edge]
                        for l in uv_vert_1:
                            u, v = uv_coords[l]
                            uv_coords[l] = u, l0_V - edge_length
                        l1_U, l1_V = uv_coords[l1]

                        edge_length = edges_length[l1.edge]
                        for l in uv_vert_2:
                            u, v = uv_coords[l]
                            uv_coords[l] = l1_U + edge_length, l1_V
                        l2_U, l2_V = uv_coords[l2]
                else:
                    # print("l0_V < l1_V")
                    edges_direction[l1.edge] = TOP
                    edges_direction[l3.edge] = BOTTOM
                    if l0_U > l3_U:
                        # print("l0_U > l3_U")
                        edges_direction[l0.edge] = RIGHT
                        edges_direction[l2.edge] = LEFT

                        edge_length = edges_length[l0.edge]
                        for l in uv_vert_1:
                            u, v = uv_coords[l]
                            uv_coords[l] = u, l0_V + edge_length
                        l1_U, l1_V = uv_coords[l1]

                        edge_length = edges_length[l1.edge]
                        for l in uv_vert_2:
                            u, v = uv_coords[l]
                            uv_coords[l] = l1_U - edge_length, l1_V
                        l2_U, l2_V = uv_coords[l2]
                    else:
                        # print("l0_U < l3_U")
                        edges_direction[l0.edge] = LEFT
                        edges_direction[l2.edge] = RIGHT

                        edge_length = edges_length[l0.edge]
                        for l in uv_vert_1:
                            u, v = uv_coords[l]
                            uv_coords[l] = u, l0_V + edge_length
                        l1_U, l1_V = uv_coords[l1]

                        edge_length = edges_length[l1.edge]
                        for l in uv_vert_2:
                            u, v = uv_coords[l]
                            uv_coords[l] = l1_U + edge_length, l1_V
                        l2_U, l2_V = uv_coords[l2]

                for l in uv_vert_3:
                    u, v = uv_coords[l]
                    uv_coords[l] = l2_U, l0_V
            # space_data = context.space_data
            # space_data.cursor_location = l0_U, l0_V

            # def print_direction(direction):
            #     if direction == 0:
            #         return "TOP"
            #     if direction == 1:
            #         return "BOTTOM"
            #     if direction == 2:
            #         return "RIGHT"
            #     if direction == 3:
            #         return "LEFT"

            # edge_0_direction = edges_direction[l0.edge]
            # print(f"EDGE_0 - {print_direction(edge_0_direction)}")
            # edge_1_direction = edges_direction[l1.edge]
            # print(f"EDGE_1 - {print_direction(edge_1_direction)}")
            # edge_2_direction = edges_direction[l2.edge]
            # print(f"EDGE_2 - {print_direction(edge_2_direction)}")
            # edge_3_direction = edges_direction[l3.edge]
            # print(f"EDGE_3 - {print_direction(edge_3_direction)}")

        def align_faces(init_face, faces, edges_direction, uv_coords):
            def get_other_edges(init_edge, face,
                                vert_from_init_edge_0, vert_from_init_edge_1):
                other_edges = {}

                for init_vert in (vert_from_init_edge_0, vert_from_init_edge_1):
                    for e in face.edges:
                        if e == init_edge:
                            continue
                        if init_vert in e.verts:
                            other_edges[init_vert] = e
                        if vert_from_init_edge_0 not in e.verts and vert_from_init_edge_1 not in e.verts:
                            last_edge = e
                return [other_edges, last_edge]

            def face_loop_from_vert(face, vert):
                for l in face.loops:
                    if l.vert == vert:
                        return l

            def edge_processing(init_edge, other_edges, face,
                                vert_from_init_edge_0, vert_from_init_edge_1):
                edge1 = other_edges[0][vert_from_init_edge_0]
                edge2 = other_edges[0][vert_from_init_edge_1]
                edge3 = other_edges[1]

                l0 = face_loop_from_vert(face, vert_from_init_edge_0)
                l1 = face_loop_from_vert(face, vert_from_init_edge_1)
                l2 = face_loop_from_vert(face, edge1.other_vert(vert_from_init_edge_0))
                l3 = face_loop_from_vert(face, edge2.other_vert(vert_from_init_edge_1))

                uv_vert_0 = get_uv_vert(l2)
                uv_vert_1 = get_uv_vert(l3)

                l0_U, l0_V = uv_coords[l0]
                l1_U, l1_V = uv_coords[l1]
                edge_length = edges_length[edge1]

                if edges_direction[init_edge] == TOP:
                    for l in uv_vert_0:
                        uv_coords[l] = l0_U, l0_V + edge_length

                    for l in uv_vert_1:
                        uv_coords[l] = l1_U, l1_V + edge_length
                    if l0_U > l1_U:
                        edges_direction[edge1] = RIGHT
                        edges_direction[edge2] = LEFT
                        edges_direction[edge3] = TOP
                    else:
                        edges_direction[edge1] = LEFT
                        edges_direction[edge2] = RIGHT
                        edges_direction[edge3] = TOP

                if edges_direction[init_edge] == RIGHT:
                    for l in uv_vert_0:
                        uv_coords[l] = l0_U + edge_length, l0_V

                    for l in uv_vert_1:
                        uv_coords[l] = l1_U + edge_length, l1_V
                    if l0_V > l1_V:
                        edges_direction[edge1] = TOP
                        edges_direction[edge2] = BOTTOM
                        edges_direction[edge3] = RIGHT
                    else:
                        edges_direction[edge1] = BOTTOM
                        edges_direction[edge2] = TOP
                        edges_direction[edge3] = RIGHT

                if edges_direction[init_edge] == BOTTOM:
                    for l in uv_vert_0:
                        uv_coords[l] = l0_U, l0_V - edge_length

                    for l in uv_vert_1:
                        uv_coords[l] = l1_U, l1_V - edge_length
                    if l0_U > l1_U:
                        edges_direction[edge1] = RIGHT
                        edges_direction[edge2] = LEFT
                        edges_direction[edge3] = BOTTOM
                    else:
                        edges_direction[edge1] = LEFT
                        edges_direction[edge2] = RIGHT
                        edges_direction[edge3] = BOTTOM

                if edges_direction[init_edge] == LEFT:
                    for l in uv_vert_0:
                        uv_coords[l] = l0_U - edge_length, l0_V

                    for l in uv_vert_1:
                        uv_coords[l] = l1_U - edge_length, l1_V
                    if l0_V > l1_V:
                        edges_direction[edge1] = TOP
                        edges_direction[edge2] = BOTTOM
                        edges_direction[edge3] = LEFT
                    else:
                        edges_direction[edge1] = BOTTOM
                        edges_direction[edge2] = TOP
                        edges_direction[edge3] = LEFT

            visited_faces = {init_face}
            stack = [e for e in init_face.edges if e.index not in seams]
            while stack:
                current_edge = stack.pop()
                for f in current_edge.link_faces:
                    if f not in visited_faces and f in faces:
                        vert_from_init_edge_0 = current_edge.verts[0]
                        vert_from_init_edge_1 = current_edge.verts[1]
                        other_edges = get_other_edges(current_edge, f,
                                                      vert_from_init_edge_0, vert_from_init_edge_1)
                        edge_processing(current_edge, other_edges, f,
                                        vert_from_init_edge_0, vert_from_init_edge_1)
                        visited_faces.add(f)
                        for e in f.edges:
                            if e == current_edge or e.index in seams:
                                continue
                            stack.append(e)

        def apply_uv(uv_coords):
            for l in uv_coords:
                l[uv].uv = uv_coords[l]

        for island in get_islands(uv, bm, seams, has_selected_faces=True):
            if self.properties.reshape_all:
                island_has_an_hidden_faces = False
                for f in island:
                    if f.select is False:
                        island_has_an_hidden_faces = True
                        break
                if island_has_an_hidden_faces:
                    continue
                faces = {f for f in island if len(f.verts) == 4}
            else:
                deselected_loops_uv = set()

                for f in island:
                    for l in f.loops:
                        if not l[uv].select:
                            deselected_loops_uv.add(f)

                faces = {f for f in island
                         if f not in deselected_loops_uv
                         and f.select
                         and len(f.verts) == 4}

            if faces:
                for init_face in faces:
                    break

                uv_coords = {}
                edges_direction = {}
                edges_length = calc_average_edges_length(faces, seams)

                align_initial_face(init_face, uv_coords, edges_length, edges_direction)

                try:
                    align_faces(init_face, faces, edges_direction, uv_coords)
                except KeyError:
                    pass
                apply_uv(uv_coords)

    def execute(self, context):
        if context.scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        objects_seams = get_objects_seams(context)

        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()
            seams = objects_seams[ob]

            self.straighten(bm, uv, seams, context)
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
