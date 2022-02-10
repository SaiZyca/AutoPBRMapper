import bpy
import os, json ,ntpath
from bpy_extras.io_utils import ExportHelper, ImportHelper
from . import actions


class AUTO_PBR_OT_export_material_data(bpy.types.Operator, ExportHelper):
    bl_idname = "material_tools.export_material_data"
    bl_label = "Export Material Mapping"
    bl_description = "Export Material Mapping data"

    filename_ext = ".json"

    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )  

    filepath = bpy.props.StringProperty(
        default="",
    )
    # type: bpy.props.EnumProperty(
    #     name="Example Enum",
    #     description="Choose between two items",
    #     items=(
    #         ('OPT_A', "First Option", "Description one"),
    #         ('OPT_B', "Second Option", "Description two"),
    #     ),
    #     default='OPT_A',
    # )

    def execute(self,context):
        objects = bpy.data.objects
        mat_dict = {}

        for obj in objects:
            material_slots = obj.material_slots
            if len(material_slots) > 0:
                materials = [material.name for material in material_slots]
                mat_dict[obj.name] = materials

        data_file = open(self.filepath, "w")
        json.dump(mat_dict, data_file, ensure_ascii=False, indent=4)
        data_file.close()
        context.scene.AUTOPBR_properties.material_data_file = self.filepath
        
        self.report({'INFO'}, str(mat_dict) )
        return {'FINISHED'}

class AUTO_PBR_OT_append_material(bpy.types.Operator, ImportHelper):
    bl_idname = "material_tools.append_material"
    bl_label = "Append Material"
    bl_description = "Export Material Mapping data"

    filename_ext = ".blend"

    filter_glob: bpy.props.StringProperty(
        default="*.blend",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )  

    filepath = bpy.props.StringProperty(
        default="",
    )

    def execute(self,context):
        self.load_material()
            # self.report({'INFO'}, str(data_to.materials))
        # self.report({'INFO'}, str(data_from) )
        return {'FINISHED'}

    def materials_dict(self):
        with bpy.data.libraries.load(self.filepath, link=False) as (data_from, data_to):
             for attr in dir(data_to.objects):
                self.report({'INFO'}, str(attr) )

    def load_material(self):
        scene_materials = bpy.data.materials
        with bpy.data.libraries.load(self.filepath, link=False) as (data_from, data_to):
            for material in data_from.materials:
                if material in scene_materials:
                    scene_materials.remove(scene_materials[material])
                    message = "Update material: %s from file" % (material)
                    self.report({'INFO'}, message )
                    
            data_to.materials = data_from.materials

        return {'FINISHED'}

class AUTO_PBR_OT_reassign_material(bpy.types.Operator):
    bl_idname = "material_tools.re_assign_material"
    bl_label = "Re assign material"
    bl_description = "re-assign material according to material json"

    def execute(self, context):
        fuzz_search = context.scene.AUTOPBR_properties.fuzzy_search

        if fuzz_search:
            self.fuzz_assign()
        else:
            self.precise_assign()
        
        return {'FINISHED'}

    def load_data(self):
        material_dict = {}
        file_path = bpy.context.scene.AUTOPBR_properties.material_data_file
        if os.path.exists(file_path):
            data_file = open(file_path, "r")
            material_dict = json.load(data_file)
            data_file.close()

        return material_dict

    def fuzz_assign(self):
        material_dict = self.load_data()
        objects = bpy.data.objects

        for obj in objects:
            for key in material_dict.keys():
                if obj.name.find(key) > -1:
                    obj.data.materials.clear()
                    materials_name = material_dict[key]
                    for name in materials_name:
                        material = bpy.data.materials[name]
                        obj.data.materials.append(material)

                    message = "Re-Assigned %s material" % (obj.name)
                    self.report({'INFO'}, (message) )

        return {'FINISHED'}

    def precise_assign(self):
        material_dict = self.load_data()
        objects = bpy.data.objects

        matched_objs = [obj for obj in objects if obj.name in material_dict]
        for obj in matched_objs:
            obj.data.materials.clear()
            materials_name = material_dict[obj.name]
            for name in materials_name:
                material = bpy.data.materials[name]
                obj.data.materials.append(material)
            
            message = "Re-Assigned %s material" % (obj.name)
            self.report({'INFO'}, (message) )

        return {'FINISHED'}


