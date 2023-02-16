from bpy.types import Operator
from bpy.props import EnumProperty


class SetActiveUvLayer(Operator):
    bl_idname = "uv.toolkit_set_active_uv_layer"
    bl_label = "Set Active UV layer"
    bl_description = "Set active UV layer for selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(
        name="Mode",
        items=[
            ("INDEX", "Index", ""),
            ("NAME", "Name", "")
        ],
    )

    def execute(self, context):
        scene = context.scene
        ob = context.active_object
        scene_layer_index = scene.uv_toolkit.uv_layer_index

        for ob in context.selected_objects:
            if ob.type == "MESH":
                if self.mode == "INDEX":
                    if len(ob.data.uv_layers) < scene_layer_index:
                        continue
                    ob.data.uv_layers.active_index = scene_layer_index - 1
                if self.mode == "NAME":
                    for uv_layer in ob.data.uv_layers:
                        if uv_layer.name == scene.uv_toolkit.uv_layer_name:
                            uv_layer.active = True
                            break
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, "mode", expand=True)
