import bmesh
from bpy.types import Operator
from ..utils.uv_utils import get_islands, get_objects_seams


class SelectIslandBorder(Operator):
    bl_idname = "uv.toolkit_select_island_border"
    bl_label = "Select Island Border"
    bl_description = "Select Island Border"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        current_uv_select_mode = scene.tool_settings.uv_select_mode

        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True):
                island_loops = set()
                for f in island:
                    for l in f.loops:
                        l[uv].select = False
                        island_loops.add(l)

                for f in island:
                    for e in f.edges:
                        if e.index in seams:
                            for v in e.verts:
                                for l in v.link_loops:
                                    if l in island_loops:
                                        l[uv].select = True
                    for l in f.loops:
                        if l.vert.is_boundary:
                            for l in l.vert.link_loops:
                                if l in island_loops:
                                    l[uv].select = True
            bmesh.update_edit_mesh(me)
        scene.tool_settings.uv_select_mode = 'VERTEX'
        scene.tool_settings.uv_select_mode = current_uv_select_mode
        return {'FINISHED'}
