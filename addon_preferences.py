import os

import bpy
import rna_keymap_ui
from bpy.types import AddonPreferences
from bpy.props import (
    EnumProperty,
    StringProperty,
)
from .keymap import keymap_items
from .utils.ui_utils import (
    view3d_items,
    uv_editor_items,
    get_icons_set,
)


def update_addon_category(self, _context):
    panels = (
        "UVTOOLKIT_PT_uv_sync",
        "UVTOOLKIT_PT_tools",
        "UVTOOLKIT_PT_pins",
        "UVTOOLKIT_PT_transform",
        "UVTOOLKIT_PT_unwrap",
        "UVTOOLKIT_PT_align",
        "UVTOOLKIT_PT_arrange",
        "UVTOOLKIT_PT_select",
        "UVTOOLKIT_PT_display",
        "UVTOOLKIT_PT_uv_maps",
        "UVTOOLKIT_PT_checker_map",
        "UVTOOLKIT_PT_quick_presets",
        "UVTOOLKIT_PT_cleanup",
        "UVTOOLKIT_PT_help",
    )
    sub_panels = (
        "UVTOOLKIT_PT_uv_sync_settings",
        "UVTOOLKIT_PT_checker_map_square",
        "UVTOOLKIT_PT_checker_map_horizontal_rectangle",
        "UVTOOLKIT_PT_checker_map_vertical_rectangle",
    )
    for panel_id in panels:
        panel_class = getattr(bpy.types, panel_id)
        bpy.utils.unregister_class(panel_class)
        panel_class.bl_category = self.category
        bpy.utils.register_class(panel_class)
    for sub_panel_id in sub_panels:
        sub_panel_class = getattr(bpy.types, sub_panel_id)
        bpy.utils.unregister_class(sub_panel_class)
        bpy.utils.register_class(sub_panel_class)


