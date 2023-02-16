import bmesh
from bpy.types import Operator


class ClearAllPins(Operator):
    bl_idname = "uv.toolkit_clear_all_pins"
    bl_label = "Clear All Pins"
    bl_description = " "
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for f in bm.faces:
                for l in f.loops:
                    l[uv].pin_uv = False
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
