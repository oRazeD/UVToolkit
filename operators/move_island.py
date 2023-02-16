import bpy
from bpy.props import BoolProperty
from bpy.types import Operator


class MoveIsland(Operator):
    bl_idname = "uv.toolkit_move_island"
    bl_label = "Move Island"
    bl_description = "Selects the island under the cursor and activates the move tool"
    bl_options = {'REGISTER', 'UNDO'}

    select_island: BoolProperty(
        name="Select Island",
        default=True,
        options={'HIDDEN'}
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        tool_settings = context.tool_settings

        if scene.tool_settings.use_uv_select_sync:
            current_mode = tool_settings.mesh_select_mode[:]
            tool_settings.mesh_select_mode = (False, False, True)
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT')
            bpy.ops.transform.translate('INVOKE_DEFAULT')
            if not self.select_island:
                bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT', deselect=True)
            tool_settings.mesh_select_mode = current_mode
        else:
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT')
            bpy.ops.transform.translate('INVOKE_DEFAULT')
            if not self.select_island:
                bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT', deselect=True)
        return {'FINISHED'}
