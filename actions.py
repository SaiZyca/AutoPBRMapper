# coding=UTF-8

'''
2019/06/05 fix 2.8 api change
colorspace setting move to image node from shader node 
'''

import bpy
import os, ntpath
import re

from mathutils import Vector

def context_collect_objects(mode: str, type: str) -> list:
    ''' mode: "ALL/SELECTION"
        type: "MESH/CURVE/SURFACE/LIGHT...etc"
    '''
    objects = None

    if mode == 'ALL':
        objects = [obj for obj in bpy.context.scene.objects if obj.type == type]
    elif mode == 'SELECTION':
        objects = [obj for obj in bpy.context.selected_objects if obj.type == type]

    return objects

def datablock_op_remove_image(images: list) -> list: 
    '''remove image block, if None remove all image block
    '''
    [bpy.data.images.remove(image) for image in images]

    return bpy.data.images

def datablock_op_fix_image_name() -> list:
    '''force image block name as file name
    '''
    images = [image for image in bpy.data.images if image.name !="Render Result"]
    for image in images:
        image.name = ntpath.basename(image.filepath)

    images = [image for image in bpy.data.images if image.name !="Render Result"]
    return images 

def datablock_collect_materials(mode: str) -> list:
    '''mode: "ALL/SELECTION"
    '''
    objects = None
    materials = None

    if mode == 'ALL':
        materials = bpy.data.materials
    elif mode == 'SELECTION':
        objects = bpy.context.selected_objects
        materials = []
        for obj in objects:
            material_slots = obj.material_slots
            for slot in material_slots:
                if slot.material not in materials:
                    materials.append(slot.material)

    return materials

def datablock_collect_images(mode: str) -> list:
    '''mode: "ALL/SELECTION"
    '''
    images = []

    if mode == 'ALL':
        images = [image for image in bpy.data.images if image.name !="Render Result"]
    elif mode == 'SELECTION':
        materials = []
        objects = bpy.context.selected_objects
        for obj in objects:
            material_slots = obj.material_slots
            for slot in material_slots:
                if slot.material not in materials:
                    materials.append(slot.material)
        
        images = []
        for material in materials:
            node_images = [node.image for node in material.node_tree.nodes if node.type == 'TEX_IMAGE' and node.image is not None]
            [images.append(image) for image in node_images if image not in images]

    return images

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

def opacity_material(material):
    material.blend_method = "BLEND"

def not_opacity_material(material):
    material.blend_method = "OPAQUE"
    material.show_transparent_back = False

def hide_shader_scoket(shader_node, status=True):
    for input in shader_node.inputs:
        input.hide = status

def offset_node_loaction(origin, x_offset, y_offset):
    new_loaction = (origin.x + x_offset, origin.y + y_offset)
    return new_loaction

