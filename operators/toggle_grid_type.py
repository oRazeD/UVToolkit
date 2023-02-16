import bpy
from bpy.types import Operator


class ToggleGridType(Operator):
    bl_idname = "uv.toolkit_toggle_grid_type"
    bl_label = "Toggle Grid Type"
    bl_description = "Switches the type of standard texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for image in bpy.data.images:
            if image.name.startswith("uv_checker_map"):
                if image.generated_type == "UV_GRID":
                    image.generated_type = "COLOR_GRID"
                else:
                    image.generated_type = "UV_GRID"
        return{'FINISHED'}
