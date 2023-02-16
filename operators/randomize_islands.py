import random
import numpy as np
from math import radians

import bmesh
from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    FloatProperty
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

    tranlate_limit: FloatProperty(
        name="Distance limit",
        default=0,
        step=0.1,
        precision=3,
        min=0,
        max=30
    )
    tranlate_u: BoolProperty(
        name="X",
        default=True
    )
    tranlate_v: BoolProperty(
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

        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            for island in get_islands(uv, bm, seams, has_selected_faces=True, islands_with_hidden_faces=False):
                bbox = get_bbox(uv, island)
                bbox_center = calc_bbox_center(bbox)

                distance_u, distance_v = 0, 0
                if self.tranlate_u or self.tranlate_v:
                    distance = random.uniform(
                        self.tranlate_limit * -1, self.tranlate_limit)
                    if self.tranlate_u:
                        distance_u = distance
                    if self.tranlate_v:
                        distance_v = distance
                tranlate = translate_matrix(distance_u, distance_v)

                angle = 0
                if self.cw and self.ccw:
                    angle = random.uniform(
                        self.angle_limit * -1, self.angle_limit)
                if self.cw and not self.ccw:
                    angle = random.uniform(self.angle_limit * -1, 0)
                if self.ccw and not self.cw:
                    angle = random.uniform(0, self.angle_limit)
                rotate = universal_rotation_matrix(context, radians(angle), bbox_center)

                scale_u, scale_v = 1, 1
                if self.scale_uniform or self.scale_u or self.scale_v:
                    scale_factor = 1 + random.uniform(
                        self.scale_limit * -1, self.scale_limit)
                    if self.scale_uniform:
                        scale_u = scale_factor
                        scale_v = scale_factor
                    if self.scale_u:
                        scale_u = scale_factor
                    if self.scale_v:
                        scale_v = scale_factor
                scale = scale_matrix((scale_u, scale_v), bbox_center)

                rotate_scale = np.dot(rotate, scale)
                convolution = np.dot(tranlate, rotate_scale)

                for f in island:
                    for l in f.loops:
                        u, v = l[uv].uv
                        l[uv].uv = convolution.dot(np.array([u, v, 1]))[:2]
            bmesh.update_edit_mesh(me)
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.label(text="Translate")
        layout.prop(self, "tranlate_limit")
        layout.prop(self, "tranlate_u")
        layout.prop(self, "tranlate_v")
        layout.label(text="Rotate")
        layout.prop(self, "angle_limit")
        layout.prop(self, "cw")
        layout.prop(self, "ccw")
        layout.label(text="Scale")
        layout.prop(self, "scale_limit")
        layout.prop(self, "scale_uniform")
        layout.prop(self, "scale_u")
        layout.prop(self, "scale_v")
