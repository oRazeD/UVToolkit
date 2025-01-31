import bpy
import bmesh
from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty

from ..utils.uv_utils import (
    clear_all_seams,
    get_objects_seams,
    get_islands
)


class StraightenIsland(Operator):
    bl_idname = "uv.toolkit_straighten_island"
    bl_label = "Straighten Island"
    bl_description = "Straightens the selected edges and relaxes faces around"
    bl_options = {'REGISTER', 'UNDO'}

    method: EnumProperty(
        name="Method",
        items=[
            ("ANGLE_BASED", "Angle Based", ""),
            ("CONFORMAL", "Conformal", ""),
        ]
    )
    pin: BoolProperty(
        name="Pin",
        default=False,
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

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def straighten_island(self, context, ob, seams):
        scene = context.scene
        current_uv_select_mode = scene.tool_settings.uv_select_mode
        scene.tool_settings.uv_select_mode = 'VERTEX'

        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        uv = bm.loops.layers.uv.verify()

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
                l[uv].pin_uv = True

        for island in get_islands(uv, bm, seams, has_selected_faces=True):
            for f in island:
                for l in f.loops:
                    if l[uv].select is False:
                        l[uv].pin_uv = False

        if self.pin:
            for loop_uv in initial_pins:
                loop_uv.pin_uv = True

        for f in bm.faces:
            for l in f.loops:
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

        for loop_uv in initial_pins:
            loop_uv.pin_uv = True

        for f in bm.faces:
            for l in f.loops:
                if l in initial_selection:
                    continue
                l[uv].select = False

        scene.tool_settings.uv_select_mode = current_uv_select_mode

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        objects_seams = get_objects_seams(context)
        view_layer = context.view_layer
        act_ob = view_layer.objects.active
        selected_ob = list(context.objects_in_mode_unique_data)

        bpy.ops.uv.toolkit_distribute(
            preserve_edge_length=True, align_to_nearest_axis=True)
        bpy.ops.object.mode_set(mode='OBJECT')

        for ob in selected_ob:
            ob.select_set(False)

        for ob in selected_ob:
            seams = objects_seams[ob]
            view_layer.objects.active = ob
            ob.select_set(True)

            bpy.ops.object.mode_set(mode='EDIT')

            self.straighten_island(context, ob, seams)

            bpy.ops.object.mode_set(mode='OBJECT')

            ob.select_set(False)

        for ob in selected_ob:
            ob.select_set(True)

        view_layer.objects.active = act_ob
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}
