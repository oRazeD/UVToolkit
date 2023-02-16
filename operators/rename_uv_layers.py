from bpy.types import Operator


class RenameUvLayers(Operator):
    bl_idname = "uv.toolkit_rename_uv_layers"
    bl_label = "Batch Rename"
    bl_description = "Batch rename UV Sets"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        for ob in context.selected_objects:
            if ob.type == "MESH":
                current_layer = ob.data.uv_layers.active_index
                ob.data.uv_layers.active_index = scene.uv_toolkit.uv_layer_index - 1
                ob.data.uv_layers.active.name = scene.uv_toolkit.uv_layer_name
                ob.data.uv_layers.active_index = current_layer
        return {'FINISHED'}
