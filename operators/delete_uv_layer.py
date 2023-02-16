from bpy.types import Operator
from bpy.props import EnumProperty


class DeleteUvLayer(Operator):
    bl_idname = "uv.toolkit_delete_uv_layer"
    bl_label = "Delete UV layer"
    bl_description = "Delete UV layer for selected objects"
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
                    if len(ob.data.uv_layers) >= scene_layer_index:
                        ob.data.uv_layers.remove(ob.data.uv_layers[scene_layer_index - 1])
                if self.mode == "NAME":
                    for uv_layer in ob.data.uv_layers:
                        if uv_layer.name == scene.uv_toolkit.uv_layer_name:
                            ob.data.uv_layers.remove(uv_layer)
                            break
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, "mode", expand=True)
