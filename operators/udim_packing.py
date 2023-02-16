import bpy
from bpy.props import BoolProperty, FloatProperty
from bpy.types import Operator

from ..utils.uv_utils import (
    get_udim_co,
)


class UdimPacking(Operator):
    bl_idname = "uv.toolkit_udim_packing"
    bl_label = "Pack UVs"
    bl_description = "Pack islands based on 2d cursor position"
    bl_options = {'REGISTER', 'UNDO'}

    rotate: BoolProperty(
        name="Rotate",
        default=True,
    )
    margin: FloatProperty(
        name="Margin",
        min=0,
    )
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        space_data = context.space_data
        cursor_position = tuple(space_data.cursor_location)
        udim_co = get_udim_co(cursor_position)
        u, v = udim_co[1][0] - 1, udim_co[1][1] - 1
        bpy.ops.uv.pack_islands(rotate=self.rotate, margin=self.margin)
        bpy.ops.transform.translate(value=(u, v, 0))
        return {'FINISHED'}
