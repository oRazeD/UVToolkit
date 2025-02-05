import bpy

from .operators.find_shattered_islands import FindShatteredIslands
from .operators.align_uv import AlignUv
from .operators.border_seam import BorderSeam
from .operators.toggle_grid_type import ToggleGridType
from .operators.clear_all_pins import ClearAllPins
from .operators.clear_all_seams import ClearAllSeams
from .operators.create_checker_material import CheckerMaterial
from .operators.create_new_uv_layer import CreateNewUvLayer
from .operators.delete_uv_layer import DeleteUvLayer
from .operators.distribute import Distribute
from .operators.execute_custom_op import ExecuteCustomOp
from .operators.export_setting import ExportSettings
from .operators.import_settings import ImportSettings
from .operators.find_udim_crossing import FindUdimCrossing
from .operators.fit_to_bounds import FitToBounds
from .operators.hotkeys import Hotkeys
from .operators.invert_selection import InvertSelection
from .operators.match_islands import MatchIslands
from .operators.mirror_seam import MirrorSeam
from .operators.open_addon_settings import OpenAddonSettings
from .operators.orient_islands import OrientIslands
from .operators.orient_to_edge import OrientToEdge
from .operators.move_island import MoveIsland
from .operators.randomize_islands import RandomizeIslands
from .operators.remove_all_checker_materials import RemoveAllCheckerMaterials
from .operators.rename_uv_layers import RenameUvLayers
from .operators.rotate_islands import RotateIslands
from .operators.scale_individual_origins import ScaleIndividualOrigins
from .operators.scale_islands import ScaleIslands
from .operators.select_island_border import SelectIslandBorder
from .operators.select_similar_islands import SelectSimilarIslands
from .operators.set_active_uv_layer import SetActiveUvLayer
from .operators.select_flipped_islands import SelectFlippedIslands
from .operators.sharp_edges_from_uv_islands import SharpEdgesFromUvIslands
from .operators.split_faces_move import SplitFacesMove
from .operators.stack_islands import StackIslands
from .operators.stack_similar_islands import StackSimilarIslands
from .operators.straighten_island import StraightenIsland
from .operators.straighten_uv import Straighten
from .operators.test_op import TestOp
from .operators.toggle_color_mode import ToggleColorMode
from .operators.toggle_material import ToggleMaterial
from .operators.udim_packing import UdimPacking
from .operators.unstack_islands import UntackIslands
from .operators.unstack_overlapped_uvs import UnstackOverlappedUvs
from .operators.unwrap_selected import UnwrapSelected
from .operators.uv_sync_mode import UvSyncMode
from .operators.center_cursor_and_view_all import CenterCursorFrameAll

from .addon_preferences import UvToolkitPreferences

from .properties import UvToolkitProperties
from .functions import get_addon_preferences

from .ui.pie_3dview import Pie3dView
from .ui.pie_uv_editor import PieUvEditor

from .ui.panel import (
    UVTOOLKIT_PT_uv_sync,
    UVTOOLKIT_PT_uv_sync_settings,
    UVTOOLKIT_PT_tools,
    UVTOOLKIT_PT_pins,
    UVTOOLKIT_PT_transform,
    UVTOOLKIT_PT_unwrap,
    UVTOOLKIT_PT_align,
    UVTOOLKIT_PT_arrange,
    UVTOOLKIT_PT_select,
    UVTOOLKIT_PT_display,
    UVTOOLKIT_PT_uv_maps,
    UVTOOLKIT_PT_checker_map,
    UVTOOLKIT_PT_quick_presets,
    UVTOOLKIT_PT_checker_map_square,
    UVTOOLKIT_PT_checker_map_horizontal_rectangle,
    UVTOOLKIT_PT_checker_map_vertical_rectangle,
    UVTOOLKIT_PT_cleanup,
    UVTOOLKIT_PT_help,
)


from .register import (
    keymap_register,
    addon_keymaps,
    icons_register,
    icons_unregister,
)

from .addon_preferences import update_addon_category


classes = (
    FindShatteredIslands,
    AlignUv,
    BorderSeam,
    ToggleGridType,
    ClearAllPins,
    ClearAllSeams,
    CheckerMaterial,
    CreateNewUvLayer,
    DeleteUvLayer,
    Distribute,
    ExecuteCustomOp,
    ExportSettings,
    ImportSettings,
    FindUdimCrossing,
    FitToBounds,
    Hotkeys,
    InvertSelection,
    MatchIslands,
    MirrorSeam,
    OpenAddonSettings,
    OrientIslands,
    OrientToEdge,
    MoveIsland,
    RandomizeIslands,
    RotateIslands,
    RemoveAllCheckerMaterials,
    RenameUvLayers,
    ScaleIndividualOrigins,
    ScaleIslands,
    SelectIslandBorder,
    SelectSimilarIslands,
    SetActiveUvLayer,
    SelectFlippedIslands,
    SharpEdgesFromUvIslands,
    StraightenIsland,
    SplitFacesMove,
    StackIslands,
    Straighten,
    StackSimilarIslands,
    ToggleColorMode,
    ToggleMaterial,
    UdimPacking,
    UnwrapSelected,
    UvSyncMode,
    UntackIslands,
    UnstackOverlappedUvs,
    CenterCursorFrameAll,
    TestOp,
    UVTOOLKIT_PT_uv_sync,
    UVTOOLKIT_PT_uv_sync_settings,
    UVTOOLKIT_PT_tools,
    UVTOOLKIT_PT_pins,
    UVTOOLKIT_PT_transform,
    UVTOOLKIT_PT_unwrap,
    UVTOOLKIT_PT_align,
    UVTOOLKIT_PT_arrange,
    UVTOOLKIT_PT_select,
    UVTOOLKIT_PT_display,
    UVTOOLKIT_PT_uv_maps,
    UVTOOLKIT_PT_checker_map,
    UVTOOLKIT_PT_quick_presets,
    UVTOOLKIT_PT_checker_map_square,
    UVTOOLKIT_PT_checker_map_horizontal_rectangle,
    UVTOOLKIT_PT_checker_map_vertical_rectangle,
    UVTOOLKIT_PT_cleanup,
    UVTOOLKIT_PT_help,
    Pie3dView,
    PieUvEditor,
    UvToolkitPreferences,
    UvToolkitProperties,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.uv_toolkit = bpy.props.PointerProperty(type=UvToolkitProperties)

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        keymap_register(wm)

    icons_register()

    update_addon_category(get_addon_preferences(), bpy.context)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.uv_toolkit

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    icons_unregister()

if __name__ == "__main__":
    register()


# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
