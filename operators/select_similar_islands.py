from collections import defaultdict

import bmesh
from bpy.types import Operator
from bpy.props import IntProperty

from ..utils.uv_utils import (
    get_objects_seams,
    get_islands,
    get_bbox,
    get_bbox_size,
    collect_island_params,
)


class SelectSimilarIslands(Operator):
    bl_idname = "uv.toolkit_select_similar_islands"
    bl_label = "Select Similar Islands"
    bl_description = "Select Similar Islands"
    bl_options = {'REGISTER', 'UNDO'}

    threshold: IntProperty(
        name="Threshold",
        default=10,
        min=0,
        max=1000,
    )
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def is_same_bbox_size(self, target_bbox_size, current_bbox_size):
        """Compares two islands in bbox size"""
        target_bbox_width = target_bbox_size[0]
        target_bbox_height = target_bbox_size[1]
        delta = 0.0001 * self.threshold
        target_bbox_width_min = target_bbox_width - delta
        target_bbox_width_max = target_bbox_width + delta
        target_bbox_height_min = target_bbox_height - delta
        target_bbox_height_max = target_bbox_height + delta
        current_bbox_width, current_bbox_height = current_bbox_size

        if target_bbox_width_min < current_bbox_width < target_bbox_width_max \
                and target_bbox_height_min < current_bbox_height < target_bbox_height_max:
            return True

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        current_uv_select_mode = scene.tool_settings.uv_select_mode

        # Collect the selected islands params
        islands_params = defaultdict(set)
        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True):
                current_bbox = get_bbox(uv, island)
                current_bbox_size = get_bbox_size(current_bbox)
                current_island_params = collect_island_params(uv, island)

                islands_params[current_island_params].add((current_bbox_size))
                # need to remove the same islands to get the coordinates for packaging
                if len(islands_params[current_island_params]) > 1:
                    found_same_islands = 0
                    for bbox_params in islands_params[current_island_params]:
                        target_bbox_size = bbox_params
                        if self.is_same_bbox_size(target_bbox_size, current_bbox_size):
                            found_same_islands += 1
                    if found_same_islands > 1:
                        for _ in range(found_same_islands - 1):
                            islands_params[current_island_params].discard((current_bbox_size))

        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()
            seams = objects_seams[ob]
            for island in get_islands(uv, bm, seams):
                current_island_params = collect_island_params(uv, island)
                target_island = islands_params.get(current_island_params)
                if target_island:
                    current_bbox = get_bbox(uv, island)
                    current_bbox_size = get_bbox_size(current_bbox)
                    for bbox_params in target_island:
                        target_bbox_size = bbox_params
                        if self.is_same_bbox_size(target_bbox_size, current_bbox_size):
                            for f in island:
                                for l in f.loops:
                                    l[uv].select = True
            bmesh.update_edit_mesh(me)

        scene.tool_settings.uv_select_mode = 'VERTEX'
        scene.tool_settings.uv_select_mode = current_uv_select_mode

        return {'FINISHED'}
