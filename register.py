import os

import bpy.utils.previews

from .keymap import keymap_items


addon_keymaps = []


def keymap_register(wm):
    for items in keymap_items:
        (area_name, space,
            item_id, button, value,
            shift_state, ctrl_state, alt_state,
            pie_name) = items
        km = wm.keyconfigs.addon.keymaps.new(name=area_name, space_type=space)
        kmi = km.keymap_items.new(
            item_id, button, value,
            shift=shift_state, ctrl=ctrl_state, alt=alt_state
        )
        if pie_name:
            kmi.properties.name = pie_name
        addon_keymaps.append((km, kmi))


icons_collections = {}


def load_icons(icons_dir, collection_name):
    icons_coll = bpy.utils.previews.new()
    for icon in os.listdir(path=icons_dir):
        icon_name = os.path.splitext(icon)[0]
        icons_coll.load(icon_name, os.path.join(icons_dir, icon), 'IMAGE')
        icons_collections[collection_name] = icons_coll


def icons_register():
    icons_color_dir = os.path.join(os.path.dirname(__file__), "icons/light")
    load_icons(icons_color_dir, "light")
    icons_black_dir = os.path.join(os.path.dirname(__file__), "icons/dark")
    load_icons(icons_black_dir, "dark")


def icons_unregister():
    for icons_coll in icons_collections.values():
        bpy.utils.previews.remove(icons_coll)
    icons_collections.clear()
