import numpy as np
from collections import defaultdict

import bmesh
from bpy.types import Operator

from ..utils.uv_utils import (
    get_uv_edges,
    get_objects_seams,
    get_islands,
    calc_slope,
    get_bbox,
    calc_bbox_center,
    min_angle_to_axis,
    universal_rotation_matrix,
)


class OrientIslands(Operator):
    bl_idname = "uv.toolkit_orient_islands"
    bl_label = "Orient Islands"
    bl_description = "Rotate Islands to the most nearest axis"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def get_uv_edges_coordinates(self, uv, island):
        island_loops = {l for f in island for l in f.loops}
        border_verts = []
        border_loops = set()

        for l in island_loops:
            if l.vert.is_boundary:
                border_verts.append(l.vert)
            else:
                vert_uv = {l[uv].uv[:] for l in l.vert.link_loops}
                if len(vert_uv) != 1:
                    border_verts.append(l.vert)

        for v in border_verts:
            for l in v.link_loops:
                if l in island_loops:
                    border_loops.add(l)

        uv_edges_co = get_uv_edges(uv, border_loops)
        return uv_edges_co

    def collect_uv_edges_angles(self, context, uv_edges_co):
        uv_edges_angles = []
        for uv_edge_co in uv_edges_co:
            point_a, point_b = uv_edge_co
            slope = calc_slope(context, point_a, point_b)
            uv_edges_angles.append(slope)
        return uv_edges_angles

    def get_rotation_angle(self, uv_edges_angles):
        corner_counter = defaultdict(int)
        for angle in uv_edges_angles:
            corner_counter[angle] += 1

        current_angle, number_angles = corner_counter.popitem()

        for angle in corner_counter:
            if number_angles < corner_counter[angle]:
                current_angle = angle
                number_angles = corner_counter[angle]
        return current_angle

    def rotate_island(self, context, uv, island, rotation_angle):
        bbox = get_bbox(uv, island)
        pivot = calc_bbox_center(bbox)

        angle = min_angle_to_axis(rotation_angle)
        rotation = universal_rotation_matrix(context, angle, pivot)

        for f in island:
            for l in f.loops:
                u, v = l[uv].uv
                l[uv].uv = rotation.dot(np.array([u, v, 1]))[:2]

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                uv_edges_co = self.get_uv_edges_coordinates(uv, island)
                uv_edges_angles = self.collect_uv_edges_angles(context, uv_edges_co)
                rotation_angle = self.get_rotation_angle(uv_edges_angles)
                self.rotate_island(context, uv, island, rotation_angle)
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
