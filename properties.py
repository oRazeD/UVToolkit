from bpy.types import PropertyGroup
from bpy.props import (
    IntProperty,
    FloatProperty,
    EnumProperty,
    StringProperty,
)


class UvToolkitProperties(PropertyGroup):
    checker_map_width: IntProperty(
        name="Width",
        min=0
    )
    checker_map_height: IntProperty(
        name="Height",
        min=0
    )
    move_distance: FloatProperty(
        name="Distance",
        default=1.0,
        min=0,
        step=0.1,
    )

    island_rotation_angle: IntProperty(
        name="Angle",
        default=90,
        min=0,
    )

    island_rotation_mode: EnumProperty(
        name="Rotation Mode",
        description="Current rotation mode",
        items=[
            ("GLOBAL", "G", "Global rotation"),
            ("LOCAL", "L", "Local rotation"),
        ],
        default="LOCAL",
    )

    align_mode: EnumProperty(
        name="Mode",
        items=[
            ("VERTICES", "Vertices", ""),
            ("ISLANDS", "Islands", "")
        ],
    )

    island_scale_x: FloatProperty(
        name="X",
        default=1,
    )

    island_scale_y: FloatProperty(
        name="Y",
        default=1,
    )

    island_scale_mode: EnumProperty(
        name="Scale Mode",
        description="Current scale mode",
        items=[
            ("GLOBAL", "G", "Global scale"),
            ("LOCAL", "L", "Local scale"),
        ],
        default="GLOBAL",
    )

    uv_layer_name: StringProperty(
        name="",
    )
    uv_layer_index: IntProperty(
        name="",
        description="Channel",
        min=1,
        default=1,
    )
