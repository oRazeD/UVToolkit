import bpy


class BorderSeam(bpy.types.Operator):
    bl_idname = "uv.toolkit_border_seam"
    bl_label = "Border Seam"
    bl_description = "Mark seams around the selection border"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        tool_settings = context.tool_settings
        current_select_mode = tool_settings.mesh_select_mode[:]
        bpy.ops.mesh.region_to_loop()
        bpy.ops.mesh.mark_seam(clear=False)
        tool_settings.mesh_select_mode = current_select_mode
        return {'FINISHED'}
