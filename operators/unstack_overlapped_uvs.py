from collections import defaultdict

import bmesh
from bpy.types import Operator
from bpy.props import IntProperty, EnumProperty

from ..utils.uv_utils import (
    get_objects_seams,
    get_islands,
    get_bbox,
    calc_bbox_center,
)


class UnstackOverlappedUvs(Operator):
    bl_idname = "uv.toolkit_unstack_overlapped_uvs"
    bl_label = "Unstack Overlapped UVs"
    bl_description = "Transfer an overlapped UVs to another UDIM"
    bl_options = {'REGISTER', 'UNDO'}

    distance: IntProperty(
        name="Distance",
        default=1,
        min=1,
    )
    axis: EnumProperty(
        items=[
            ("U", "X", "", 0),
            ("-U", "-X", "", 1),
            ("V", "Y", "", 2),
            ("-V", "-Y", "", 3),
        ],
        name="Axis",
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, "distance")
        layout.prop(self, "axis", expand=True)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}
        # print("------------")
        all_islands = defaultdict(list)
        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                bbox = get_bbox(uv, island)
                bbox_center_u, bbox_center_v = calc_bbox_center(bbox)
                bbox_center = (float(f'{bbox_center_u:.5f}'), float(f'{bbox_center_v:.5f}'))
                island_loops = {ob: [f.index for f in island]}
                all_islands[bbox_center].append(island_loops)

        overlapped_islands = {}

        for bbox_center in all_islands:
            if len(all_islands[bbox_center]) == 1:
                continue
            if len(all_islands[bbox_center]) > 1:
                overlapped_islands[bbox_center] = all_islands[bbox_center]
                overlapped_islands[bbox_center].pop()

        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()
            bm.faces.ensure_lookup_table()

            if self.axis == "U":
                for bbox_center in overlapped_islands:
                    for ob_islands in overlapped_islands[bbox_center]:
                        if ob_islands.get(ob):
                            for idx in ob_islands[ob]:
                                for l in bm.faces[idx].loops:
                                    u, v = l[uv].uv
                                    l[uv].uv = u + self.distance, v
            if self.axis == "-U":
                for bbox_center in overlapped_islands:
                    for ob_islands in overlapped_islands[bbox_center]:
                        if ob_islands.get(ob):
                            for idx in ob_islands[ob]:
                                for l in bm.faces[idx].loops:
                                    u, v = l[uv].uv
                                    l[uv].uv = u - self.distance, v
            if self.axis == "V":
                for bbox_center in overlapped_islands:
                    for ob_islands in overlapped_islands[bbox_center]:
                        if ob_islands.get(ob):
                            for idx in ob_islands[ob]:
                                for l in bm.faces[idx].loops:
                                    u, v = l[uv].uv
                                    l[uv].uv = u, v + self.distance
            if self.axis == "-V":
                for bbox_center in overlapped_islands:
                    for ob_islands in overlapped_islands[bbox_center]:
                        if ob_islands.get(ob):
                            for idx in ob_islands[ob]:
                                for l in bm.faces[idx].loops:
                                    u, v = l[uv].uv
                                    l[uv].uv = u, v - self.distance
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
