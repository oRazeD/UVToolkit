from math import sin, cos

import bmesh
from bpy.types import Operator
from bpy.props import BoolProperty

from ..utils.uv_utils import (
    calc_slope,
    calc_length_sorted_uv_edges,
    get_sorted_uv_edge_loops,
    find_nearest_axis,
    get_direction,
)

AXIS_U = 0
AXIS_V = 1
NEGATIVE = 0
POSITIVE = 1


class Distribute(Operator):
    bl_idname = "uv.toolkit_distribute"
    bl_label = "Distribute"
    bl_description = "Align the selected vertices evenly or keeping edges length"
    bl_options = {'REGISTER', 'UNDO'}

    preserve_edge_length: BoolProperty(
        name="Preserve length",
        default=False
    )

    align_to_nearest_axis: BoolProperty(
        name="Align",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def distribute(
            self, uv, first_uv_vert, end_uv_vert,
            first_uv_vert_co, end_uv_vert_co,
            u1, v1, u2, v2, slope, number_uv_edges,
            uv_edge_loop):

        if self.align_to_nearest_axis or slope == 0:
            axis = find_nearest_axis(slope,
                                     first_uv_vert_co.to_tuple(4),
                                     end_uv_vert_co.to_tuple(4))

            direction = get_direction(axis, first_uv_vert_co, end_uv_vert_co)

            if axis == AXIS_U:
                uv_edge_length = abs((u1 - u2)) / number_uv_edges
                avg_v = v1 + ((v2 - v1) / 2)
                first_uv_vert_co = (u1, avg_v)
            if axis == AXIS_V:
                uv_edge_length = abs((v1 - v2)) / number_uv_edges
                avg_u = u1 + ((u2 - u1) / 2)
                first_uv_vert_co = (avg_u, v1)

            for l in first_uv_vert:
                l[uv].uv = first_uv_vert_co
            # Apply uv coordinates.
            for idx in range(number_uv_edges):
                current_uv_vert = uv_edge_loop[idx]
                next_uv_vert = uv_edge_loop[idx + 1]

                u1 = current_uv_vert[0][uv].uv[0]
                v1 = current_uv_vert[0][uv].uv[1]

                if axis == AXIS_U:
                    if direction == POSITIVE:
                        new_co = (u1 + uv_edge_length, avg_v)
                    if direction == NEGATIVE:
                        new_co = (u1 - uv_edge_length, avg_v)
                if axis == AXIS_V:
                    if direction == POSITIVE:
                        new_co = (avg_u, v1 + uv_edge_length)
                    if direction == NEGATIVE:
                        new_co = (avg_u, v1 - uv_edge_length)

                for l in next_uv_vert:
                    l[uv].uv = new_co
        else:
            uv_edge_length = (
                (first_uv_vert_co - end_uv_vert_co).length / (number_uv_edges))

            if v1 < v2:
                start_uv_vert = 'BOTTOM'
            else:
                start_uv_vert = 'TOP'

            if u1 < u2:
                direction = POSITIVE
            else:
                direction = NEGATIVE

            u_projection = uv_edge_length * cos(slope)
            v_projection = uv_edge_length * sin(slope)

            # Apply uv coordinates.
            for idx in range(number_uv_edges):
                current_uv_vert = uv_edge_loop[idx]
                next_uv_vert = uv_edge_loop[idx + 1]

                u1 = current_uv_vert[0][uv].uv[0]
                v1 = current_uv_vert[0][uv].uv[1]

                if start_uv_vert == 'BOTTOM':
                    if direction == POSITIVE:
                        new_co = (u1 + u_projection, v1 + v_projection)
                    if direction == NEGATIVE:
                        new_co = (u1 - u_projection, v1 - v_projection)
                if start_uv_vert == 'TOP':
                    if direction == POSITIVE:
                        new_co = (u1 + u_projection, v1 + v_projection)
                    if direction == NEGATIVE:
                        new_co = (u1 - u_projection, v1 - v_projection)

                for l in next_uv_vert:
                    l[uv].uv = new_co

    def distribute_preserve_edges_length(
            self, uv, first_uv_vert, end_uv_vert,
            first_uv_vert_co, end_uv_vert_co,
            u1, v1, u2, v2, slope, number_uv_edges,
            uv_edge_loop):

        uv_edges_length = calc_length_sorted_uv_edges(uv, uv_edge_loop)
        all_edges_length = sum(uv_edges_length)

        if self.align_to_nearest_axis or slope == 0:
            axis = find_nearest_axis(slope,
                                     first_uv_vert_co.to_tuple(4),
                                     end_uv_vert_co.to_tuple(4))

            direction = get_direction(axis, first_uv_vert_co, end_uv_vert_co)

            if axis == AXIS_U:
                offset = (all_edges_length - abs(u2 - u1)) / 2
                avg_v = v1 + ((v2 - v1) / 2)
                if direction == POSITIVE:
                    first_uv_vert_co = (u1 - offset, avg_v)
                if direction == NEGATIVE:
                    first_uv_vert_co = (u1 + offset, avg_v)
            if axis == AXIS_V:
                offset = (all_edges_length - abs(v2 - v1)) / 2
                avg_u = u1 + ((u2 - u1) / 2)
                if direction == POSITIVE:
                    first_uv_vert_co = (avg_u, v1 - offset)
                if direction == NEGATIVE:
                    first_uv_vert_co = (avg_u, v1 + offset)

            for l in first_uv_vert:
                l[uv].uv = first_uv_vert_co
            # Apply uv coordinates.
            for idx in range(number_uv_edges):
                current_uv_vert = uv_edge_loop[idx]
                next_uv_vert = uv_edge_loop[idx + 1]
                edge_length = uv_edges_length[idx]

                u1 = current_uv_vert[0][uv].uv[0]
                v1 = current_uv_vert[0][uv].uv[1]

                if axis == AXIS_U:
                    if direction == POSITIVE:
                        new_co = (u1 + edge_length, v1)
                    if direction == NEGATIVE:
                        new_co = (u1 - edge_length, v1)
                if axis == AXIS_V:
                    if direction == POSITIVE:
                        new_co = (u1, v1 + edge_length)
                    if direction == NEGATIVE:
                        new_co = (u1, v1 - edge_length)

                for l in next_uv_vert:
                    l[uv].uv = new_co
        else:
            initial_length = (first_uv_vert_co - end_uv_vert_co).length
            offset = (all_edges_length - initial_length) / 2
            u_projection = offset * cos(slope)
            v_projection = offset * sin(slope)

            if v1 < v2:
                start_uv_vert = 'BOTTOM'
            else:
                start_uv_vert = 'TOP'

            if u1 < u2:
                direction = POSITIVE
            else:
                direction = NEGATIVE
            # Tweak start vert.
            if start_uv_vert == 'BOTTOM':
                if direction == POSITIVE:
                    new_co = (u1 - u_projection, v1 - v_projection)
                if direction == NEGATIVE:
                    new_co = (u1 + u_projection, v1 + v_projection)
            if start_uv_vert == 'TOP':
                if direction == POSITIVE:
                    new_co = (u1 - u_projection, v1 - v_projection)
                if direction == NEGATIVE:
                    new_co = (u1 + u_projection, v1 + v_projection)

            for l in first_uv_vert:
                l[uv].uv = new_co
            # Apply uv coordinates.
            for idx in range(number_uv_edges):
                current_uv_vert = uv_edge_loop[idx]
                next_uv_vert = uv_edge_loop[idx + 1]
                edge_length = uv_edges_length[idx]

                u1 = current_uv_vert[0][uv].uv[0]
                v1 = current_uv_vert[0][uv].uv[1]

                u_projection = edge_length * cos(slope)
                v_projection = edge_length * sin(slope)

                if start_uv_vert == 'BOTTOM':
                    if direction == POSITIVE:
                        new_co = (u1 + u_projection, v1 + v_projection)
                    if direction == NEGATIVE:
                        new_co = (u1 - u_projection, v1 - v_projection)
                if start_uv_vert == 'TOP':
                    if direction == POSITIVE:
                        new_co = (u1 + u_projection, v1 + v_projection)
                    if direction == NEGATIVE:
                        new_co = (u1 - u_projection, v1 - v_projection)

                for l in next_uv_vert:
                    l[uv].uv = new_co

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            loops = set()
            for f in bm.faces:
                if f.select:
                    for l in f.loops:
                        if l[uv].select:
                            loops.add(l)

            uv_edge_loops = get_sorted_uv_edge_loops(uv, loops)

            if not uv_edge_loops:
                continue

            for uv_edge_loop in uv_edge_loops:
                first_uv_vert = uv_edge_loop[0]
                if not first_uv_vert:
                    continue
                end_uv_vert = uv_edge_loop[-1]

                first_uv_vert_co = first_uv_vert[0][uv].uv
                end_uv_vert_co = end_uv_vert[0][uv].uv

                u1, v1 = first_uv_vert_co[0], first_uv_vert_co[1]
                u2, v2 = end_uv_vert_co[0], end_uv_vert_co[1]

                slope = calc_slope(context, first_uv_vert_co, end_uv_vert_co)
                number_uv_edges = len(uv_edge_loop) - 1

                if self.properties.preserve_edge_length:
                    self.distribute_preserve_edges_length(
                        uv, first_uv_vert, end_uv_vert,
                        first_uv_vert_co, end_uv_vert_co,
                        u1, v1, u2, v2, slope, number_uv_edges,
                        uv_edge_loop)
                else:
                    self.distribute(
                        uv, first_uv_vert, end_uv_vert,
                        first_uv_vert_co, end_uv_vert_co,
                        u1, v1, u2, v2, slope, number_uv_edges,
                        uv_edge_loop)
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
