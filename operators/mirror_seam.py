import bpy
from bpy.props import EnumProperty


class MirrorSeam(bpy.types.Operator):
    bl_idname = "uv.toolkit_mirror_seam"
    bl_label = "Mirror Seam"
    bl_description = "Mirror the selected edges and mark them with seams"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(
        name="Axis",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
        ],
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        mt_state = context.object.data.use_mirror_topology
        context.object.data.use_mirror_topology = False
        bpy.ops.mesh.select_mirror(axis={self.axis}, extend=True)
        context.object.data.use_mirror_topology = True
        bpy.ops.mesh.select_mirror(axis={self.axis}, extend=True)
        bpy.ops.mesh.mark_seam(clear=False)
        context.object.data.use_mirror_topology = mt_state
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(self, "axis", expand=True)
