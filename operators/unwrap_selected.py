import bpy
import bmesh
from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty

from ..utils.uv_utils import clear_all_seams


class UnwrapSelected(Operator):
    bl_idname = "uv.toolkit_unwrap_selected"
    bl_label = "Unwrap Selected"
    bl_description = "Unwrap the selected faces"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    method: EnumProperty(
        name="Method",
        items=[
            ("ANGLE_BASED", "Angle Based", ""),
            ("CONFORMAL", "Conformal", ""),
        ]
    )
    fill_holes: BoolProperty(
        name="Fill Holes",
        default=True,
    )
    correct_aspect: BoolProperty(
        name="Correct Aspect",
        default=False,
    )
    use_subsurf_data: BoolProperty(
        name="Use Subdivision Surface",
        default=False,
    )

    def unwrap_selected_uv_verts(self, bm, uv):
        initial_pins = []
        initial_seams = []
        initial_selection = set()

        for f in bm.faces:
            for l in f.loops:
                if l[uv].pin_uv:
                    initial_pins.append(l[uv])

                if l.edge.seam:
                    initial_seams.append(l.edge)

                if l[uv].select:
                    initial_selection.add(l)
                else:
                    l[uv].pin_uv = True
                l[uv].select = True

        bpy.ops.uv.seams_from_islands(mark_seams=True)
        bpy.ops.uv.unwrap(method=self.method,
                          fill_holes=self.fill_holes,
                          correct_aspect=self.correct_aspect,
                          use_subsurf_data=self.use_subsurf_data,
                          margin=0)

        clear_all_seams(bm)

        for e in initial_seams:
            e.seam = True

        for f in bm.faces:
            for l in f.loops:
                l[uv].pin_uv = False

        for l in initial_pins:
            l.pin_uv = True

        for f in bm.faces:
            for l in f.loops:
                if l in initial_selection:
                    continue
                l[uv].select = False

    def execute(self, context):
        scene = context.scene
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

            self.unwrap_selected_uv_verts(bm, uv)

            bpy.ops.object.mode_set(mode='OBJECT')
            ob.select_set(False)

        for ob in selected_ob:
            ob.select_set(True)

        bpy.ops.object.mode_set(mode='EDIT')
        view_layer.objects.active = act_ob
        return {'FINISHED'}
