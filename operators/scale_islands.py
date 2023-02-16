import bpy
from bpy.types import Operator


class ScaleIslands(Operator):
    bl_idname = "uv.toolkit_scale_islands"
    bl_label = "Scale Islands"
    bl_description = "Scale the selected islands"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        space_data = context.space_data

        curent_pivot = space_data.pivot_point

        bpy.ops.uv.select_linked()

        if scene.uv_toolkit.island_scale_mode == "LOCAL":
            space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        else:
            space_data.pivot_point = 'CENTER'

        bpy.ops.transform.resize(value=(
            scene.uv_toolkit.island_scale_x,
            scene.uv_toolkit.island_scale_y, 1))
        space_data.pivot_point = curent_pivot
        return {'FINISHED'}
