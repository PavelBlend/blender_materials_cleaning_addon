
bl_info = {
    'name': 'Materials Cleaning',
    'author': 'Pavel_Blend',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'location': 'Properties > Material',
    'category': 'Material'
    }


import bpy


def get_unused_materials(ob, me):
    used_material_indices = set()
    for polygon in me.polygons:
        used_material_indices.add(polygon.material_index)
    used_material_indices = list(used_material_indices)
    used_material_indices.sort()

    unused_material_indices = set()
    for mat_slot_index, mat_slot in enumerate(ob.material_slots):
        if mat_slot_index not in used_material_indices:
            unused_material_indices.add(mat_slot_index)
    unused_material_count = len(unused_material_indices)

    return unused_material_indices, unused_material_count


class MaterialsCleaningOp(bpy.types.Operator):
    bl_idname = 'material.materials_cleaning'
    bl_label = 'Materials Cleaning'
    bl_options = {'REGISTER', 'UNDO'}

    use_fake_user = bpy.props.BoolProperty(name='Use Fake User', default=False)

    def execute(self, context):
        ob = context.object
        me = ob.data
        unused_mat_indices, unused_mat_count = get_unused_materials(ob, me)

        for _ in range(unused_mat_count):
            unused_mat_indices, unused_mat_count = get_unused_materials(ob, me)
            for mat_slot_index in range(len(ob.material_slots)):
                if mat_slot_index in unused_mat_indices:
                    ob.active_material_index = mat_slot_index
                    material = ob.material_slots[mat_slot_index].material
                    bpy.ops.object.material_slot_remove()
                    if material.users == 0:
                        material.use_fake_user = self.use_fake_user
                    break

        return {'FINISHED'}


class MaterialsCleaningPanel(bpy.types.Panel):
    bl_label = "Materials Cleaning"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return (len(ob.material_slots) > 0 and ob.mode == 'OBJECT')

    def draw(self, context):
        layout = self.layout
        layout.operator('material.materials_cleaning')


def register():
    bpy.utils.register_class(MaterialsCleaningOp)
    bpy.utils.register_class(MaterialsCleaningPanel)


def unregister():
    bpy.utils.unregister_class(MaterialsCleaningPanel)
    bpy.utils.unregister_class(MaterialsCleaningOp)
