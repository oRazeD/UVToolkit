import bmesh
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty

from ..utils.uv_utils import (
    get_objects_seams,
    get_islands,
    get_bbox,
)


class UntackIslands(Operator):
    bl_idname = "uv.toolkit_unstack_islands"
    bl_label = "Unstack Islands"
    bl_description = "Places islands in an axis with a given indent"
    bl_options = {'REGISTER', 'UNDO'}

    margin: FloatProperty(
        name="Margin",
        default=0.005,
        min=0,
        max=1,
        step=0.01,
        precision=3,
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
        layout.prop(self, "margin")
        layout.prop(self, "axis", expand=True)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        is_initial_island = False
        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                bbox = get_bbox(uv, island)
                if self.axis == 'U':
                    if not is_initial_island:
                        is_initial_island = True
                        island_bound = bbox[1][0]
                    else:
                        margin = self.margin
                        offset = (island_bound - bbox[0][0]) + margin
                        for f in island:
                            for l in f.loops:
                                u = l[uv].uv[0] + offset
                                v = l[uv].uv[1]
                                l[uv].uv = (u, v)
                        island_width = abs(bbox[0][0] - bbox[1][0])
                        island_bound = island_bound + margin + island_width
                if self.axis == '-U':
                    if not is_initial_island:
                        is_initial_island = True
                        island_bound = bbox[0][0]
                    else:
                        margin = self.margin
                        offset = (island_bound - bbox[1][0]) - margin
                        for f in island:
                            for l in f.loops:
                                u = l[uv].uv[0] + offset
                                v = l[uv].uv[1]
                                l[uv].uv = (u, v)
                        island_width = abs(bbox[0][0] - bbox[1][0])
                        island_bound = island_bound - margin - island_width
                if self.axis == 'V':
                    if not is_initial_island:
                        is_initial_island = True
                        island_bound = bbox[1][1]
                    else:
                        margin = self.margin
                        offset = (island_bound - bbox[0][1]) + margin
                        for f in island:
                            for l in f.loops:
                                u = l[uv].uv[0]
                                v = l[uv].uv[1] + offset
                                l[uv].uv = (u, v)
                        island_height = abs(bbox[0][1] - bbox[1][1])
                        island_bound = island_bound + margin + island_height
                if self.axis == '-V':
                    if not is_initial_island:
                        is_initial_island = True
                        island_bound = bbox[0][1]
                    else:
                        margin = self.margin
                        offset = (island_bound - bbox[1][1]) - margin
                        for f in island:
                            for l in f.loops:
                                u = l[uv].uv[0]
                                v = l[uv].uv[1] + offset
                                l[uv].uv = (u, v)
                        island_height = abs(bbox[0][1] - bbox[1][1])
                        island_bound = island_bound - margin - island_height
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}
