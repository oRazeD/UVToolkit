import bpy


def get_addon_preferences():
    return bpy.context.preferences.addons[__package__].preferences
