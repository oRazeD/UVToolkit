from bpy.types import Operator
from bpy.props import BoolProperty


class CreateNewUvLayer(Operator):
    bl_idname = "uv.toolkit_create_new_uv_layer"
    bl_label = "Create new UV layer"
    bl_description = "Create new UV layer for selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    set_active: BoolProperty(
        name="Set Active",
        default=True
    )

    def execute(self, context):
        scene = context.scene
        for ob in context.selected_objects:
            if ob.type == "MESH":
                ob.data.uv_layers.new(name=scene.uv_toolkit.uv_layer_name)
                if self.set_active:
                    ob.data.uv_layers.active_index = len(ob.data.uv_layers) - 1
        return {'FINISHED'}
