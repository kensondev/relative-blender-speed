import bpy, math
from mathutils import Vector
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='STUDIO'; sc.display.shading.color_type='OBJECT'
sc.display.shading.show_cavity=True
sc.frame_set(200)
cd=bpy.data.cameras.new("Over"); c=bpy.data.objects.new("Over",cd); sc.collection.objects.link(c)
c.location=(9, 505, 5); t=Vector((0,528,0)); c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler(); cd.lens=24
sc.camera=c
for o in bpy.data.objects:
    if o.type=='FONT': o.hide_render=True
sc.render.filepath='//wip/wip_viewport.png'; sc.render.resolution_percentage=100
bpy.ops.render.render(write_still=True)
