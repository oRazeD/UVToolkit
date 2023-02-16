import bpy
from bpy.types import Operator
from bpy.props import StringProperty


class ExecuteCustomOp(Operator):
    bl_idname = "uv.toolkit_execute_custom_op"
    bl_label = "Execute Custom Operator"
    bl_description = ""
    bl_options = {'INTERNAL', 'REGISTER', 'UNDO'}

    exec_op: StringProperty(options={'HIDDEN'})

    def execute(self, context):
        exec(self.exec_op)
        return {'FINISHED'}
