# coding=UTF-8

'''
2019/06/05 fix 2.8 api change
colorspace setting move to image node from shader node 
'''

import bpy
import os
import re

def get_objects():
    objects = None
    value = bpy.context.scene.AUTOPBR_properties.objects_collection
    if value == 'ALL':
        objects = bpy.context.scene.objects
    elif value == 'SELECTION':
        objects = bpy.context.selected_objects
    
    return objects

def get_name_dict(obj):
    data_dict = {}
    data_dict['OBJECT'] = obj
    data_dict['DATA'] = obj.data
    data_dict['MATERIAL'] = None

    if len(obj.material_slots) > 0:
        if obj.material_slots[0].material:
            data_dict['MATERIAL'] = obj.material_slots[0].material

    return data_dict

def find_replace():
    objects = get_objects()
    name_target = bpy.context.scene.AUTOPBR_properties.name_target
    string_find = bpy.context.scene.AUTOPBR_properties.string_find
    string_replace = bpy.context.scene.AUTOPBR_properties.string_replace
    case_sensitive = bpy.context.scene.AUTOPBR_properties.case_sensitive

    for obj in objects:
        data_dict = get_name_dict(obj)
        if case_sensitive:
            new_name = data_dict[name_target].name.replace(string_find, string_replace)
            data_dict[name_target].name = new_name
        else:
            new_name = re.compile(re.escape(string_find), re.IGNORECASE)
            new_name = new_name.sub(string_replace, data_dict[name_target].name)
            # print (new_name)
            data_dict[name_target].name = new_name

def data_rename():
    objects = get_objects()
    name_target = bpy.context.scene.AUTOPBR_properties.name_target
    name_from = bpy.context.scene.AUTOPBR_properties.name_from
    
    for obj in objects:
        data_dict = get_name_dict(obj)
        print (data_dict)
        if data_dict[name_from] and data_dict[name_target] is not None:
            data_dict[name_target].name = data_dict[name_from].name


def get_preferences():
    name = get_addon_name()
    return bpy.context.user_preferences.addons[name].preferences

def get_addon_name():
    return os.path.basename(os.path.dirname(os.path.realpath(__file__)))

def assign_pbr_maps(material):
    # os.system('cls')
    autopbr_properties = bpy.context.scene.AUTOPBR_properties
    tex_folder = autopbr_properties.filepath
    ext = autopbr_properties.filename_ext
    prefix = autopbr_properties.prefix
    mMaterialtype = autopbr_properties.materialtype
    margin = 100

    base_color_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_basecolor + ext) 
    matellic_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_metallic + ext) 
    specular_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_specular + ext) 
    roughness_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_roughness + ext) 
    opacity_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_opacity + ext) 
    normal_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_normal + ext)  

    if material.use_nodes is not True:
        material.use_nodes = True

    mat_nodes = material.node_tree.nodes
    mat_links = material.node_tree.links

    # inital shader
    material.blend_method = "OPAQUE"
    mat_nodes.clear() 
    output_shader = mat_nodes.new("ShaderNodeOutputMaterial")
    mix = mat_nodes.new("ShaderNodeMixShader")
    mix.location = (-1 * (mix.width + margin), 150)
    mix.inputs[0].default_value = 1
    transparent = mat_nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (-1 * 2 *(transparent.width + margin), 150)
    main_shader = mat_nodes.new("ShaderNodeBsdfPrincipled")
    main_shader.location = (-1 * 2 * (main_shader.width + margin), 0)

    if mMaterialtype == 'Principle':
        mat_links.new(mix.outputs["Shader"], output_shader.inputs["Surface"])
        mat_links.new(transparent.outputs["BSDF"], mix.inputs[1])
        mat_links.new(main_shader.outputs["BSDF"], mix.inputs[2])
    elif mMaterialtype == 'gltf' :
        mat_links.new(main_shader.outputs["BSDF"], output_shader.inputs["Surface"])

    # print (bpy.path.abspath(base_color_filepath))

    if os.path.isfile(bpy.path.abspath(base_color_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(base_color_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = (-1 * 3 * (image_node.width + margin), 0)
        image_node.image.colorspace_settings.name = 'sRGB'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Base Color"])
 
    if os.path.isfile(bpy.path.abspath(matellic_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(matellic_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = (-1 * 4 * (image_node.width + margin), 0)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Metallic"])

    if os.path.isfile(bpy.path.abspath(specular_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(specular_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = (-1 * 5 * (image_node.width + margin), 0)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Specular"])

    if os.path.isfile(bpy.path.abspath(roughness_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(roughness_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = (-1 * 6 * (image_node.width + margin), 0)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Roughness"])

    if os.path.isfile(bpy.path.abspath(opacity_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(opacity_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = (-1 * 7 * (image_node.width + margin), 0)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], mix.inputs[0])
        material.blend_method = "BLEND"

        

    if os.path.isfile(bpy.path.abspath(normal_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(normal_filepath, check_existing=True)
        image_node.hide = True
        image_node.image.colorspace_settings.name = 'Linear'
        bump = mat_nodes.new("ShaderNodeBump")
        bump.location = (-1 * 4 * (bump.width + margin), -400)
        normal_map = mat_nodes.new("ShaderNodeNormalMap")
        normal_map.location = (-1 * 5 * (normal_map.width + margin), -400)


        if mMaterialtype == 'Principle':
            image_node.location = (-1 * 7 * (image_node.width + margin), -400)
            mat_links.new(bump.outputs["Normal"], main_shader.inputs["Normal"])
            mat_links.new(normal_map.outputs["Normal"], bump.inputs["Normal"])
            combin = mat_nodes.new("ShaderNodeCombineRGB")
            combin.location = (-1 * 6 * (combin.width + margin), -400)
            invert = mat_nodes.new("ShaderNodeInvert")
            invert.location = (-1 * 7 *(invert.width + margin), -400)
            sp = mat_nodes.new("ShaderNodeSeparateRGB")
            sp.location = (-1 * 8 * (sp.width + margin), -400)
            mat_links.new(combin.outputs["Image"], normal_map.inputs["Color"])
            mat_links.new(sp.outputs["R"], combin.inputs["R"])
            mat_links.new(sp.outputs["B"], combin.inputs["B"])
            mat_links.new(sp.outputs["G"], invert.inputs["Color"])
            mat_links.new(invert.outputs["Color"], combin.inputs["G"])
            mat_links.new(image_node.outputs["Color"], sp.inputs["Image"])

        elif mMaterialtype == 'gltf' :
            image_node.location = (-1 * 5 * (image_node.width + margin), -400)
            mat_links.new(bump.outputs["Normal"], main_shader.inputs["Normal"])
            mat_links.new(normal_map.outputs["Normal"], bump.inputs["Normal"])
            mat_links.new(image_node.outputs["Color"], normal_map.inputs["Color"])     

#

def collect_materials(type):
    if type == 'All':
        materials = bpy.data.materials
    elif type == 'Selected':
        selectedObjects = bpy.context.selected_objects
        materials = []
        for object in selectedObjects:
            material_slots = object.material_slots
            for slot in material_slots:
                materials.append(slot.material)

    return materials


def check_pbr_map(file_path):
    pass