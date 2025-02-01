import bpy
from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty,
    EnumProperty
)

from ..utils.uv_utils import (
    get_udim_co,
)


class UdimPacking(Operator):
    bl_idname = "uv.toolkit_udim_packing"
    bl_label = "Pack UVs"
    bl_description = "Pack islands based on 2d cursor position"
    bl_options = {'REGISTER', 'UNDO'}

    shape_method: EnumProperty(
        name="Shape Method",
        items=[("CONCAVE", "Concave", "Uses exact geometry"),
               ("CONVEX", "Convex", "Uses convex hull"),
               ("AABB", "AABB", "Uses bounding boxes")
               ],
        default="CONCAVE"
    )
    use_seed: BoolProperty(
        name="Use Random Seed",
        description="Randomize the UV layout before packing to find better solutions",
        default=False,
    )
    seed: IntProperty(
        name="Random Seed",
        default=0
    )
    scale: BoolProperty(
        name="Scale",
        default=True,
    )
    rotate: BoolProperty(
        name="Rotate",
        default=True,
    )
    margin_method: EnumProperty(
        name="Margin Method",
        items=[("SCALED", "Scaled", "Use scale of existing UVs to multiply margin"),
               ("ADD", "Add", "Add the margin, ignoring any UV scale"),
               ("FRACTION", "Fraction", "Specify a precise fraction of final UV output")
               ],
        default="SCALED"
    )
    margin: FloatProperty(
        name="Margin",
        precision=3,
        default=0.001,
        step=0.3,
        min=0,
    )
    pin: BoolProperty(
        name="Pin",
        description="Lock Pinned Islands, Constrain islands containing any pinned UV's",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        space_data = context.space_data

        if self.use_seed and not scene.tool_settings.use_uv_select_sync:
            bpy.ops.uv.toolkit_randomize_islands(
                seed=self.seed,
                translate_limit=10,
                angle_limit=360 if self.rotate else 0
                )
        elif self.use_seed:  # FIXME: Not sure if this is the way to go but it's consistent with Randomize Islands for now
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        cursor_position = tuple(space_data.cursor_location)
        udim_co = get_udim_co(cursor_position)
        u, v = udim_co[1][0] - 1, udim_co[1][1] - 1
        bpy.ops.uv.pack_islands(
            rotate=self.rotate,
            scale=self.scale,
            margin_method=self.margin_method,
            margin=self.margin,
            pin=self.pin,
            shape_method=self.shape_method
            )
        bpy.ops.transform.translate(value=(u, v, 0))
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        row = layout.row()
        row.prop(self, "shape_method", expand=True)
        layout.prop(self, "use_seed")
        row = layout.row()
        row.enabled = self.use_seed
        row.prop(self, "seed")
        layout.prop(self, "scale")
        layout.prop(self, "rotate")
        row = layout.row()
        row.prop(self, "margin_method", expand=True)
        layout.prop(self, "margin")
        layout.prop(self, "pin")
