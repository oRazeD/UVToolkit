import bpy

from ..functions import get_addon_preferences
from ..register import icons_collections

# EnumProperty
# [(identifier, name, description, icon, number),..]
uv_editor_items = [
    ("uv.toolkit_align_uv", "Align UV", ""),
    ("uv.toolkit_clear_all_seams", "Clear All Seams", ""),
    ("uv.toolkit_distribute", "Distribute", ""),
    ("uv.toolkit_find_udim_crossing", "Find UDIMs crossing", ""),
    ("uv.toolkit_fit_to_bounds", "Fit to Bounds", ""),
    ("uv.toolkit_invert_selection", "Invert Selection", ""),
    ("uv.toolkit_match_islands", "Match Islands", ""),
    ("uv.toolkit_orient_islands", "Orient Islands", ""),
    ("uv.toolkit_orient_to_edge", "Orient to Edge", ""),
    ("uv.toolkit_randomize_islands", "Randomize Islands", ""),
    ("uv.toolkit_remove_all_checker_materials", "Remove All Checker Materials", ""),
    ("uv.toolkit_select_island_border", "Select Island Border", ""),
    ("uv.toolkit_select_similar_islands", "Select Similar Islands", ""),
    ("uv.toolkit_select_flipped_islands", "Select Flipped Islands", ""),
    ("uv.toolkit_sharp_edges_from_uv_islands", "Sharp Edges From UV Islands", ""),
    ("uv.toolkit_split_faces_move", "Split Faces", ""),
    ("uv.toolkit_stack_islands", "Stack Islands", ""),
    ("uv.toolkit_stack_similar_islands", "Stack Similar Islands", ""),
    ("uv.toolkit_straighten_island", "Straighten Island", ""),
    ("uv.toolkit_straighten", "Straighten UVs", ""),
    ("uv.toolkit_toggle_material", "Toggle Material", ""),
    ("uv.toolkit_toggle_color_mode", "Toggle Color Mode", ""),
    ("uv.toolkit_unstack_islands", "Unstack Islands", ""),
    ("uv.toolkit_unstack_overlapped_uvs", "Unstack Overlapped UVs", ""),
    ("uv.toolkit_unwrap_selected", "Unwrap Selected", ""),
    ("uv.toolkit_center_cursor_and_frame_all", "Center Cursor and View All", ""),
    ("uv.toolkit_udim_packing", "Pack UVs", ""),
    ("uv.toolkit_clear_all_pins", "Clear All Pins", ""),
    ("PIN", "Pin", ""),
    ("UNPIN", "Unpin", ""),
    ("MARK_SEAM", "Mark Seam", ""),
    ("CLEAR_SEAM", "Clear Seam", ""),
    ("CUSTOM_OP", "Custom operator", ""),
    ("DISABLE", "Disable", ""),
]

view3d_items = [
    ("uv.toolkit_clear_all_seams", "Clear All Seams", ""),
    ("uv.toolkit_remove_all_checker_materials", "Remove All Checker Materials", ""),
    ("uv.toolkit_sharp_edges_from_uv_islands", "Sharp Edges From UV Islands", ""),
    ("uv.toolkit_toggle_material", "Toggle Material", ""),
    ("uv.toolkit_toggle_color_mode", "Toggle Color Mode", ""),
    ("uv.toolkit_border_seam", "Border Seam", ""),
    ("uv.toolkit_mirror_seam", "Mirror Seam", ""),
    ("uv.unwrap", "Unwrap", ""),
    ("MARK_SEAM", "Mark Seam", ""),
    ("CLEAR_SEAM", "Clear Seam", ""),
    ("UV_MENU", "UV menu", ""),
    ("CUSTOM_OP", "Custom operator", ""),
    ("DISABLE", "Disable", ""),
]


def get_operator_name(context, custom_op):
    custom_op = custom_op.split(".")
    if 3 < len(custom_op):
        if hasattr(bpy.ops, custom_op[2]):
            op_category = getattr(bpy.ops, custom_op[2])
            op_id_end_line = custom_op[3].find("(")
            op_id = custom_op[3][:op_id_end_line]
            op = getattr(op_category, op_id)
            return op.get_rna_type().name
    return "Unknown Operator"


def get_icons_set(context, pie_menu=False):
    addon_prefs = get_addon_preferences()
    if addon_prefs.icon_style == 'LIGHT' or pie_menu:
        icons_coll = icons_collections["light"]
    else:
        icons_coll = icons_collections["dark"]
    return icons_coll
