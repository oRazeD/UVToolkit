import bpy


class OpenAddonSettings(bpy.types.Operator):
    bl_idname = "uv.toolkit_open_addon_settings"
    bl_label = "Settings"
    bl_description = "Open addon settings in new window"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        bpy.data.window_managers["WinMan"].addon_search = "UV Toolkit"
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers["WinMan"].addon_support = {
            'OFFICIAL', 'COMMUNITY'
        }
        return {'FINISHED'}
