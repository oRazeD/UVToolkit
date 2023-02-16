# from time import time
from math import sqrt
from collections import defaultdict

import bmesh
from bpy.types import Operator

from ..utils.uv_utils import (
    get_objects_seams,
    get_islands,
    get_bbox,
    calc_bbox_center,
    collect_island_params,
)


class MatchIslands(Operator):
    bl_idname = "uv.toolkit_match_islands"
    bl_label = "Match Islands"
    bl_description = "Make near-identical islands identical"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def build_map(self, target_bbox, target_bbox_center, target_coords):
        if len(target_coords) < 1000:
            subdivisions = 2
        if len(target_coords) > 1000:
            subdivisions = 4
        if len(target_coords) > 4000:
            subdivisions = 8
        if len(target_coords) > 20000:
            subdivisions = 12

        areas = defaultdict(list)

        bbox_width = target_bbox[1][0] - target_bbox[0][0]
        bbox_height = target_bbox[1][1] - target_bbox[0][1]
        width = bbox_width / subdivisions
        height = bbox_height / subdivisions
        start_point_u = target_bbox[0][0]
        start_point_v = target_bbox[0][1]
        next_point_u = start_point_u

        for _ in range(subdivisions):
            start_point_v = start_point_v + height
            for _ in range(subdivisions):
                next_point_u = next_point_u + width
                area_center = (next_point_u - width / 2,
                               start_point_v - height / 2)
                u1, v1 = next_point_u, start_point_v
                u2, v2 = area_center
                length = sqrt((u1 - u2) * (u1 - u2) + (v1 - v2) * (v1 - v2))
                min_length = length + (length / 100) * 5
                u1, v1 = area_center
                for point in target_coords:
                    u2, v2 = point
                    length = sqrt((u1 - u2) * (u1 - u2) + (v1 - v2) * (v1 - v2))
                    if length < min_length:
                        areas[area_center].append(point)
                    if not areas[area_center]:
                        del areas[area_center]
            next_point_u = start_point_u
        return areas

    def find_closest_point(self, areas, current_point, target_coords):
        min_length = 1000
        min_length_area = 1000
        area_coords = None

        u1, v1 = current_point
        for area in areas:
            u2, v2 = area
            length = sqrt((u1 - u2) * (u1 - u2) + (v1 - v2) * (v1 - v2))
            if length < min_length_area:
                min_length_area = length
                area_coords = areas[area]

        target_point = 0, 0
        for point in area_coords:
            u2, v2 = point
            length = sqrt((u1 - u2) * (u1 - u2) + (v1 - v2) * (v1 - v2))
            if length < min_length:
                min_length = length
                target_point = point
        return target_point

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        # print('>>>>>')
        # start = time()
        target_island_found = False
        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for target_island in get_islands(uv, bm, seams, has_selected_faces=True):
                target_island_found = True
                break
            if target_island_found:
                break
        if not target_island_found:
            return {'FINISHED'}

        target_stats = collect_island_params(uv, target_island)

        target_coords = {l[uv].uv[:]
                         for f in target_island
                         for l in f.loops}

        target_bbox = get_bbox(uv, target_island)
        target_bbox_center = calc_bbox_center(target_bbox)

        bbox_min_u, bbox_min_v = target_bbox[0]
        bbox_max_u, bbox_max_v = target_bbox[1]
        tolerance = (((bbox_max_u - bbox_min_u) / 100) * 15,
                     ((bbox_max_v - bbox_min_v) / 100) * 15)

        target_bbox_center_u, target_bbox_center_v = target_bbox_center
        min_tollerance_u = target_bbox_center_u - tolerance[0]
        max_tollerance_u = target_bbox_center_u + tolerance[0]
        min_tollerance_v = target_bbox_center_v - tolerance[1]
        max_tollerance_v = target_bbox_center_v + tolerance[1]

        areas = self.build_map(target_bbox, target_bbox_center, target_coords)

        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams):
                island_has_selection = False
                for f in island:
                    for l in f.loops:
                        if l[uv].select:
                            island_has_selection = True
                    if island_has_selection:
                        break

                if island_has_selection:
                    continue

                island_stats = collect_island_params(uv, island)
                if island_stats == target_stats:
                    bbox = get_bbox(uv, island)
                    bbox_center = calc_bbox_center(bbox)
                    bbox_center_u, bbox_center_v = bbox_center
                    if min_tollerance_u < bbox_center_u < max_tollerance_u \
                            and min_tollerance_v < bbox_center_v < max_tollerance_v:

                        island_uvs = defaultdict(set)
                        for f in island:
                            for l in f.loops:
                                coord = l[uv].uv
                                for l in l.vert.link_loops:
                                    if l[uv].uv == coord:
                                        island_uvs[coord[:]].add(l)

                        for uv_vert in island_uvs:
                            new_co = self.find_closest_point(
                                areas, uv_vert, target_coords)
                            for l in island_uvs[uv_vert]:
                                l[uv].uv = new_co

            bmesh.update_edit_mesh(me)
        # print(f"{(time() - start): .4f} sec")
        return {'FINISHED'}