class MaterialTools_OT_assign_pbr_maps(bpy.types.Operator):
    bl_idname = "material_tools.assign_pbr_maps"
    bl_label = "Assign PBR Maps"
    bl_description = "auto assign pbr map form folder"

    def execute(self, context):
        mode = context.scene.AUTOPBR_properties.objects_collection
        materials = actions.datablock_collect_materials(mode)
        images = actions.datablock_collect_images(mode=mode)
        actions.datablock_op_remove_image(images=images)
        for material in materials:
            result = actions.assign_pbr_maps(material)
            message = "process material %s -- %s" % (material.name, result)
            self.report({'INFO'}, str(message) )
        # assign_pbr_map()

        return {'FINISHED'}
 
class MaterialTools_OT_copy_name(bpy.types.Operator):
    bl_idname = "material_tools.copy_name"
    bl_label = "Copy Name"
    bl_description = "Copy Name From Data"

    def execute(self, context):
        mode = bpy.context.scene.AUTOPBR_properties.objects_collection
        objects = actions.context_collect_objects(mode=mode, type='MESH')
        name_target = context.scene.AUTOPBR_properties.name_target
        name_from = context.scene.AUTOPBR_properties.name_from

        for obj in objects:
            data_dict = actions.get_name_dict(obj)
            # self.report({'INFO'}, str(data_dict) )
            if data_dict[name_from] and data_dict[name_target] is not None:
                data_dict[name_target].name = data_dict[name_from].name

        return {'FINISHED'}

class MaterialTools_OT_reset_material(bpy.types.Operator):
    bl_idname = "material_tools.reset_material"
    bl_label = "Reset Materials"
    bl_description = "Create new material for objects"

    def execute(self, context):
        mode = bpy.context.scene.AUTOPBR_properties.objects_collection
        objects = actions.context_collect_objects(mode=mode, type='MESH')
        materials = bpy.data.materials

        for obj in objects:
            if not bpy.data.materials.get(obj.name):
                material = bpy.data.materials.new(name=obj.name)
                obj.data.materials[0] = material
            else:
                obj.data.materials[0] = bpy.data.materials.get(obj.name)

        for material in bpy.data.materials:
            if material.users == 0:
                bpy.data.materials.remove(material)

        return {'FINISHED'}

class MaterialTools_OT_convert_texture(bpy.types.Operator):
    bl_idname = "material_tools.convert_texture"
    bl_label = "Convert Texture"
    bl_description = "Convert scene textures to other format"

    def execute(self, context):
        message = ""
        ratio = context.scene.AUTOPBR_properties.export_scale/100
        bpy.ops.file.make_paths_absolute()
        image_settings = context.scene.render.image_settings
        export_folder = context.scene.AUTOPBR_properties.exportfolder
        temp_file = context.scene.render.frame_path(frame=1)
        render_folder, export_file_extension = ntpath.splitext(temp_file)
        images = [image for image in bpy.data.images if image.name !="Render Result"]

        export_folder = bpy.path.abspath(export_folder)
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
        
        for image in images:
            file_folder, full_file_name = ntpath.split(image.filepath)
            file_name, file_extension = ntpath.splitext(full_file_name)
            new_file_path = "%s/%s%s" % (export_folder, file_name, export_file_extension)
            if ratio < 1:
                image.scale(image.size[0]*ratio, image.size[1]*ratio)
            image.save_render(filepath=new_file_path, scene = context.scene)

            # image.filepath_raw = new_file_path
            # message = "%s %s" % (image.name, new_file_path)
            # filename = ntpath.basename(image.filepath)
            # self.report({'INFO'}, str(message) )
        # bpy.ops.file.make_paths_relative()

        return {'FINISHED'}


class AutoPBRMapper_OT_Actions(bpy.types.Operator):
    """ Actions """
    bl_label ="AutoPBRMapper Operator"
    bl_idname = "autopbrmapper.actions"
    bl_options = {"REGISTER", "UNDO"}

    button : bpy.props.StringProperty(default="")
    texturepath : bpy.props.StringProperty(default="")

    def execute(self, context):
        button=self.button
        try:
            ## ObjectOperator
            if button=="AssignMaterial": 
                actions.assign_pbr_maps()
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
    AUTO_PBR_OT_export_material_data,
    AUTO_PBR_OT_reassign_material,
    MaterialTools_OT_assign_pbr_maps,
    AutoPBRMapper_OT_Actions,
    AUTO_PBR_OT_append_material,
    MaterialTools_OT_copy_name,
    MaterialTools_OT_reset_material,
    MaterialTools_OT_convert_texture,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
