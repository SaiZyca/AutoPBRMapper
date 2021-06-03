import bpy
from . import actions
import os, json



class MaterialTools_OT_exportMaterialData(bpy.types.Operator):
    bl_idname = "material_tools.export_material_data"
    bl_label = "Export material data"

    def execute(self,context):
        file_path = context.scene.AutoPBRMapper_setting.material_data_file
        objects = bpy.data.objects
        mat_dict = {}

        for obj in objects:
            material_slots = obj.material_slots
            if len(material_slots) > 0:
                materials = [material.name for material in material_slots]
                mat_dict[obj.name] = materials

        data_file = open(file_path, "w")
        json.dump(mat_dict, data_file, ensure_ascii=False, indent=4)
        data_file.close()
        
        self.report({'INFO'}, str(mat_dict) )
        return {'FINISHED'}
        

class MaterialTools_OT_reAssignMaterial(bpy.types.Operator):
    bl_idname = "material_tools.re_assign_material"
    bl_label = "Re assign material"

    def execute(self, context):
        material_dict = {}
        file_path = context.scene.AutoPBRMapper_setting.material_data_file
        objects = bpy.data.objects
        if os.path.exists(file_path):
            data_file = open(file_path, "r")
            material_dict = json.load(data_file)
            data_file.close()
        
        matched_objs = [obj for obj in objects if obj.name in material_dict]
        for obj in matched_objs:
            obj.data.materials.clear()
            materials_name = material_dict[obj.name]
            for name in materials_name:
                material = bpy.data.materials[name]
                obj.data.materials.append(material)

        return {'FINISHED'}


class MaterialTools_OT_assignPbrMaps(bpy.types.Operator):
    bl_idname = "material_tools.assign_bpr_maps"
    bl_label = "Assign PBR maps"

class AutoPBRMapper_OT_Actions(bpy.types.Operator):
    """ Actions """
    bl_label ="AutoPBRMapper Operator"
    bl_idname = "autopbrmapper.actions"
    bl_options = {"REGISTER", "UNDO"}

    button : bpy.props.StringProperty(default="")
    texturepath : bpy.props.StringProperty(default="")
    # texturepath : bpy.context.scene.AutoPBRMapper_setting.filepath

    def execute(self, context):
        button=self.button
        try:
            ## ObjectOperator
            if button=="AssignMaterial": 
                actions.assignMaterial()

            elif button == 'Apply Name':
                actions.data_rename()

            elif button == 'Find Replace':
                actions.find_replace()

            else:
                print ('Not defined !')
        except Exception as e:
            print ('Execute Error:',e)
        
        return {"FINISHED"}


classes = (
    MaterialTools_OT_exportMaterialData,
    MaterialTools_OT_reAssignMaterial,
    MaterialTools_OT_assignPbrMaps,
    AutoPBRMapper_OT_Actions,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
