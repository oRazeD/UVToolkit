from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

from ..functions import get_addon_preferences


class ImportSettings(Operator, ImportHelper):
    bl_idname = "uv.toolkit_import_settings"
    bl_label = "Import Settings"
    bl_description = "Import addon settings"

    filename_ext = ".ini"

    filter_glob: StringProperty(
        default="*.ini",
        options={'HIDDEN'},
        maxlen=2000,
    )

    def execute(self, context):
        with open(self.filepath, 'r', encoding='utf-8') as addon_settings:
            for item in addon_settings:
                idx = item.find('=')
                prop = item[:idx]
                value = item[idx + 2:-2]

                addon_prefs = get_addon_preferences()
                setattr(addon_prefs, prop, value)
        return {'FINISHED'}
