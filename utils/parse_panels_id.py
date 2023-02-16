import os

panel_path = os.path.split(__file__)[0][:-5] + "ui/panel.py"

with open(panel_path, 'r', encoding='utf-8') as file:
    for line in file:
        if 'bl_idname' in line:
            panel_id = line.split('"')[-2]
            print(f'"{panel_id}",')
