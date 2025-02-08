from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty


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
    render: BoolProperty(
        name="Active Render",
        default=False,
    )
    cloning: BoolProperty(
        name="Active Cloning",
        default=True,
    )

    def invoke(self, context, event):
        scene = context.scene
        if scene.uv_toolkit.uv_layer_name != "":
            self.mode = "NAME"
        else:
            self.mode = "INDEX"
        return self.execute(context)

    def execute(self, context):
        scene = context.scene
        ob = context.active_object
        scene_layer_index = scene.uv_toolkit.uv_layer_index

        for ob in context.selected_objects:
            if ob.type != "MESH":
                continue
            if self.mode == "INDEX":
                if len(ob.data.uv_layers) < scene_layer_index:
                    continue
                ob.data.uv_layers.active_index = scene_layer_index - 1
                if self.render:
                    ob.data.uv_layers.active.active_render = True
                if self.cloning:
                    ob.data.uv_layers.active.active_clone = True
            elif self.mode == "NAME":
                for uv_layer in ob.data.uv_layers:
                    if uv_layer.name == scene.uv_toolkit.uv_layer_name:
                        uv_layer.active = True
                        if self.render:
                            uv_layer.active_render = True
                        if self.cloning:
                            uv_layer.active_clone = True
                        break
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, "mode", expand=True)
        layout.prop(self, "render")
        layout.prop(self, "cloning")