class UvToolkitPreferences(AddonPreferences):
    bl_idname = __package__
    # Pie 3d View
    pie_3dview_left: EnumProperty(
        name="Left",
        items=view3d_items,
        default="CLEAR_SEAM"
    )
    pie_3dview_right: EnumProperty(
        name="Right",
        items=view3d_items,
        default="MARK_SEAM"
    )
    pie_3dview_bottom: EnumProperty(
        name="Bottom",
        items=view3d_items,
        default="UV_MENU"
    )
    pie_3dview_top: EnumProperty(
        name="Top",
        items=view3d_items,
        default="uv.unwrap"
    )
    pie_3dview_top_left: EnumProperty(
        name="Top Left",
        items=view3d_items,
        default="uv.toolkit_clear_all_seams"
    )
    pie_3dview_top_right: EnumProperty(
        name="Top Right",
        items=view3d_items,
        default="uv.toolkit_border_seam"
    )
    pie_3dview_bottom_left: EnumProperty(
        name="Bottom Left",
        items=view3d_items,
        default="uv.toolkit_toggle_color_mode"
    )
    pie_3dview_bottom_right: EnumProperty(
        name="Bottom Right",
        items=view3d_items,
        default="uv.toolkit_mirror_seam"
    )
    pie_3dview_custom_op_left: StringProperty(default="")
    pie_3dview_custom_op_name_left: StringProperty(default="")

    pie_3dview_custom_op_right: StringProperty(default="")
    pie_3dview_custom_op_name_right: StringProperty(default="")

    pie_3dview_custom_op_top: StringProperty(default="")
    pie_3dview_custom_op_name_top: StringProperty(default="")

    pie_3dview_custom_op_bottom: StringProperty(default="")
    pie_3dview_custom_op_name_bottom: StringProperty(default="")

    pie_3dview_custom_op_top_left: StringProperty(default="")
    pie_3dview_custom_op_name_top_left: StringProperty(default="")

    pie_3dview_custom_op_top_right: StringProperty(default="")
    pie_3dview_custom_op_name_top_right: StringProperty(default="")

    pie_3dview_custom_op_bottom_left: StringProperty(default="")
    pie_3dview_custom_op_name_bottom_left: StringProperty(default="")

    pie_3dview_custom_op_bottom_right: StringProperty(default="")
    pie_3dview_custom_op_name_bottom_right: StringProperty(default="")
    # Pie UV Editor
    pie_uv_editor_left: EnumProperty(
        name="Left",
        items=uv_editor_items,
        default="uv.toolkit_split_faces_move"
    )
    pie_uv_editor_right: EnumProperty(
        name="Right",
        items=uv_editor_items,
        default="uv.toolkit_align_uv"
    )
    pie_uv_editor_bottom: EnumProperty(
        name="Bottom",
        items=uv_editor_items,
        default="uv.toolkit_invert_selection"
    )
    pie_uv_editor_top: EnumProperty(
        name="Top",
        items=uv_editor_items,
        default="uv.toolkit_unwrap_selected"
    )
    pie_uv_editor_top_left: EnumProperty(
        name="Top Left",
        items=uv_editor_items,
        default="uv.toolkit_distribute"
    )
    pie_uv_editor_top_right: EnumProperty(
        name="Top Right",
        items=uv_editor_items,
        default="uv.toolkit_straighten"
    )
    pie_uv_editor_bottom_left: EnumProperty(
        name="Bottom Left",
        items=uv_editor_items,
        default="uv.toolkit_unstack_islands"
    )
    pie_uv_editor_bottom_right: EnumProperty(
        name="Bottom Right",
        items=uv_editor_items,
        default="uv.toolkit_stack_islands"
    )
    pie_uv_editor_custom_op_left: StringProperty(default="")
    pie_uv_editor_custom_op_name_left: StringProperty(default="")

    pie_uv_editor_custom_op_right: StringProperty(default="")
    pie_uv_editor_custom_op_name_right: StringProperty(default="")

    pie_uv_editor_custom_op_top: StringProperty(default="")
    pie_uv_editor_custom_op_name_top: StringProperty(default="")

    pie_uv_editor_custom_op_bottom: StringProperty(default="")
    pie_uv_editor_custom_op_name_bottom: StringProperty(default="")

    pie_uv_editor_custom_op_top_left: StringProperty(default="")
    pie_uv_editor_custom_op_name_top_left: StringProperty(default="")

    pie_uv_editor_custom_op_top_right: StringProperty(default="")
    pie_uv_editor_custom_op_name_top_right: StringProperty(default="")

    pie_uv_editor_custom_op_bottom_left: StringProperty(default="")
    pie_uv_editor_custom_op_name_bottom_left: StringProperty(default="")

    pie_uv_editor_custom_op_bottom_right: StringProperty(default="")
    pie_uv_editor_custom_op_name_bottom_right: StringProperty(default="")

    chekcer_maps_path: StringProperty(
        name="",
        description="Path to Directory",
        default=os.path.join(os.path.split(__file__)[0], "checker_maps"),
        maxlen=2000,
        subtype='DIR_PATH'
    )
    icon_style: EnumProperty(
        items=[
            ("LIGHT", "Light", ""),
            ("DARK", "Dark", ""),
        ],
        default="LIGHT"
    )
    checker_map: EnumProperty(
        items=[
            ("BUILT-IN", "Built-in", ""),
            ("CUSTOM", "Custom", ""),
        ]
    )
    checker_type: EnumProperty(
        description="Choose image type",
        items=[
            ("UV_GRID", "Checker Grid", ""),
            ("COLOR_GRID", "Color Grid", ""),
        ]
    )
    assign_image_in_uv_editor: EnumProperty(
        items=[
            ("ENABLE", "Enable", ""),
            ("DISABLE", "Disable", "")
        ],
        default="DISABLE"
    )
    sync_selection: EnumProperty(
        name="Sync Selected Elements",
        items=[
            ("enable", "Enable", ""),
            ("disable", "Disable", "")
        ],
        default="enable"
    )
    sync_uv_selction_mode: EnumProperty(
        name="Sync Selection Mode",
        items=[
            ("enable", "Enable", ""),
            ("disable", "Disable", "")
        ],
        default="enable"
    )
    tab: EnumProperty(
        items=[
            ("GENERAL", "General", ""),
            ("KEYMAP", "Keymap", ""),
            ("PIE_MENU", "Pie Menu", ""),
            ("HELP", "Help/Links", ""),
        ],
        default="GENERAL"
    )
    pie_tab: EnumProperty(
        items=[
            ("PIE_3D_VIEW", "3D View", ""),
            ("PIE_UV_EDITOR", "UV Editor", ""),
        ],
    )
    category: StringProperty(
        description="Choose a name for the category of the panel",
        default="UV Toolkit",
        update=update_addon_category
    )

    def draw_keymap(self, context):
        def get_pie_menu_hotkey(km, kmi_name, kmi_value):
            for i, km_item in enumerate(km.keymap_items):
                if km.keymap_items.keys()[i] == kmi_name:
                    if km.keymap_items[i].properties.name == kmi_value:
                        return km_item

        def get_operator_hotkey(km, kmi_name):
            for i, km_item in enumerate(km.keymap_items):
                if km.keymap_items.keys()[i] == kmi_name:
                    return km_item

        wm = context.window_manager
        kc = wm.keyconfigs.user
        layout = self.layout
        box = layout.box()
        split = box.split()
        col = split.column()

        for km_item in keymap_items:
            km = kc.keymaps[km_item[0]]
            operator = km_item[2]
            if operator == 'wm.call_menu_pie':
                value = km_item[-1]
                kmi = get_pie_menu_hotkey(km, 'wm.call_menu_pie', value)
            else:
                kmi = get_operator_hotkey(km, operator)
            if kmi:
                col.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)

    def draw(self, context):
        icons_coll = get_icons_set(context)
        layout = self.layout
        row = layout.row()
        row.prop(self, "tab", expand=True)
        if self.tab == 'GENERAL':
            layout = layout.box()
            split = layout.split()
            # First column
            col = split.column()
            col.label(text="Panel Category:")
            col.separator()
            col.label(text="Always set checker image in the UV Editor:")
            col.separator()
            col.label(text="Icon set:")
            col.separator()
            col.label(text="Checker maps folder:")
            # Second column
            col = split.column()
            col.prop(self, "category", text="")
            col.separator()
            row = col.row()
            row.prop(self, "assign_image_in_uv_editor", expand=True)
            col.separator()
            row = col.row()
            row.prop(self, "icon_style", expand=True)
            col.separator()
            col.prop(self, "chekcer_maps_path")

            layout.separator()
            row = layout.row()
            row.operator("uv.toolkit_import_settings", icon_value=icons_coll["import_settings"].icon_id)
            row.operator("uv.toolkit_export_settings", icon_value=icons_coll["export_settings"].icon_id)

        if self.tab == 'PIE_MENU':
            layout = layout.box()
            row = layout.row()
            row.prop(self, "pie_tab", expand=True)
            if self.pie_tab == 'PIE_3D_VIEW':
                layout.prop(self, "pie_3dview_left")
                if self.pie_3dview_left == "CUSTOM_OP":
                    layout.prop(self, "pie_3dview_custom_op_left", text="   Operator")
                    layout.prop(self, "pie_3dview_custom_op_name_left", text="   Name")
                layout.prop(self, "pie_3dview_right")
                if self.pie_3dview_right == "CUSTOM_OP":
                    layout.prop(self, "pie_3dview_custom_op_right", text="   Operator")
                    layout.prop(self, "pie_3dview_custom_op_name_right", text="   Name")
                layout.prop(self, "pie_3dview_top")
                if self.pie_3dview_top == "CUSTOM_OP":
                    layout.prop(self, "pie_3dview_custom_op_top", text="   Operator")
                    layout.prop(self, "pie_3dview_custom_op_name_top", text="   Name")
                layout.prop(self, "pie_3dview_bottom")
                if self.pie_3dview_bottom == "CUSTOM_OP":
                    layout.prop(self, "pie_3dview_custom_op_bottom", text="   Operator")
                    layout.prop(self, "pie_3dview_custom_op_name_bottom", text="   Name")
                layout.prop(self, "pie_3dview_top_left")
                if self.pie_3dview_top_left == "CUSTOM_OP":
                    layout.prop(self, "pie_3dview_custom_op_top_left", text="   Operator")
                    layout.prop(self, "pie_3dview_custom_op_name_top_left", text="   Name")
                layout.prop(self, "pie_3dview_top_right")
                if self.pie_3dview_top_right == "CUSTOM_OP":
                    layout.prop(self, "pie_3dview_custom_op_top_right", text="   Operator")
                    layout.prop(self, "pie_3dview_custom_op_name_top_right", text="   Name")
                layout.prop(self, "pie_3dview_bottom_left")
                if self.pie_3dview_bottom_left == "CUSTOM_OP":
                    layout.prop(self, "pie_3dview_custom_op_bottom_left", text="   Operator")
                    layout.prop(self, "pie_3dview_custom_op_name_bottom_left", text="   Name")
                layout.prop(self, "pie_3dview_bottom_right")
                if self.pie_3dview_bottom_right == "CUSTOM_OP":
                    layout.prop(self, "pie_3dview_custom_op_bottom_right", text="   Operator")
                    layout.prop(self, "pie_3dview_custom_op_name_bottom_right", text="   Name")
            if self.pie_tab == 'PIE_UV_EDITOR':
                layout.prop(self, "pie_uv_editor_left")
                if self.pie_uv_editor_left == "CUSTOM_OP":
                    layout.prop(self, "pie_uv_editor_custom_op_left", text="   Operator")
                    layout.prop(self, "pie_uv_editor_custom_op_name_left", text="   Name")
                layout.prop(self, "pie_uv_editor_right")
                if self.pie_uv_editor_right == "CUSTOM_OP":
                    layout.prop(self, "pie_uv_editor_custom_op_right", text="   Operator")
                    layout.prop(self, "pie_uv_editor_custom_op_name_right", text="   Name")
                layout.prop(self, "pie_uv_editor_top")
                if self.pie_uv_editor_top == "CUSTOM_OP":
                    layout.prop(self, "pie_uv_editor_custom_op_top", text="   Operator")
                    layout.prop(self, "pie_uv_editor_custom_op_name_top", text="   Name")
                layout.prop(self, "pie_uv_editor_bottom")
                if self.pie_uv_editor_bottom == "CUSTOM_OP":
                    layout.prop(self, "pie_uv_editor_custom_op_bottom", text="   Operator")
                    layout.prop(self, "pie_uv_editor_custom_op_name_bottom", text="   Name")
                layout.prop(self, "pie_uv_editor_top_left")
                if self.pie_uv_editor_top_left == "CUSTOM_OP":
                    layout.prop(self, "pie_uv_editor_custom_op_top_left", text="   Operator")
                    layout.prop(self, "pie_uv_editor_custom_op_name_top_left", text="   Name")
                layout.prop(self, "pie_uv_editor_top_right")
                if self.pie_uv_editor_top_right == "CUSTOM_OP":
                    layout.prop(self, "pie_uv_editor_custom_op_top_right", text="   Operator")
                    layout.prop(self, "pie_uv_editor_custom_op_name_top_right", text="   Name")
                layout.prop(self, "pie_uv_editor_bottom_left")
                if self.pie_uv_editor_bottom_left == "CUSTOM_OP":
                    layout.prop(self, "pie_uv_editor_custom_op_bottom_left", text="   Operator")
                    layout.prop(self, "pie_uv_editor_custom_op_name_bottom_left", text="   Name")
                layout.prop(self, "pie_uv_editor_bottom_right")
                if self.pie_uv_editor_bottom_right == "CUSTOM_OP":
                    layout.prop(self, "pie_uv_editor_custom_op_bottom_right", text="   Operator")
                    layout.prop(self, "pie_uv_editor_custom_op_name_bottom_right", text="   Name")
        if self.tab == 'KEYMAP':
            self.draw_keymap(context)
        if self.tab == 'HELP':
            documentation = "https://alexbelyakov.gitlab.io/uv-toolkit-docs/"
            tutorials = "https://www.youtube.com/playlist?list=PLex7IjhY06w63StowG501tBbEyZrzHa00"
            gumroad = "https://gumroad.com/alexbel"
            blender_market = "https://blendermarket.com/creators/alexdev"
            twitter = "https://twitter.com/AIexanderBel"
            youtube = "https://www.youtube.com/channel/UCplYEvDn4G92ykGEKcyVaHw/featured"
            blender_artists = "https://blenderartists.org/t/uv-toolkit-for-blender-2-8x/1165216"
            polycount = "https://polycount.com/discussion/212218/uv-toolkit-for-blender-2-8"

            row = layout.row(align=True)
            row.operator("wm.url_open", text="Documentation",
                         icon_value=icons_coll["documentation"].icon_id).url = documentation
            row.operator("wm.url_open", text="Tutorials",
                         icon_value=icons_coll["tutorials"].icon_id).url = tutorials
            row = layout.row(align=True)
            row.operator("wm.url_open", text="Blender Market",
                         icon_value=icons_coll["blender_market"].icon_id).url = blender_market
            row.operator("wm.url_open", text="Gumroad",
                         icon_value=icons_coll["gumroad"].icon_id).url = gumroad
            row = layout.row(align=True)
            row.operator("wm.url_open", text="Twitter",
                         icon_value=icons_coll["twitter"].icon_id).url = twitter
            row.operator("wm.url_open", text="YouTube",
                         icon_value=icons_coll["youtube"].icon_id).url = youtube
            row = layout.row(align=True)
            row.operator("wm.url_open", text="Blender Artists",
                         icon_value=icons_coll["blender_artists"].icon_id).url = blender_artists
            row.operator("wm.url_open", text="Polycount",
                         icon_value=icons_coll["polycount"].icon_id).url = polycount
