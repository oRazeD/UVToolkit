# import bmesh
from bpy.types import Operator

from ..utils.uv_utils import (
    debug_time,
)


@debug_time
def test(operator, context):
    print('>>>')


class TestOp(Operator):
    bl_idname = "uv.toolkit_test_op"
    bl_label = "Test Operator"
    bl_description = ""
    bl_options = {'INTERNAL', 'UNDO'}

    def execute(self, context):
        test(self, context)
        return {'FINISHED'}
