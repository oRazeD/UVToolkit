import numpy as np

import bmesh
from bpy.types import Operator
from bpy.props import FloatProperty

from ..utils.uv_utils import (
    get_bbox,
    calc_bbox_center,
    get_bbox_size,
    translate_matrix,
    scale_matrix,
    get_objects_seams,
    get_islands,
)


class FitToBounds(Operator):
    bl_idname = "uv.toolkit_fit_to_bounds"
    bl_label = "Fit to Bounds"
    bl_description = "Scale the island to the size of the UV space"
    bl_options = {'REGISTER', 'UNDO'}

    margin: FloatProperty(
        name="Margin",
        default=0,
        step=0.1,
        precision=3,
        min=0,
        max=0.5,
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        margin = self.margin * 2
        pivot = 0.5, 0.5
        pivot_u, pivot_v = pivot

        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                bbox = get_bbox(uv, island)
                bbox_center_u, bbox_center_v = calc_bbox_center(bbox)
                bbox_width, bbox_height = get_bbox_size(bbox)

                if bbox_height > bbox_width:
                    factor_u = factor_v = (1 - margin) / bbox_height
                else:
                    factor_u = factor_v = (1 - margin) / bbox_width

                scale = scale_matrix((factor_u, factor_v), pivot)
                tranlate = translate_matrix(pivot_u - bbox_center_u, pivot_v - bbox_center_v)
                convolution = np.dot(scale, tranlate)

                for f in island:
                    for l in f.loops:
                        u, v = l[uv].uv
                        l[uv].uv = convolution.dot(np.array([u, v, 1]))[:2]
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
