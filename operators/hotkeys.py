import bpy


class Hotkeys(bpy.types.Operator):
    bl_idname = "uv.toolkit_hotkeys"
    bl_label = "Hotkeys"
    bl_description = "List of hotkeys"
    bl_options = {'REGISTER'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=330)

    def draw(self, context):
        layout = self.layout
        layout = layout.box()
        col = layout.column()
        row = col.row(align=True)
        row.label(text="UV Editor Pie")
        row.label(text="Shift+F")
        row = col.row(align=True)
        row.label(text="3D View Pie")
        row.label(text="Shift+F")
        row = col.row(align=True)
        row.label(text="Unwrap the selected faces")
        row.label(text="Shift+E")
        row = col.row(align=True)
        row.label(text="Straighten UVs")
        row.label(text="Shift+Q")
        row = col.row(align=True)
        row.label(text="Distribute")
        row.label(text="D")
        row = col.row(align=True)
        row.label(text="Center Cursor and Frame All")
        row.label(text="Shift+C")
        row = col.row(align=True)
        row.label(text="Move Island")
        row.label(text="F")
        row = col.row(align=True)
        row.label(text="Invert Selection")
        row.label(text="Ctrl+Shift+I")
        row = col.row(align=True)
        row.label(text="Scale Individual Origins")
        row.label(text="Alt+S")
