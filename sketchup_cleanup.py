bl_info = {
    "name": "SketchUp Cleanup",
    "author": "NXSXTYNATE",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Tools Tab",
    "description": "Cleans up imported SketchUp files: clears parents, deletes empties, and moves objects to a new collection",
    "category": "Object",
}

import bpy

# ------------------------------
# Core Function
# ------------------------------
def sketchup_cleanup():
    # 1. Select all
    bpy.ops.object.select_all(action='SELECT')

    # 2. Clear parent (keep transforms)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    # 3. Select and delete all empties
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.view_layer.objects:
        if obj.type == 'EMPTY':
            obj.select_set(True)
    bpy.ops.object.delete()

    # 4. Move remaining objects to new collection
    bpy.ops.object.select_all(action='SELECT')

    # Center pivot points on objects.
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

    # Create new collection if it doesn't exist
    collection_name = "CleanUp"
    if collection_name not in bpy.data.collections:
        new_col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_col)
    else:
        new_col = bpy.data.collections[collection_name]

    for obj in bpy.context.selected_objects:
        for col in obj.users_collection:
            col.objects.unlink(obj)
        new_col.objects.link(obj)

# ------------------------------
# Operator Class
# ------------------------------
class OBJECT_OT_sketchup_cleanup_operator(bpy.types.Operator):
    bl_idname = "object.sketchup_cleanup"
    bl_label = "SketchUp Cleanup"
    bl_description = "Cleans up scene: clears parents, deletes empties, moves to collection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sketchup_cleanup()
        return {'FINISHED'}

# ------------------------------
# Panel Class
# ------------------------------
class VIEW3D_PT_sketchup_cleanup_panel(bpy.types.Panel):
    bl_label = "SketchUp Cleanup"
    bl_idname = "VIEW3D_PT_sketchup_cleanup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NXSTY-Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.sketchup_cleanup", icon="TRASH")

# ------------------------------
# Registration
# ------------------------------
classes = [
    OBJECT_OT_sketchup_cleanup_operator,
    VIEW3D_PT_sketchup_cleanup_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

# Prevent duplicate buttons
if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
