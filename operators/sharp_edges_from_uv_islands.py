from collections import defaultdict

import bpy
import bmesh
from bpy.types import Operator
from bpy.props import BoolProperty


class SharpEdgesFromUvIslands(Operator):
    bl_idname = "uv.toolkit_sharp_edges_from_uv_islands"
    bl_label = "Sharp Edges From UV Islands"
    bl_description = "Marks UV Island boundaries with sharp edges and activates smooth shading"
    bl_options = {'REGISTER', 'UNDO'}

    use_existing_seams: BoolProperty(
        name="Use existing seams",
        default=False,
    )
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        current_mode = context.object.mode
        view_layer = context.view_layer
        act_ob = view_layer.objects.active

        selected_ob = list(context.selected_objects)
        mesh_ob = [ob for ob in context.selected_objects if ob.type == 'MESH']
        initial_selection = defaultdict(set)

        if not mesh_ob:
            return {'FINISHED'}

        for ob in selected_ob:
            if ob.type != 'MESH':
                ob.select_set(False)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.shade_auto_smooth(use_auto_smooth=True,
                                         angle=3.14159)

        view_layer.objects.active = mesh_ob[0]
        bpy.ops.object.mode_set(mode='EDIT')

        for ob in mesh_ob:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()
            view_layer.objects.active = ob

            bpy.ops.mesh.customdata_custom_splitnormals_clear()

            for f in bm.faces:
                f.smooth = True  # Set all faces shaded smooth
                for l in f.loops:
                    l.edge.smooth = True  # Remove all sharp edges
                    if l[uv].select:
                        initial_selection[ob].add(l.index)

        bpy.ops.uv.reveal()
        bpy.ops.uv.select_all(action='SELECT')
        if not self.use_existing_seams:
            bpy.ops.uv.seams_from_islands(mark_seams=False, mark_sharp=True)

        for ob in selected_ob:
            ob.select_set(True)
        view_layer.objects.active = act_ob

        for ob in context.objects_in_mode_unique_data:
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for f in bm.faces:
                for l in f.loops:
                    if l.index in initial_selection[ob]:
                        continue
                    l[uv].select = False
            if self.use_existing_seams:
                for e in bm.edges:
                    if e.seam:
                        e.smooth = False
        bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}
