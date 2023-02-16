import bpy
import bmesh
from bpy.types import Operator

from ..utils.uv_utils import (
    get_objects_seams,
    get_islands,
)


class SelectFlippedIslands(Operator):
    bl_idname = "uv.toolkit_select_flipped_islands"
    bl_label = "Select Flipped Islands"
    bl_description = "Select Flipped Islands"
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def is_flipped_island(self, uv, island):
        for f in island:
            sum_c = 0
            for i in range(3):
                a = f.loops[i][uv].uv
                b = f.loops[(i + 1) % 3][uv].uv
                c = b.cross(a)
                sum_c += c
            if sum_c > 0:
                return True

    def execute(self, context):
        scene = context.scene

        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        current_uv_select_mode = scene.tool_settings.uv_select_mode

        bpy.ops.uv.select_all(action='DESELECT')

        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams):
                if self.is_flipped_island(uv, island):
                    for f in island:
                        for l in f.loops:
                            l[uv].select = True

        scene.tool_settings.uv_select_mode = 'VERTEX'
        scene.tool_settings.uv_select_mode = current_uv_select_mode
        return {'FINISHED'}
