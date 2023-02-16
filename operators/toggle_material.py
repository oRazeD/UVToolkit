import bpy
import bmesh
from bpy.types import Operator


class ToggleMaterial(Operator):
    bl_idname = "uv.toolkit_toggle_material"
    bl_label = "Toggle Material"
    bl_description = "Toggles materials between initial and checker material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, 'No Objects Selected')
            return {'CANCELLED'}

        view_layer = context.view_layer
        act_ob = view_layer.objects.active
        selected_objectes = [ob for ob in context.selected_objects if ob.type == 'MESH']

        if selected_objectes:
            view_layer.objects.active = selected_objectes[0]

            initial_mode = context.active_object.mode
            if initial_mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')
            for ob in selected_objectes:
                if "uv_toolkit_checker_material" in ob:
                    material_index = ob.data.polygons[0].material_index
                    ob.active_material_index = material_index
                    material_slot_name = ob.material_slots[material_index].name
                    if material_slot_name.startswith("uv_checker_material"):
                        if "uv_toolkit_init_material" in ob:
                            init_material = bpy.data.materials.get(
                                ob["uv_toolkit_init_material"]
                            )
                            if init_material:
                                ob.active_material = init_material
                        else:
                            ob.active_material = None
                    else:
                        checker_material = bpy.data.materials.get(
                            ob["uv_toolkit_checker_material"]
                        )
                        if checker_material:
                            ob.active_material = checker_material
                if "uv_toolkit_multiple_materials" in ob:
                    me = ob.data
                    bm = bmesh.from_edit_mesh(me)
                    if ob["uv_toolkit_multiple_materials"]:
                        material_idx_layer = bm.faces.layers.int.get("material_idx_layer")
                        if material_idx_layer:
                            for f in bm.faces:
                                f.material_index = f[material_idx_layer]
                        ob["uv_toolkit_multiple_materials"] = 0
                    else:
                        for index, slot in enumerate(ob.material_slots):
                            if slot.material:
                                if slot.material.name.startswith("uv_checker_material"):
                                    break
                        ob.active_material_index = index
                        for f in bm.faces:
                            f.material_index = index
                        ob["uv_toolkit_multiple_materials"] = 1
                    bmesh.update_edit_mesh(me)
            bpy.ops.object.mode_set(mode=initial_mode)
            view_layer.objects.active = act_ob
        return{'FINISHED'}
