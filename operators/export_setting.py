import os

from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper


class ExportSettings(Operator, ExportHelper):
    bl_idname = "uv.toolkit_export_settings"
    bl_label = "Export Settings"
    bl_description = "Export addon settings"

    filename_ext = ".ini"

    filter_glob: StringProperty(
        default="*.ini",
        options={'HIDDEN'},
        maxlen=2000,
    )

    def get_addon_properties(self):
        addon_prefs_path = os.path.split(__file__)[0][:-9] + "addon_preferences.py"
        with open(addon_prefs_path, 'r', encoding='utf-8') as file:
            for line in file:
                if ": EnumProperty" in line or ": StringProperty" in line:
                    yield line.split(" ")[4][:-1]

    def execute(self, context):
        preferences = context.preferences
        with open(self.filepath, 'w', encoding='utf-8') as file:
            for addon_property in self.get_addon_properties():
                value = getattr(preferences.addons[__name__.partition('.')[0]].preferences, addon_property)
                file.write(f"{addon_property}='{value}'" + '\n')
        return {'FINISHED'}
