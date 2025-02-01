import bpy
import bmesh
from bpy_extras import bmesh_utils
from bpy.props import IntProperty, BoolProperty
from bpy.types import Operator


class FindShatteredUVs(Operator):
    bl_idname = "uv.toolkit_find_shattered_uvs"
    bl_label = "Find Shattered UVs"
    bl_description = "Find UV islands that contain an unusually small number of faces\n(and optionally pin them in the top-left corner)"
    bl_options = {'REGISTER', 'UNDO'}

    min_acceptance: IntProperty(
        name="Minimum Acceptance",
        description="The lowest number of faces an island must contain to be considered intact",
        default=4,
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'
    
    pin: BoolProperty(
        name="Pin",
        description="Move and pin islands to the top-left corner within the UV space\n(handy for testing your workflow under ideal conditions)",
        default=False,
    )

    def execute(self, context):
        scene = context.scene
        use_uv_select_sync = scene.tool_settings.use_uv_select_sync

        if use_uv_select_sync:
            self.report({"INFO"}, "UV Sync enabled, selecting faces in the 3D view")

        for ob in bpy.context.objects_in_mode_unique_data:
            bm = bmesh.from_edit_mesh(ob.data)

            uv_layer = bm.loops.layers.uv.verify()
            islands = bmesh_utils.bmesh_linked_uv_islands(bm, uv_layer)
            shattered_islands = [i for i in islands if len(i) < self.min_acceptance]

            if len(shattered_islands) < 1:
                continue

            bm.faces.ensure_lookup_table()

            for island in shattered_islands:
                for face in island:
                    if use_uv_select_sync:
                         face.select = True
                    for loop in face.loops:
                        if not use_uv_select_sync:
                            loop[uv_layer].select = True
                        if self.pin:
                            loop[uv_layer].uv = (0, 1)
                            loop[uv_layer].pin_uv = True
            
            bmesh.update_edit_mesh(ob.data)
            bm.free()
        return {'FINISHED'}
