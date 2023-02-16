import bpy


class CenterCursorFrameAll(bpy.types.Operator):
    bl_idname = "uv.toolkit_center_cursor_and_frame_all"
    bl_label = "Center Cursor and Frame All"
    bl_description = " "
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        space_data = context.space_data
        space_data.cursor_location = 0, 0
        bpy.ops.image.view_all()
        return {'FINISHED'}
