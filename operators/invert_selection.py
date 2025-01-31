import bpy
import bmesh
from bpy.props import BoolProperty
from bpy.types import Operator

from ..utils.uv_utils import (
    create_list_of_loops_from_uv_selection
)


class InvertSelection(Operator):
    bl_idname = "uv.toolkit_invert_selection"
    bl_label = "Invert selection"
    bl_description = "Invert selection locally or globally"
    bl_options = {'UNDO', 'REGISTER'}

    local: BoolProperty(
        name="Local",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        current_uv_select_mode = scene.tool_settings.uv_select_mode

        if self.local:

            if scene.tool_settings.use_uv_select_sync:
                self.report({'INFO'}, "Need to disable UV Sync")
                return {'CANCELLED'}

            view_layer = context.view_layer
            act_ob = view_layer.objects.active

            selected_ob = tuple(context.objects_in_mode_unique_data)

            bpy.ops.object.mode_set(mode='OBJECT')

            for ob in selected_ob:
                ob.select_set(False)

            for ob in selected_ob:
                view_layer.objects.active = ob
                ob.select_set(True)

                bpy.ops.object.mode_set(mode='EDIT')

                me = ob.data
                bm = bmesh.from_edit_mesh(me)
                uv = bm.loops.layers.uv.verify()

                loops = create_list_of_loops_from_uv_selection(uv, bm.faces)

                bpy.ops.uv.select_linked()

                for l in loops:
                    l[uv].select = False

                bpy.ops.object.mode_set(mode='OBJECT')
                ob.select_set(False)

            for ob in selected_ob:
                ob.select_set(True)

            bpy.ops.object.mode_set(mode='EDIT')
            view_layer.objects.active = act_ob
        else:
            bpy.ops.uv.select_all(action='INVERT')

        scene.tool_settings.uv_select_mode = 'VERTEX'
        scene.tool_settings.uv_select_mode = current_uv_select_mode
        return {'FINISHED'}
