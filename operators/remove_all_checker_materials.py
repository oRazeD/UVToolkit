import bpy
import bmesh


class RemoveAllCheckerMaterials(bpy.types.Operator):
    bl_idname = "uv.toolkit_remove_all_checker_materials"
    bl_label = "Remove All Checker Materials"
    bl_description = "Completely remove all checker materials and textures"
    bl_options = {'REGISTER', 'UNDO'}

    def remove_checker_material_slot(self, ob):
        for index, slot in enumerate(ob.material_slots):
            if slot.material \
            and slot.material.name.startswith("uv_checker_material"):
                ob.active_material_index = index
                break
        bpy.ops.object.material_slot_remove()

    def execute(self, context):
        mesh_objects = [ob for ob in bpy.data.objects if ob.type == 'MESH']
        objects_has_init_material = \
            [ob for ob in mesh_objects if "uv_toolkit_init_material" in ob]
        objects_has_checker_material = \
            [ob for ob in mesh_objects if "uv_toolkit_checker_material" in ob]
        objects_has_multiple_materials = []
        for ob in mesh_objects:
            if not "uv_toolkit_multiple_materials" in ob \
            or not bpy.ops.object.mode_set.poll():
                continue
            objects_has_multiple_materials.append(ob)

        for ob in objects_has_init_material:
            init_material_name = ob["uv_toolkit_init_material"]
            init_material = bpy.data.materials.get(init_material_name)
            if init_material:
                material_index = ob.data.polygons[0].material_index
                ob.active_material_index = material_index
                ob.active_material = init_material
            del(ob["uv_toolkit_init_material"])

        for ob in objects_has_checker_material:
            del(ob["uv_toolkit_checker_material"])

        if objects_has_multiple_materials:
            view_layer = context.view_layer
            initial_active_ob = view_layer.objects.active
            if initial_active_ob is None:
                view_layer.objects.active = objects_has_multiple_materials[0]
            initial_mode = context.active_object.mode
            bpy.ops.object.mode_set(mode='OBJECT')

            initial_selection = []
            for ob in context.selected_objects:
                if ob.type == 'MESH':
                    initial_selection.append(ob)
                    ob.select_set(False)
            for ob in objects_has_multiple_materials:
                ob.select_set(True)

            # Remove checker material slot
            for ob in objects_has_multiple_materials:
                view_layer.objects.active = ob
                self.remove_checker_material_slot(ob)

            bpy.ops.object.mode_set(mode='EDIT')
            # Restore initial material indices
            for ob in objects_has_multiple_materials:
                me = ob.data
                bm = bmesh.from_edit_mesh(me)

                material_idx_layer = bm.faces.layers.int.get("material_idx_layer")
                if material_idx_layer:
                    for f in bm.faces:
                        f.material_index = f[material_idx_layer]
                    bm.faces.layers.int.remove(material_idx_layer)
                    del(ob["uv_toolkit_multiple_materials"])
            # Restore initial selected objects
            bpy.ops.object.mode_set(mode='OBJECT')
            for ob in objects_has_multiple_materials:
                ob.select_set(False)
            for ob in initial_selection:
                ob.select_set(True)
            view_layer.objects.active = initial_active_ob
            bpy.ops.object.mode_set(mode=initial_mode)

        for image in bpy.data.images:
            if image.name.startswith("uv_checker_map"):
                bpy.data.images.remove(image)

        for mat in bpy.data.materials:
            if mat.name.startswith("uv_checker_material"):
                bpy.data.materials.remove(mat)
        return {'FINISHED'}
