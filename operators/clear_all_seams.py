from bpy.types import Operator
import bmesh
from ..utils.uv_utils import clear_all_seams


class ClearAllSeams(Operator):
    bl_idname = "uv.toolkit_clear_all_seams"
    bl_label = "Clear All Seams"
    bl_description = "Clear all seams of objects in edit mode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            clear_all_seams(bm)
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