def assign_pbr_maps(material):
    # os.system('cls')
    autopbr_properties = bpy.context.scene.AUTOPBR_properties
    tex_folder = autopbr_properties.filepath
    ext = autopbr_properties.filename_ext
    prefix = autopbr_properties.prefix
    mMaterialtype = autopbr_properties.materialtype
    margin = 100

    base_color_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_basecolor + ext) 
    emission_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_emission + ext) 
    matellic_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_metallic + ext) 
    specular_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_specular + ext) 
    roughness_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_roughness + ext) 
    opacity_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_opacity + ext) 
    height_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_height + ext) 
    normal_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_normal + ext)
    displace_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_displace + ext) 
    refraction_filepath = (tex_folder + '/' + prefix + material.name + autopbr_properties.suffix_refraction + ext) 

    if material.use_nodes is not True:
        material.use_nodes = True

    mat_nodes = material.node_tree.nodes
    mat_links = material.node_tree.links

    # inital shader display
    material.blend_method = "OPAQUE"
    material.show_transparent_back = False

    # inital shader node tree
    mat_nodes.clear() 
    output_shader = mat_nodes.new("ShaderNodeOutputMaterial")
    main_shader = mat_nodes.new("ShaderNodeBsdfPrincipled")
    main_shader.location = offset_node_loaction(output_shader.location, -500, -150)
    hide_shader_scoket(main_shader)

    if mMaterialtype == 'Mix':
        material.blend_method = "OPAQUE"
        mix = mat_nodes.new("ShaderNodeMixShader")
        mix.location = offset_node_loaction(output_shader.location, -200, 0)
        mix.inputs[0].default_value = 1
        glass_shader = mat_nodes.new("ShaderNodeBsdfPrincipled")
        glass_shader.label = "Glass Shader"
        glass_shader.location = offset_node_loaction(mix.location, -300, -20)
        glass_shader.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1)
        glass_shader.inputs['Roughness'].default_value = 0.16
        glass_shader.inputs['Transmission'].default_value = 0.9
        glass_shader.inputs['IOR'].default_value = 1.01
        glass_shader.inputs['Alpha'].default_value = 0.8
        mat_links.new(mix.outputs["Shader"], output_shader.inputs["Surface"])
        mat_links.new(glass_shader.outputs["BSDF"], mix.inputs[1])
        mat_links.new(main_shader.outputs["BSDF"], mix.inputs[2])
        hide_shader_scoket(glass_shader)

    elif mMaterialtype == 'Principle' :
        material.blend_method = "CLIP"
        mat_links.new(main_shader.outputs["BSDF"], output_shader.inputs["Surface"])

    if os.path.isfile(bpy.path.abspath(displace_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(displace_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = offset_node_loaction(output_shader.location, -200, -200)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], output_shader.inputs["Displacement"])

    if os.path.isfile(bpy.path.abspath(base_color_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(base_color_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = offset_node_loaction(main_shader.location, -300, -50)
        filename, file_extension = os.path.splitext(base_color_filepath)
        if file_extension == 'exr':
            image_node.image.colorspace_settings.name = 'Linear'
        else:
            image_node.image.colorspace_settings.name = 'sRGB'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Base Color"])
 
    if os.path.isfile(bpy.path.abspath(emission_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(emission_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = offset_node_loaction(main_shader.location, -350, -330)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Emission"])

    if os.path.isfile(bpy.path.abspath(matellic_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(matellic_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = offset_node_loaction(main_shader.location, -600, -50)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Metallic"])

    if os.path.isfile(bpy.path.abspath(specular_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(specular_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = offset_node_loaction(main_shader.location, -900, -50)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Specular"])

    if os.path.isfile(bpy.path.abspath(roughness_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(roughness_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = offset_node_loaction(main_shader.location, -1200, -50)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], main_shader.inputs["Roughness"])

    if os.path.isfile(bpy.path.abspath(opacity_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(opacity_filepath, check_existing=True)
        image_node.hide = True
        image_node.image.colorspace_settings.name = 'Linear'

        if mMaterialtype == 'Mix':
            invert_node = mat_nodes.new("ShaderNodeInvert")
            invert_node.location = offset_node_loaction(mix.location, -300, 100)
            invert_node.inputs['Fac'].default_value = 0
            image_node.location = offset_node_loaction(invert_node.location, -300, -80)
            mat_links.new(image_node.outputs["Color"], invert_node.inputs["Color"])
            mat_links.new(invert_node.outputs["Color"], mix.inputs[0])
            material.blend_method = "BLEND"
        elif mMaterialtype == 'Principle':
            image_node.location = offset_node_loaction(main_shader.location, -350, -450)
            mat_links.new(image_node.outputs["Color"], main_shader.inputs['Alpha'])

    if os.path.isfile(bpy.path.abspath(refraction_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(refraction_filepath, check_existing=True)
        image_node.hide = True
        image_node.image.colorspace_settings.name = 'Linear'

        if mMaterialtype == 'Mix':
            image_node.location = offset_node_loaction(glass_shader.location, -300, -80)
            mat_links.new(image_node.outputs["Color"], glass_shader.inputs['Transmission'])
            material.blend_method = "BLEND"
        elif mMaterialtype == 'Principle':
            image_node.location = offset_node_loaction(main_shader.location, -350, -450)
            mat_links.new(image_node.outputs["Color"], main_shader.inputs['Transmission'])

    bump_node = mat_nodes.new("ShaderNodeBump")
    bump_node.inputs['Distance'].default_value = 0.1
    bump_node.location = offset_node_loaction(main_shader.location, -550, -240)
    mat_links.new(bump_node.outputs["Normal"], main_shader.inputs["Normal"])

    if os.path.isfile(bpy.path.abspath(height_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(height_filepath, check_existing=True)
        image_node.hide = True
        image_node.location = offset_node_loaction(bump_node.location, -280, -210)
        image_node.image.colorspace_settings.name = 'Linear'
        mat_links.new(image_node.outputs["Color"], bump_node.inputs["Height"])

    if os.path.isfile(bpy.path.abspath(normal_filepath)):
        image_node = mat_nodes.new("ShaderNodeTexImage")
        image_node.image = bpy.data.images.load(normal_filepath, check_existing=True)
        image_node.hide = True
        image_node.image.colorspace_settings.name = 'Linear'

        normal_map = mat_nodes.new("ShaderNodeNormalMap")
        normal_map.location = (-1 * 5 * (normal_map.width + margin), -400)
        
        mat_links.new(normal_map.outputs["Normal"], bump_node.inputs["Normal"])

        filp_normal_map = autopbr_properties.filp_normal_map
        channel_dict = {0:'R',1:"G",2:"B"}
        if True not in filp_normal_map:
            image_node.location = offset_node_loaction(normal_map.location, -400, -120)
            mat_links.new(image_node.outputs["Color"], normal_map.inputs["Color"])
        else:
            combin_node = mat_nodes.new("ShaderNodeCombineRGB")
            combin_node.location = offset_node_loaction(normal_map.location, -200, 0)
            mat_links.new(combin_node.outputs["Image"], normal_map.inputs["Color"])
            spearate_node = mat_nodes.new("ShaderNodeSeparateRGB")
            spearate_node.location = offset_node_loaction(normal_map.location, -600, 0)
            image_node.location = offset_node_loaction(normal_map.location, -900, 0)
            mat_links.new(image_node.outputs["Color"], spearate_node.inputs["Image"])
            for index in range(0, 3):
                if filp_normal_map[index]:
                    invert_node = mat_nodes.new("ShaderNodeInvert")
                    invert_node.hide = True
                    y_offset = 110*index
                    invert_node.location = offset_node_loaction(normal_map.location, -400, 50-y_offset)
                    invert_node.label = "Invert %s" % (channel_dict[index])
                    mat_links.new(spearate_node.outputs[index], invert_node.inputs["Color"])
                    mat_links.new(invert_node.outputs["Color"], combin_node.inputs[index])
                else:
                    mat_links.new(spearate_node.outputs[index], combin_node.inputs[index])
                    
    for node in material.node_tree.nodes:
        node.select = False

    return {'FINISH'}
#   



def check_pbr_map(file_path):
    pass

def create_materials_keeper():
    activate_object = bpy.context.object
    if bpy.data.objects.get('_all_material_keeper'):
        material_keeper = bpy.data.objects['_all_material_keeper']
    else:
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.object.name = '_all_material_keeper'
        material_keeper = bpy.data.objects['_all_material_keeper']
    
    if bpy.context.collection.objects.get('_all_material_keeper'):
        pass
    else:
        bpy.context.collection.objects.link(material_keeper)
        
    material_keeper.data.materials.clear()
    
    for material in bpy.data.materials:
        if not material.grease_pencil:
            material_keeper.data.materials.append(material)
    
    material_keeper.select_set(False)
    material_keeper.hide_select = True
    material_keeper.hide_viewport = True
    material_keeper.hide_render = True


    
    # bpy.context.view_layer.objects.active = activate_object

def remove_materials_keeper():
    if bpy.data.objects.get('_all_material_keeper'):
        material_keeper = bpy.data.objects['_all_material_keeper']
        bpy.data.objects.remove(material_keeper, do_unlink=True)