from math import radians

import bpy

from bpy.props import BoolProperty
from bpy.types import Operator


class RotateIslands(Operator):
    bl_idname = "uv.toolkit_rotate_islands"
    bl_label = "Rotate islands"
    bl_description = "Rotate the selected islands"
    bl_options = {'REGISTER', 'UNDO'}

    cw: BoolProperty(
        default=True,
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        angle = radians(scene.uv_toolkit.island_rotation_angle)
        if self.cw is False:
            angle = angle * -1

        if scene.uv_toolkit.island_rotation_mode == "LOCAL":
            space_data = context.space_data
            current_pivot_point = space_data.pivot_point
            space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
            bpy.ops.transform.rotate(value=angle, use_proportional_edit=False)
            space_data.pivot_point = current_pivot_point

        if scene.uv_toolkit.island_rotation_mode == "GLOBAL":
            bpy.ops.transform.rotate(value=angle, use_proportional_edit=False)
        return {'FINISHED'}
