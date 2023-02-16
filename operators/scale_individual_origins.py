import bpy


class ScaleIndividualOrigins(bpy.types.Operator):
    bl_idname = "uv.toolkit_scale_individual_origins"
    bl_label = "Scale Individual Origins"
    bl_description = "Scale individual origins"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        space_data = context.space_data

        current_pivot_point = space_data.pivot_point
        space_data.pivot_point = 'INDIVIDUAL_ORIGINS'
        bpy.ops.transform.resize('INVOKE_DEFAULT')

        space_data.pivot_point = current_pivot_point
        return {'FINISHED'}
