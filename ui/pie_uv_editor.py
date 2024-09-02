from bpy.types import Menu

from ..functions import get_addon_preferences
from ..utils.ui_utils import get_operator_name, get_icons_set


class PieUvEditor(Menu):
    bl_idname = "UVTOOLKIT_MT_pie_uv_editor"
    bl_label = "UV Editor Pie"

    def pie_item(self, context, pie_property, custom_op, custom_op_name):
        icons_coll = get_icons_set(context, pie_menu=True)
        layout = self.layout
        pie = layout.menu_pie()
        if pie_property == "CUSTOM_OP":
            if custom_op_name:
                op_name = custom_op_name
            else:
                op_name = get_operator_name(context, custom_op)
            pie.operator("uv.toolkit_execute_custom_op", text=op_name).exec_op = custom_op
        elif pie_property == "MARK_SEAM":
            pie.operator("uv.mark_seam", text="Mark Seam",
                         icon_value=icons_coll["mark_seam"].icon_id).clear = False
        elif pie_property == "CLEAR_SEAM":
            pie.operator("uv.mark_seam", text="Clear Seam",
                         icon_value=icons_coll["clear_seam"].icon_id).clear = True
        elif pie_property == "PIN":
            pie.operator("uv.pin", text="Pin",
                         icon_value=icons_coll["pin_uv"].icon_id).clear = False
        elif pie_property == "UNPIN":
            pie.operator("uv.pin", text="Unpin",
                         icon_value=icons_coll["unpin_uv"].icon_id).clear = True
        elif pie_property == "DISABLE":
            pie.separator()
        elif pie_property == "uv.toolkit_center_cursor_and_frame_all":
            pie.operator(pie_property)
        else:
            icon_name = pie_property[11:]
            if icon_name == "align_uv":
                icon_name = "align_uv_min_y"
            pie.operator(pie_property, icon_value=icons_coll[icon_name].icon_id)

    def draw(self, context):
        addon_prefs = get_addon_preferences()
        self.pie_item(context,
                      addon_prefs.pie_uv_editor_left,
                      addon_prefs.pie_uv_editor_custom_op_left,
                      addon_prefs.pie_uv_editor_custom_op_name_left)  # 4
        self.pie_item(context,
                      addon_prefs.pie_uv_editor_right,
                      addon_prefs.pie_uv_editor_custom_op_right,
                      addon_prefs.pie_uv_editor_custom_op_name_right)  # 6
        self.pie_item(context,
                      addon_prefs.pie_uv_editor_bottom,
                      addon_prefs.pie_uv_editor_custom_op_bottom,
                      addon_prefs.pie_uv_editor_custom_op_name_bottom)  # 2
        self.pie_item(context,
                      addon_prefs.pie_uv_editor_top,
                      addon_prefs.pie_uv_editor_custom_op_top,
                      addon_prefs.pie_uv_editor_custom_op_name_top)  # 8
        self.pie_item(context,
                      addon_prefs.pie_uv_editor_top_left,
                      addon_prefs.pie_uv_editor_custom_op_top_left,
                      addon_prefs.pie_uv_editor_custom_op_name_top_left)  # 7
        self.pie_item(context,
                      addon_prefs.pie_uv_editor_top_right,
                      addon_prefs.pie_uv_editor_custom_op_top_right,
                      addon_prefs.pie_uv_editor_custom_op_name_top_right)  # 9
        self.pie_item(context,
                      addon_prefs.pie_uv_editor_bottom_left,
                      addon_prefs.pie_uv_editor_custom_op_bottom_left,
                      addon_prefs.pie_uv_editor_custom_op_name_bottom_left)  # 1
        self.pie_item(context,
                      addon_prefs.pie_uv_editor_bottom_right,
                      addon_prefs.pie_uv_editor_custom_op_bottom_right,
                      addon_prefs.pie_uv_editor_custom_op_name_bottom_right)  # 3
