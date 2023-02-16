import bpy


class SplitFacesMove(bpy.types.Operator):
    bl_idname = "uv.toolkit_split_faces_move"
    bl_label = "Split Faces"
    bl_description = "Separates the selected faces and activates the move tool"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene

        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        bpy.ops.uv.select_split()
        bpy.ops.transform.translate('INVOKE_DEFAULT')
        return {'FINISHED'}
