import os
from collections import defaultdict

import bpy
import bmesh
from bpy.props import IntProperty, StringProperty

from ..functions import get_addon_preferences


class CheckerMaterial(bpy.types.Operator):
    bl_idname = "uv.toolkit_create_checker_material"
    bl_label = "Create Checker Material"
    bl_description = "Create and assign checker material for the selected objects"
    bl_options = {'REGISTER', 'INTERNAL', 'UNDO'}

    width: IntProperty(options={'HIDDEN'})
    height: IntProperty(options={'HIDDEN'})
    checker_image_path: StringProperty(options={'HIDDEN'})

    def get_uv_checker_map(self, _context):
        addon_prefs = get_addon_preferences()
        checker_type = addon_prefs.checker_type
        if addon_prefs.checker_map == "BUILT-IN":
            if checker_type in ('UV_GRID', 'COLOR_GRID'):
                img_size = f"{self.width}x{self.height}"
                checker_name = \
                    f"uv_checker_map_{str.lower(checker_type)}_{img_size}"
                if not bpy.data.images.get(checker_name):
                    bpy.ops.image.new(
                        name=checker_name,
                        width=self.width,
                        height=self.height,
                        generated_type=checker_type
                    )
        else:
            img_name = os.path.basename(self.checker_image_path)
            checker_name = f"uv_checker_map_custom_{img_name}"
            if len(checker_name) > 63:
                checker_name = checker_name[0:63]

            if bpy.data.images.get(checker_name) is None:
                img = bpy.data.images.load(self.checker_image_path)
                img.name = checker_name
        return bpy.data.images[checker_name]

    def get_uv_checker_material(self, _context, uv_checker_map):
        checker_name = uv_checker_map.name
        material_name = checker_name.replace("uv_checker_map",
                                             "uv_checker_material")
        if len(material_name) > 63:
            material_name = material_name[0:63]
        if bpy.data.materials.get(material_name) is None:
            mat = bpy.data.materials.new(material_name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.remove(nodes["Principled BSDF"])
            node_texture = nodes.new(type="ShaderNodeTexImage")
            node_texture.image = bpy.data.images[checker_name]
            node_texture.location = -20, 300
            links = mat.node_tree.links
            links.new(node_texture.outputs[0],
                      nodes.get("Material Output").inputs[0])
        return bpy.data.materials.get(material_name)

    def backup_active_material(self, context, ob, bm, multiple_materials):
        if multiple_materials:
            materials_faces = defaultdict(list)
            material_idx_layer = bm.faces.layers.int.get("material_idx_layer")
            if not material_idx_layer:
                material_idx_layer = bm.faces.layers.int.new("material_idx_layer")

            for f in bm.faces:
                materials_faces[f.material_index].append(f)

            for material_index in materials_faces:
                for f in materials_faces[material_index]:
                    f[material_idx_layer] = material_index
        else:
            if ob.material_slots:
                if ob.data.polygons:
                    material_index = ob.data.polygons[0].material_index
                    ob.active_material_index = material_index
                    material = ob.active_material
                    if material and not material.name.startswith("uv_checker_material"):
                        context.object.active_material.use_fake_user = True
                        ob["uv_toolkit_init_material"] = material.name

    def set_viewport_shading(self, context):
        workspace = context.workspace
        current_workspace = workspace.screens[0].areas
        for area in current_workspace:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if space.shading.type == 'WIREFRAME':
                        space.shading.type = 'SOLID'
                    space.shading.color_type = 'TEXTURE'

    def assign_image_in_uv_editor(self, context, uv_checker_map, addon_prefs):
        screen = context.screen
        for area in screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.spaces.active.image = uv_checker_map
                if addon_prefs.assign_image_in_uv_editor == 'DISABLE':
                    area.spaces.active.image = None

    def get_multiple_materials(self, _context, bm):
        if bm.faces:
            current_material_index = bm.faces[0].material_index
            for f in bm.faces:
                if f.material_index != current_material_index:
                    return True

    def assign_checker_material(self, context, ob, bm, uv_checker_map, multiple_materials):
        material = self.get_uv_checker_material(context, uv_checker_map)
        if "uv_toolkit_multiple_materials" in ob:
            for index, slot in enumerate(ob.material_slots):
                if slot.material:
                    if slot.material.name.startswith("uv_checker_material"):
                        break
            ob.active_material_index = index
            for f in bm.faces:
                f.material_index = index
            ob.active_material = material
            context.object.active_material.use_fake_user = True
            ob["uv_toolkit_multiple_materials"] = 1
            return

        if multiple_materials:
            # print("Multiple mats")
            bpy.ops.object.material_slot_add()
            index = ob.active_material_index
            for f in bm.faces:
                f.material_index = index
            ob["uv_toolkit_multiple_materials"] = 1
        else:
            # print("Single mat")
            if bm.faces:
                material_index = bm.faces[0].material_index
                ob.active_material_index = material_index
                ob["uv_toolkit_checker_material"] = material.name
        ob.active_material = material
        context.object.active_material.use_fake_user = True

    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, 'No Objects Selected')
            return {'CANCELLED'}
        addon_prefs = get_addon_preferences()
        uv_checker_map = self.get_uv_checker_map(context)

        self.set_viewport_shading(context)

        view_layer = context.view_layer
        act_ob = view_layer.objects.active
        selected_objectes = [ob for ob in context.selected_objects if ob.type == 'MESH']

        if selected_objectes:
            view_layer.objects.active = selected_objectes[0]

            initial_mode = context.active_object.mode
            if initial_mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')
            for ob in selected_objectes:
                view_layer.objects.active = ob
                me = ob.data
                bm = bmesh.from_edit_mesh(me)
                bm.faces.ensure_lookup_table()
                multiple_materials = self.get_multiple_materials(context, bm)

                self.backup_active_material(context, ob, bm, multiple_materials)
                self.assign_checker_material(context, ob, bm, uv_checker_map, multiple_materials)

            bpy.ops.object.mode_set(mode=initial_mode)
            view_layer.objects.active = act_ob
        self.assign_image_in_uv_editor(context, uv_checker_map, addon_prefs)
        return {'FINISHED'}
