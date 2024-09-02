import bmesh
from bpy.types import Operator

from ..functions import get_addon_preferences


class UvSyncMode(Operator):
    bl_idname = "uv.toolkit_sync_mode"
    bl_label = "UV Sync mode"
    bl_description = "Toggle UV Sync Mode"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def sync_uv_selction_mode(self, context, uv_sync_enable):
        scene = context.scene

        vertex = True, False, False
        edge = False, True, False
        face = False, False, True

        if uv_sync_enable:
            uv_select_mode = scene.tool_settings.uv_select_mode
            tool_settings = context.tool_settings

            if uv_select_mode == 'VERTEX':
                tool_settings.mesh_select_mode = vertex
            if uv_select_mode == 'EDGE':
                tool_settings.mesh_select_mode = edge
            if uv_select_mode == 'FACE':
                tool_settings.mesh_select_mode = face

        else:
            mesh_select_mode = context.tool_settings.mesh_select_mode[:]
            tool_settings = scene.tool_settings

            if mesh_select_mode == vertex:
                tool_settings.uv_select_mode = 'VERTEX'
            if mesh_select_mode == edge:
                tool_settings.uv_select_mode = 'EDGE'
            if mesh_select_mode == face:
                tool_settings.uv_select_mode = 'FACE'

    def sync_selected_elements(self, context, uv_sync_enable):
        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)

            uv_layer = bm.loops.layers.uv.verify()

            if uv_sync_enable:
                for face in bm.faces:
                    for loop in face.loops:
                        loop_uv = loop[uv_layer]
                        if not loop_uv.select:
                            face.select = False

                for face in bm.faces:
                    for loop in face.loops:
                        loop_uv = loop[uv_layer]
                        if loop_uv.select:
                            loop.vert.select = True

                for edge in bm.edges:
                    vert_count = 0
                    for vert in edge.verts:
                        if vert.select:
                            vert_count += 1
                    if vert_count == 2:
                        edge.select = True

            else:
                for face in bm.faces:
                    for loop in face.loops:
                        loop_uv = loop[uv_layer]
                        loop_uv.select = False

                mesh_select_mode = context.tool_settings.mesh_select_mode[:]

                if mesh_select_mode[2]:  # face
                    for face in bm.faces:
                        if face.select:
                            for loop in face.loops:
                                loop_uv = loop[uv_layer]
                                if loop.vert.select:
                                    loop_uv.select = True
                else:
                    for face in bm.faces:
                        for loop in face.loops:
                            loop_uv = loop[uv_layer]
                            if loop.vert.select:
                                loop_uv.select = True

                for face in bm.faces:
                    face.select = True

            bmesh.update_edit_mesh(me)

    def execute(self, context):
        addon_prefs = get_addon_preferences()
        tool_settings = context.tool_settings
        uv_sync_enable = not tool_settings.use_uv_select_sync
        tool_settings.use_uv_select_sync = uv_sync_enable

        if addon_prefs.sync_uv_selction_mode == "enable":
            self.sync_uv_selction_mode(context, uv_sync_enable)

        if addon_prefs.sync_selection == "enable":
            self.sync_selected_elements(context, uv_sync_enable)
        return {'FINISHED'}
