import bmesh
from bpy.types import Operator
from bpy.props import EnumProperty

from ..utils.uv_utils import get_islands, get_bbox, get_objects_seams


class AlignUv(Operator):
    bl_idname = "uv.toolkit_align_uv"
    bl_label = "Align UV"
    bl_description = "Align Verts or UV Islands"
    bl_options = {'REGISTER', 'UNDO'}

    align_uv: EnumProperty(
        name='Axis',
        items=[
            ('MAX_U', 'Max X', ''),
            ('MIN_U', 'Min X', ''),
            ('MAX_V', 'Max Y', ''),
            ('MIN_V', 'Min Y', ''),
        ],
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def align_islands(self, context):
        bboxes = []
        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()
            for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                bbox = get_bbox(uv, island)
                bboxes.append(bbox)

        if not bboxes:
            return {'CANCELED'}

        if self.align_uv == 'MAX_U':
            max_u = max([bbox[1][0] for bbox in bboxes])
            for ob in context.objects_in_mode_unique_data:
                seams = objects_seams[ob]
                me = ob.data
                bm = bmesh.from_edit_mesh(me)
                uv = bm.loops.layers.uv.verify()
                for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                    bbox = get_bbox(uv, island)
                    bbox_max_u = bbox[1][0]
                    distance = max_u - bbox_max_u
                    for f in island:
                        for l in f.loops:
                            u, v = l[uv].uv
                            new_co = u + distance, v
                            l[uv].uv = new_co
                bmesh.update_edit_mesh(me)

        if self.align_uv == 'MIN_U':
            min_u = min([bbox[0][0] for bbox in bboxes])
            for ob in context.objects_in_mode_unique_data:
                seams = objects_seams[ob]
                me = ob.data
                bm = bmesh.from_edit_mesh(me)
                uv = bm.loops.layers.uv.verify()
                for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                    bbox = get_bbox(uv, island)
                    bbox_min_u = bbox[0][0]
                    distance = bbox_min_u - min_u
                    for f in island:
                        for l in f.loops:
                            u, v = l[uv].uv
                            new_co = u - distance, v
                            l[uv].uv = new_co
                bmesh.update_edit_mesh(me)

        if self.align_uv == 'MAX_V':
            max_v = max([bbox[1][1] for bbox in bboxes])
            for ob in context.objects_in_mode_unique_data:
                seams = objects_seams[ob]
                me = ob.data
                bm = bmesh.from_edit_mesh(me)
                uv = bm.loops.layers.uv.verify()
                for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                    bbox = get_bbox(uv, island)
                    bbox_max_v = bbox[1][1]
                    distance = max_v - bbox_max_v
                    for f in island:
                        for l in f.loops:
                            u, v = l[uv].uv
                            new_co = u, v + distance
                            l[uv].uv = new_co
                bmesh.update_edit_mesh(me)

        if self.align_uv == 'MIN_V':
            min_v = min([bbox[0][1] for bbox in bboxes])
            for ob in context.objects_in_mode_unique_data:
                seams = objects_seams[ob]
                me = ob.data
                bm = bmesh.from_edit_mesh(me)
                uv = bm.loops.layers.uv.verify()
                for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                    bbox = get_bbox(uv, island)
                    bbox_min_v = bbox[0][1]
                    distance = bbox_min_v - min_v
                    for f in island:
                        for l in f.loops:
                            u, v = l[uv].uv
                            new_co = u, v - distance
                            l[uv].uv = new_co
                bmesh.update_edit_mesh(me)

    def align_vertices(self, context):
        coords = []

        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for f in bm.faces:
                if f.select:
                    for l in f.loops:
                        if l[uv].select:
                            coords.append(l[uv].uv[:])

        if not coords:
            return {'CANCELED'}

        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            if self.align_uv == 'MAX_U':
                u = max([uv[0] for uv in coords])
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            if l[uv].select:
                                for l in l.vert.link_loops:
                                    if l[uv].select:
                                        l[uv].uv[0] = u

            if self.align_uv == 'MIN_U':
                u = min([uv[0] for uv in coords])
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            if l[uv].select:
                                for l in l.vert.link_loops:
                                    if l[uv].select:
                                        l[uv].uv[0] = u

            if self.align_uv == 'MAX_V':
                v = max([uv[1] for uv in coords])
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            if l[uv].select:
                                for l in l.vert.link_loops:
                                    if l[uv].select:
                                        l[uv].uv[1] = v

            if self.align_uv == 'MIN_V':
                v = min([uv[1] for uv in coords])
                for f in bm.faces:
                    if f.select:
                        for l in f.loops:
                            if l[uv].select:
                                for l in l.vert.link_loops:
                                    if l[uv].select:
                                        l[uv].uv[1] = v
            bmesh.update_edit_mesh(me)

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        if scene.uv_toolkit.align_mode == 'VERTICES':
            self.align_vertices(context)
        else:
            self.align_islands(context)
        return {'FINISHED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
        row.label(text="")
        row.prop(scene.uv_toolkit, "align_mode", expand=True)
        layout.use_property_split = True
        layout.prop(self, "align_uv", expand=True)
