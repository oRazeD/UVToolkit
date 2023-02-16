import bpy
import bmesh
from bpy.types import Operator

from ..utils.uv_utils import (
    get_objects_seams,
    get_islands,
    get_bbox,
    calc_bbox_center,
)


class StackIslands(Operator):
    bl_idname = "uv.toolkit_stack_islands"
    bl_label = "Stack Islands"
    bl_description = "Stacks the selected islands on top of each other"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        space_data = context.space_data
        initial_cursor_position = tuple(space_data.cursor_location)
        bpy.ops.uv.snap_cursor(target='SELECTED')
        median_point = tuple(space_data.cursor_location)
        space_data.cursor_location = initial_cursor_position

        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                bbox = get_bbox(uv, island)
                bbox_center = calc_bbox_center(bbox)
                bbox_center_u = bbox_center[0]
                bbox_center_v = bbox_center[1]
                median_point_u = median_point[0]
                median_point_v = median_point[1]

                offset_u = abs(bbox_center_u - median_point_u)
                offset_v = abs(bbox_center_v - median_point_v)

                for f in island:
                    for l in f.loops:
                        if bbox_center_u < median_point_u:
                            u = l[uv].uv[0] + offset_u
                        else:
                            u = l[uv].uv[0] - offset_u

                        if bbox_center_v < median_point_v:
                            v = l[uv].uv[1] + offset_v
                        else:
                            v = l[uv].uv[1] - offset_v
                        l[uv].uv = (u, v)
                        l[uv].select = True
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
