import bpy
import bmesh
from bpy_extras import bmesh_utils
from bpy.props import IntProperty, BoolProperty
from bpy.types import Operator


class FindShatteredIslands(Operator):
    bl_idname = "uv.toolkit_find_shattered_islands"
    bl_label = "Find Shattered Islands"
    bl_description = "Find islands that contain an unusually small number of faces\n(and optionally pin them in the top-left corner)"
    bl_options = {'REGISTER', 'UNDO'}

    shattered_threshold: IntProperty(
        name="Threshold",
        description="The maximum number of faces for islands to be shattered",
        min=1,
        default=3
    )
    
    pin: BoolProperty(
        name="Pin to Corner",
        description="Move and pin islands to the top-left corner within UV space\n(handy for testing your workflow under ideal conditions)",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        use_uv_select_sync = scene.tool_settings.use_uv_select_sync

        if use_uv_select_sync:
            self.report({"INFO"}, "UV Sync enabled, selecting faces in the 3D view")

        for ob in bpy.context.objects_in_mode_unique_data:
            bm = bmesh.from_edit_mesh(ob.data)

            uv_layer = bm.loops.layers.uv.verify()
            islands = bmesh_utils.bmesh_linked_uv_islands(bm, uv_layer)
            shattered_islands = [i for i in islands if len(i) <= self.shattered_threshold]

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
