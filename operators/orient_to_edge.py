import numpy as np

import bmesh
from bpy.types import Operator

from ..utils.uv_utils import (
    calc_slope,
    min_angle_to_axis,
    get_bbox,
    calc_bbox_center,
    universal_rotation_matrix,
    get_objects_seams,
    get_islands,
)


class OrientToEdge(Operator):
    bl_idname = "uv.toolkit_orient_to_edge"
    bl_label = "Orient to Edge"
    bl_description = "Rotates an island at the selected points to the nearest axis"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

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
                selected_uv_verts_co = {l[uv].uv.copy().freeze()
                                        for f in island
                                        for l in f.loops
                                        if l[uv].select}
                if not len(selected_uv_verts_co) >= 2:
                    continue

                selected_uv_verts_co = list(selected_uv_verts_co)

                point_a = selected_uv_verts_co[0]
                point_b = selected_uv_verts_co[-1]

                bbox = get_bbox(uv, island)
                bbox_center = calc_bbox_center(bbox)

                slope = calc_slope(context, point_a, point_b)
                angle = min_angle_to_axis(slope)

                rotation = universal_rotation_matrix(context, angle, bbox_center)
                for f in island:
                    for l in f.loops:
                        u, v = l[uv].uv
                        l[uv].uv = rotation.dot(np.array([u, v, 1]))[:2]
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
