import random
import numpy as np
from math import radians

import bmesh
from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    FloatProperty,
    IntProperty
)

from ..utils.uv_utils import (
    universal_rotation_matrix,
    scale_matrix,
    translate_matrix,
    get_objects_seams,
    get_islands,
    get_bbox,
    calc_bbox_center,
)


class RandomizeIslands(Operator):
    bl_idname = "uv.toolkit_randomize_islands"
    bl_label = "Randomize Islands"
    bl_description = "Randomize uv islands position, scale, or rotation"
    bl_options = {'REGISTER', 'UNDO'}

    seed: IntProperty(
        name="Random Seed",
        default=0
    )
    translate_limit: FloatProperty(
        name="Distance limit",
        default=0,
        step=0.1,
        precision=3,
        min=0,
        max=30
    )
    translate_u: BoolProperty(
        name="X",
        default=True
    )
    translate_v: BoolProperty(
        name="Y",
        default=True
    )
    angle_limit: FloatProperty(
        name="Angle limit",
        description="Set threshold for max and min angle",
        default=0,
        step=0.1,
        precision=1,
        min=0,
        max=360
    )
    cw: BoolProperty(
        name="CW",
        default=True
    )
    ccw: BoolProperty(
        name="CCW",
        default=True
    )
    scale_limit: FloatProperty(
        name="Scale limit",
        description="Set the scaling limit",
        default=0,
        step=0.1,
        precision=3,
        min=0
    )
    scale_uniform: BoolProperty(
        name="Uniform",
        default=True
    )
    scale_u: BoolProperty(
        name="X",
        default=False
    )
    scale_u: BoolProperty(
        name="X",
        default=False
    )
    scale_v: BoolProperty(
        name="Y",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}

        random.seed(self.seed)

        objects_seams = get_objects_seams(context)
        translate_limit = self.translate_limit
        angle_limit = self.angle_limit
        scale_limit = self.scale_limit

        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                bbox = get_bbox(uv, island)
                bbox_center = calc_bbox_center(bbox)

                distance_u = random.uniform(-translate_limit, translate_limit) if self.translate_u else 0
                distance_v = random.uniform(-translate_limit, translate_limit) if self.translate_v else 0
                translate = translate_matrix(distance_u, distance_v)

                if self.cw and self.ccw:
                    angle = random.uniform(-angle_limit, angle_limit)
                elif self.cw:
                    angle = random.uniform(-angle_limit, 0)
                elif self.ccw:
                    angle = random.uniform(0, angle_limit)
                else:
                    angle = 0
                rotate = universal_rotation_matrix(context, radians(angle), bbox_center)

                scale_factor = 1 + random.uniform(-scale_limit, scale_limit) if (self.scale_uniform or self.scale_u or self.scale_v) else 1
                scale_u = scale_factor if self.scale_uniform or self.scale_u else 1
                scale_v = scale_factor if self.scale_uniform or self.scale_v else 1
                scale = scale_matrix((scale_u, scale_v), bbox_center)

                rotate_scale = np.dot(rotate, scale)
                convolution = np.dot(translate, rotate_scale)

                for f in island:
                    for l in f.loops:
                        u, v = l[uv].uv
                        l[uv].uv = convolution.dot(np.array([u, v, 1]))[:2]
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, "seed")
        layout.label(text="Translate")
        layout.prop(self, "translate_limit")
        layout.prop(self, "translate_u")
        layout.prop(self, "translate_v")
        layout.label(text="Rotate")
        layout.prop(self, "angle_limit")
        layout.prop(self, "cw")
        layout.prop(self, "ccw")
        layout.label(text="Scale")
        layout.prop(self, "scale_limit")
        layout.prop(self, "scale_uniform")
        layout.prop(self, "scale_u")
        layout.prop(self, "scale_v")
