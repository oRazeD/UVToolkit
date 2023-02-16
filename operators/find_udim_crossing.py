import bmesh
from bpy.types import Operator

from ..utils.uv_utils import (
    get_bbox,
    get_udim_co,
    get_objects_seams,
    get_islands,
    deselect_all_loops_uv,
    select_all_faces,
)


class FindUdimCrossing(Operator):
    bl_idname = "uv.toolkit_find_udim_crossing"
    bl_label = "Find UDIM crossing"
    bl_description = "Find islands that cross the borders of UDIM"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        scene = context.scene
        if scene.tool_settings.use_uv_select_sync:
            self.report({'INFO'}, "Need to disable UV Sync")
            return {'CANCELLED'}


        tool_settings = context.tool_settings

        uv_sync_status = tool_settings.use_uv_select_sync
        current_uv_select_mode = scene.tool_settings.uv_select_mode

        if uv_sync_status:
            tool_settings.use_uv_select_sync = False


        islands_count = 0

        objects_seams = get_objects_seams(context)
        for ob in context.objects_in_mode_unique_data:
            seams = objects_seams[ob]
            me = ob.data
            bm = bmesh.from_edit_mesh(me)
            uv = bm.loops.layers.uv.verify()

            deselect_all_loops_uv(uv, bm)

            if uv_sync_status:
                select_all_faces(bm)

            for island in get_islands(uv, bm, seams):
                bbox = get_bbox(uv, island)
                bbox_u1, bbox_v1 = bbox[0][0], bbox[0][1]
                bbox_u2, bbox_v2 = bbox[1][0], bbox[1][1]

                for f in island:
                    for l in f.loops:
                        uv_vert_co = l[uv].uv
                        break

                udim_co = get_udim_co(uv_vert_co)
                udim_u1, udim_v1 = udim_co[0][0], udim_co[0][1]
                udim_u2, udim_v2 = udim_co[1][0], udim_co[1][1]

                if bbox_u1 < udim_u1 or bbox_v1 < udim_v1 \
                        or bbox_u2 > udim_u2 or bbox_v2 > udim_v2:

                    for f in island:
                        for l in f.loops:
                            l[uv].select = True
                    islands_count += 1

            bmesh.update_edit_mesh(me)

        if islands_count:
            scene.tool_settings.uv_select_mode = 'VERTEX'

            if islands_count == 1:
                island = "Island"
            else:
                island = "Islands"
            message = f"{str(islands_count)} {island} found"
            self.report({'WARNING'}, message)

            scene.tool_settings.uv_select_mode = current_uv_select_mode
        return {'FINISHED'}
