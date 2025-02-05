from bpy.types import Panel
import os

from ..functions import get_addon_preferences
from ..utils.ui_utils import get_icons_set


class UVTOOLKIT_PT_uv_sync(Panel):
    bl_label = "UV Sync"
    bl_idname = "UVTOOLKIT_PT_uv_sync"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator("uv.toolkit_sync_mode", text="Toggle UV Sync", icon='UV_SYNC_SELECT')


class UVTOOLKIT_PT_uv_sync_settings(Panel):
    bl_label = "UV Sync Settings"
    bl_parent_id = "UVTOOLKIT_PT_uv_sync"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        addon_prefs = get_addon_preferences()
        layout.label(text="Sync Selected Elements")
        layout.prop(addon_prefs, "sync_selection", expand=True)
        layout.label(text="Sync Selection Mode")
        layout.prop(addon_prefs, "sync_uv_selction_mode", expand=True)


class UVTOOLKIT_PT_tools(Panel):
    bl_label = "Tools"
    bl_idname = "UVTOOLKIT_PT_tools"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        icons_coll = get_icons_set(context)
        layout = self.layout
        layout.operator("uv.toolkit_sharp_edges_from_uv_islands",
                        icon_value=icons_coll["sharp_edges_from_uv_islands"].icon_id)
        prop = layout.operator("uv.seams_from_islands", icon_value=icons_coll["seams_from_islands"].icon_id)
        prop.mark_seams, prop.mark_sharp = True, False
        row = layout.row(align=True)
        row.operator("uv.toolkit_border_seam", icon_value=icons_coll["border_seam"].icon_id)
        row.operator("uv.toolkit_mirror_seam", icon_value=icons_coll["mirror_seam"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_split_faces_move", text="Split Faces",
                     icon_value=icons_coll["split_faces_move"].icon_id)
        row.operator("uv.toolkit_clear_all_seams", icon_value=icons_coll["clear_all_seams"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_udim_packing", icon_value=icons_coll["udim_packing"].icon_id)
        row.label(text="")
        # layout.label(text="Debug")
        # layout.scale_y = 2
        # layout.operator("uv.toolkit_test_op", icon='SHADERFX')


class UVTOOLKIT_PT_unwrap(Panel):
    bl_label = "Unwrap"
    bl_idname = "UVTOOLKIT_PT_unwrap"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        icons_coll = get_icons_set(context)
        layout = self.layout
        row = layout.row(align=True)
        row.operator("uv.toolkit_unwrap_selected", icon_value=icons_coll["unwrap_selected"].icon_id)
        row.operator("uv.toolkit_straighten_island",
                     icon_value=icons_coll["straighten_island"].icon_id)
        row = layout.row(align=True)
        row.operator('uv.toolkit_straighten',
                     icon_value=icons_coll["straighten"].icon_id).gridify = False
        row.operator('uv.toolkit_straighten', text="Gridify",
                     icon_value=icons_coll["gridify"].icon_id).gridify = True
        # row = layout.row(align=True)
        # row.operator("uv.toolkit_lazy_unwrap")
        # row.label(text="")


class UVTOOLKIT_PT_align(Panel):
    bl_label = "Align"
    bl_idname = "UVTOOLKIT_PT_align"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        scene = context.scene
        icons_coll = get_icons_set(context)
        layout = self.layout

        row = layout.row(align=True)
        # First column
        col = row.column(align=True)
        col.label(text="")
        col.operator('uv.toolkit_align_uv', text='', icon_value=icons_coll["align_uv_min_x"].icon_id).align_uv = 'MIN_U'
        # Second column
        col = row.column(align=True)
        col.scale_x = 3.15
        col.operator('uv.toolkit_align_uv', text='', icon_value=icons_coll["align_uv_max_y"].icon_id).align_uv = 'MAX_V'
        col.operator('uv.toolkit_align_uv', text='', icon_value=icons_coll["align_uv_min_y"].icon_id).align_uv = 'MIN_V'
        # Third column
        col = row.column(align=True)
        col.label(text="")
        col.operator('uv.toolkit_align_uv', text='', icon_value=icons_coll["align_uv_max_x"].icon_id).align_uv = 'MAX_U'
        row = layout.row(align=True)
        row.label(text="Mode")
        row.prop(scene.uv_toolkit, "align_mode", expand=True)


class UVTOOLKIT_PT_arrange(Panel):
    bl_label = "Arrange"
    bl_idname = "UVTOOLKIT_PT_arrange"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        icons_coll = get_icons_set(context)
        layout = self.layout
        row = layout.row(align=True)
        row.operator("uv.toolkit_orient_islands", icon_value=icons_coll["orient_islands"].icon_id)
        row.operator("uv.toolkit_orient_to_edge", icon_value=icons_coll["orient_to_edge"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_stack_islands", icon_value=icons_coll["stack_islands"].icon_id)
        row.operator("uv.toolkit_stack_similar_islands", text="Stack Similar",
                     icon_value=icons_coll["stack_similar_islands"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_unstack_islands", text="Unstack", icon_value=icons_coll["unstack_islands"].icon_id)
        row.operator("uv.toolkit_unstack_overlapped_uvs", icon_value=icons_coll["unstack_overlapped_uvs"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_distribute", icon_value=icons_coll["distribute"].icon_id)
        row.operator("uv.toolkit_match_islands", icon_value=icons_coll["match_islands"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_randomize_islands", text="Randomize",
                     icon_value=icons_coll["randomize_islands"].icon_id)
        row.operator("uv.toolkit_fit_to_bounds", icon_value=icons_coll["fit_to_bounds"].icon_id)
        # row.label(text="")


class UVTOOLKIT_PT_pins(Panel):
    bl_label = "Pins"
    bl_idname = "UVTOOLKIT_PT_pins"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        icons_coll = get_icons_set(context)
        layout = self.layout
        row = layout.row(align=True)
        row.operator("uv.pin", text="Pin", icon_value=icons_coll["pin_uv"].icon_id).clear = False
        row.operator("uv.pin", text="Unpin", icon_value=icons_coll["unpin_uv"].icon_id).clear = True
        row = layout.row(align=True)
        row.operator("uv.toolkit_clear_all_pins", icon_value=icons_coll["clear_all_pins"].icon_id)
        row.label(text="")


class UVTOOLKIT_PT_transform(Panel):
    bl_label = "Transform"
    bl_idname = "UVTOOLKIT_PT_transform"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        scene = context.scene
        icons_coll = get_icons_set(context)
        layout = self.layout
        row = layout.row(align=True)
        distance = scene.uv_toolkit.move_distance
        # First column
        col = row.column(align=True)
        col.operator_context = 'EXEC_DEFAULT'
        col.label(text="Move")
        col.operator("transform.translate", text="",
                     icon_value=icons_coll["move_left"].icon_id).value = (distance * -1, 0, 0)
        col.label(text="")
        # Second column
        col = row.column(align=True)
        col.operator("transform.translate", text="",
                     icon_value=icons_coll["move_up"].icon_id).value = (0, distance, 0)
        col.prop(scene.uv_toolkit, "move_distance", text="")
        col.operator("transform.translate", text="",
                     icon_value=icons_coll["move_down"].icon_id).value = (0, distance * - 1, 0)
        # Third column
        col = row.column(align=True)
        col.label(text="")
        col.operator("transform.translate", text="",
                     icon_value=icons_coll["move_right"].icon_id).value = (distance, 0, 0)
        col.label(text="")

        row = layout.row(align=True)
        row.scale_x = 2
        row.label(text="Rotate")
        row.scale_x = 2
        row.prop(scene.uv_toolkit, "island_rotation_angle", text="")
        row.prop(scene.uv_toolkit, "island_rotation_mode", expand=True)
        row = layout.row(align=True)
        angle = scene.uv_toolkit.island_rotation_angle
        row.operator("uv.toolkit_rotate_islands", text=f"-{angle}°",
                     icon_value=icons_coll["rotate_ccw"].icon_id).cw = False
        row.operator("uv.toolkit_rotate_islands", text=f"{angle}°",
                     icon_value=icons_coll["rotate_cw"].icon_id).cw = True
        # Scale
        row = layout.row(align=True)
        row.label(text="Scale")
        row.prop(scene.uv_toolkit, "island_scale_x")
        row.prop(scene.uv_toolkit, "island_scale_y")

        split = layout.split(factor=0.68, align=True)
        col = split.column(align=True)
        col.operator("uv.toolkit_scale_islands", icon_value=icons_coll["scale"].icon_id)
        col = split.column(align=True)
        row = col.row(align=True)
        row.prop(scene.uv_toolkit, "island_scale_mode", expand=True)

        row = layout.row(align=True)
        row.operator_context = 'EXEC_DEFAULT'
        row.operator("transform.mirror", text="Flip X",
                     icon_value=icons_coll["mirror_x"].icon_id).constraint_axis = (True, False, False)
        row.operator("transform.mirror", text="Flip Y",
                     icon_value=icons_coll["mirror_y"].icon_id).constraint_axis = (False, True, False)


class UVTOOLKIT_PT_select(Panel):
    bl_label = "Select"
    bl_idname = "UVTOOLKIT_PT_select"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        icons_coll = get_icons_set(context)
        layout = self.layout
        row = layout.row(align=True)
        row.operator("uv.toolkit_select_island_border",
                     text="Island border", icon_value=icons_coll["select_island_border"].icon_id)
        row.operator("uv.toolkit_select_similar_islands",
                     text="Similar Islands", icon_value=icons_coll["select_similar_islands"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_invert_selection", icon_value=icons_coll["invert_selection"].icon_id)
        row.operator("uv.toolkit_select_flipped_islands", text="Flipped Islands",
                     icon_value=icons_coll["select_flipped_islands"].icon_id)
        layout.operator("uv.toolkit_find_udim_crossing", icon_value=icons_coll["find_udim_crossing"].icon_id)
        layout.operator("uv.toolkit_find_shattered_islands", icon_value=icons_coll["find_shattered_islands"].icon_id)


class UVTOOLKIT_PT_display(Panel):
    bl_label = "Display"
    bl_idname = "UVTOOLKIT_PT_display"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        icons_coll = get_icons_set(context)
        layout = self.layout
        row = layout.row(align=True)
        row.operator("uv.toolkit_toggle_material", icon_value=icons_coll["toggle_material"].icon_id)
        row.operator("uv.toolkit_toggle_color_mode", icon_value=icons_coll["toggle_color_mode"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_toggle_grid_type", icon_value=icons_coll["toggle_grid_type"].icon_id)
        row.label(text="")


class UVTOOLKIT_PT_checker_map(Panel):
    bl_label = "Checker Map"
    bl_idname = "UVTOOLKIT_PT_checker_map"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw_user_checker_maps(self, context):
        supported_formats = {
            ".bmp", ".sgi", ".rgb", ".bw", ".png",
            ".jpg", ".jpeg", ".jp2", ".jp2", ".j2c",
            ".tga", ".cin", ".dpx", ".exr", ".hdr",
            ".tif", ".tiff"
        }

        def get_checker_maps_path():
            addon_prefs = get_addon_preferences()
            c_maps_path = addon_prefs.chekcer_maps_path
            if os.path.exists(c_maps_path):
                for path in os.listdir(path=c_maps_path):
                    current_path = os.path.join(c_maps_path, path)
                    if os.path.isfile(current_path):
                        file_format = os.path.splitext(current_path)[-1]
                        if file_format in supported_formats:
                            yield current_path

        layout = self.layout
        row = layout.row(align=True)
        idx = None
        for idx, path in enumerate(sorted(get_checker_maps_path()), 1):
            c_map_name = os.path.basename(os.path.splitext(path)[0])
            row.operator("uv.toolkit_create_checker_material", text=c_map_name).checker_image_path = path
            if idx % 2 == 0:
                row = layout.row(align=True)
        if idx and idx % 2 != 0:
            row.label(text="")

    def draw(self, context):
        scene = context.scene
        addon_prefs = get_addon_preferences()
        icons_coll = get_icons_set(context)
        layout = self.layout
        row = layout.row()
        row.prop(addon_prefs, "checker_map", expand=True)
        if addon_prefs.checker_map == "BUILT-IN":
            col = layout.column(align=True)
            split = col.split(align=True)
            split.prop(scene.uv_toolkit, "checker_map_width")
            split.prop(scene.uv_toolkit, "checker_map_height")
            row = col.row(align=True)
            row.prop(addon_prefs, "checker_type", expand=True)

            prop = layout.operator("uv.toolkit_create_checker_material",
                                   icon_value=icons_coll["create_checker_material"].icon_id)
            prop.width, prop.height = scene.uv_toolkit.checker_map_width, scene.uv_toolkit.checker_map_height
        else:
            self.draw_user_checker_maps(context)


class UVTOOLKIT_PT_quick_presets(Panel):
    bl_label = "Quick Presets"
    bl_idname = "UVTOOLKIT_PT_quick_presets"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    @classmethod
    def poll(cls, _context):
        return get_addon_preferences().checker_map == "BUILT-IN"

    def draw(self, context):
        pass


class UVTOOLKIT_PT_checker_map_square(Panel):
    bl_label = "Square"
    bl_parent_id = "UVTOOLKIT_PT_quick_presets"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="64x64")
        prop.width, prop.height = 64, 64
        prop = row.operator("uv.toolkit_create_checker_material", text="128x128")
        prop.width, prop.height = 128, 128
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="256x256")
        prop.width, prop.height = 256, 256
        prop = row.operator("uv.toolkit_create_checker_material", text="512x512")
        prop.width, prop.height = 512, 512
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="1024x1024")
        prop.width, prop.height = 1024, 1024
        prop = row.operator("uv.toolkit_create_checker_material", text="2048x2048")
        prop.width, prop.height = 2048, 2048
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="4096x4096")
        prop.width, prop.height = 4096, 4096
        prop = row.operator("uv.toolkit_create_checker_material", text="8192x8192")
        prop.width, prop.height = 8192, 8192


class UVTOOLKIT_PT_checker_map_horizontal_rectangle(Panel):
    bl_label = "Horizontal Rectangle"
    bl_parent_id = "UVTOOLKIT_PT_quick_presets"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="64x32")
        prop.width, prop.height = 64, 32
        prop = row.operator("uv.toolkit_create_checker_material", text="128x64")
        prop.width, prop.height = 128, 64
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="256x128")
        prop.width, prop.height = 256, 128
        prop = row.operator("uv.toolkit_create_checker_material", text="512x256")
        prop.width, prop.height = 512, 256
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="1024x512")
        prop.width, prop.height = 1024, 512
        prop = row.operator("uv.toolkit_create_checker_material", text="2048x1024")
        prop.width, prop.height = 2048, 1024
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="4096x2048")
        prop.width, prop.height = 4096, 2048
        prop = row.operator("uv.toolkit_create_checker_material", text="8192x4096")
        prop.width, prop.height = 8192, 4096


class UVTOOLKIT_PT_checker_map_vertical_rectangle(Panel):
    bl_label = "Vertical Rectangle"
    bl_parent_id = "UVTOOLKIT_PT_quick_presets"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="32x64")
        prop.width, prop.height = 32, 64
        prop = row.operator("uv.toolkit_create_checker_material", text="64x128")
        prop.width, prop.height = 64, 128
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="128x256")
        prop.width, prop.height = 128, 256
        prop = row.operator("uv.toolkit_create_checker_material", text="256x512")
        prop.width, prop.height = 256, 512
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="512x1024")
        prop.width, prop.height = 512, 1024
        prop = row.operator("uv.toolkit_create_checker_material", text="1024x2048")
        prop.width, prop.height = 1024, 2048
        row = layout.row(align=True)
        prop = row.operator("uv.toolkit_create_checker_material", text="2048x4096")
        prop.width, prop.height = 2048, 4096
        prop = row.operator("uv.toolkit_create_checker_material", text="4096x8192")
        prop.width, prop.height = 4096, 8192


class UVTOOLKIT_PT_cleanup(Panel):
    bl_label = "Cleanup"
    bl_idname = "UVTOOLKIT_PT_cleanup"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        icons_coll = get_icons_set(context)
        layout = self.layout
        layout.operator("uv.toolkit_remove_all_checker_materials",
                        icon_value=icons_coll["remove_all_checker_materials"].icon_id)


class UVTOOLKIT_PT_uv_maps(Panel):
    bl_label = "UV Maps"
    bl_idname = "UVTOOLKIT_PT_uv_maps"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"

    def draw(self, context):
        scene = context.scene
        icons_coll = get_icons_set(context)

        layout = self.layout
        row = layout.row()
        row.prop(scene.uv_toolkit, "uv_layer_name", text="Name")
        split = layout.split(factor=0.4)
        col = split.column()
        col.label(text="UV Set Index:")
        col = split.column()
        col.prop(scene.uv_toolkit, "uv_layer_index")
        row = layout.row(align=True)
        row.operator("uv.toolkit_set_active_uv_layer", text="Set Active",
                     icon_value=icons_coll["set_active_uv_layer"].icon_id)
        row.operator("uv.toolkit_create_new_uv_layer", text="Create New",
                     icon_value=icons_coll["create_new_uv_layer"].icon_id)
        row = layout.row(align=True)
        row.operator("uv.toolkit_rename_uv_layers", text="Rename",
                     icon_value=icons_coll["rename_uv_layers"].icon_id)
        row.operator("uv.toolkit_delete_uv_layer", text="Delete",
                     icon_value=icons_coll["delete_uv_layer"].icon_id)


class UVTOOLKIT_PT_help(Panel):
    bl_label = "Help/Settings"
    bl_idname = "UVTOOLKIT_PT_help"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "UV Toolkit"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        documentation = "https://alexbelyakov.gitlab.io/uv-toolkit-docs/"
        tutorials = "https://www.youtube.com/playlist?list=PLex7IjhY06w63StowG501tBbEyZrzHa00"
        icons_coll = get_icons_set(context)
        layout = self.layout
        layout.operator("uv.toolkit_open_addon_settings", icon_value=icons_coll["settings"].icon_id)
        layout.operator("uv.toolkit_hotkeys", text="List of Hotkeys", icon_value=icons_coll["hotkeys"].icon_id)
        layout.operator("wm.url_open", text="Documentation",
                        icon_value=icons_coll["documentation"].icon_id).url = documentation
        layout.operator("wm.url_open", text="Tutorials",
                        icon_value=icons_coll["tutorials"].icon_id).url = tutorials
