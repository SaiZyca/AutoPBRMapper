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
    value = bpy.context.scene.AutoPBRMapper_setting.objects_collection
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
    name_target = bpy.context.scene.AutoPBRMapper_setting.name_target
    string_find = bpy.context.scene.AutoPBRMapper_setting.string_find
    string_replace = bpy.context.scene.AutoPBRMapper_setting.string_replace
    case_sensitive = bpy.context.scene.AutoPBRMapper_setting.case_sensitive

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
    name_target = bpy.context.scene.AutoPBRMapper_setting.name_target
    name_from = bpy.context.scene.AutoPBRMapper_setting.name_from
    
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

def assignMaterial():
    os.system('cls')

    tex_folder = bpy.context.scene.AutoPBRMapper_setting.filepath
    ext = bpy.context.scene.AutoPBRMapper_setting.filename_ext
    prefix = bpy.context.scene.AutoPBRMapper_setting.prefix

    mBaseColor = bpy.context.scene.AutoPBRMapper_setting.suffix_basecolor
    mMetallic = bpy.context.scene.AutoPBRMapper_setting.suffix_metallic
    mSpecular = bpy.context.scene.AutoPBRMapper_setting.suffix_specular
    mRoughness = bpy.context.scene.AutoPBRMapper_setting.suffix_roughness
    mOpacity = bpy.context.scene.AutoPBRMapper_setting.suffix_opacity
    mNormal = bpy.context.scene.AutoPBRMapper_setting.suffix_normal
    
    mMaterialtype = bpy.context.scene.AutoPBRMapper_setting.materialtype
    mAssigntype = bpy.context.scene.AutoPBRMapper_setting.assigntype

    marggin = 100

    print (mAssigntype)

    if mAssigntype == 'All':
        materials = bpy.data.materials
    elif mAssigntype == 'Selected':
        selectedObjects = bpy.context.selected_objects
        materials = []
        for object in selectedObjects:
            material_slots = object.material_slots
            for slot in material_slots:
                materials.append(slot.material)


    for material in materials:
        main_name = material.name
        tempPathA = (tex_folder + '\\' + prefix + main_name + mBaseColor + ext)

        if material.use_nodes is not True:
            material.use_nodes = True
        # Test if path available
        if os.path.isfile(tempPathA):

            mat_nodes = material.node_tree.nodes
            mat_links = material.node_tree.links

            mat_nodes.clear() # remove all before create our own
            output_shader = mat_nodes.new("ShaderNodeOutputMaterial")

            mix = mat_nodes.new("ShaderNodeMixShader")
            mix.location = (-1 * (mix.width + marggin), 150)
            mix.inputs[0].default_value = 1

            transparent = mat_nodes.new("ShaderNodeBsdfTransparent")
            transparent.location = (-1 * 2 *(transparent.width + marggin), 150)

            main_shader = mat_nodes.new("ShaderNodeBsdfPrincipled")
            main_shader.location = (-1 * 2 * (main_shader.width + marggin), 0)


            tex_base_color = mat_nodes.new("ShaderNodeTexImage")
            try:
                tex_base_color.image = bpy.data.images.load(os.path.join(tex_folder, (prefix + main_name + mBaseColor + ext)), check_existing=True)
                tex_base_color.image.colorspace_settings.name = 'sRGB'
            except RuntimeError as e:
                print(prefix + main_name + " has no baseColor map.\n" + str(e))
            tex_base_color.hide = True
            tex_base_color.location = (-1 * 3 * (tex_base_color.width + marggin), 0)


            tex_metallic = mat_nodes.new("ShaderNodeTexImage")
            try:
                tex_metallic.image = bpy.data.images.load(os.path.join(tex_folder, (prefix + main_name + mMetallic + ext)), check_existing=True)
                tex_metallic.image.colorspace_settings.name = 'Linear'
            except RuntimeError as e:
                print(prefix + main_name + " has no metallic map.\n" + str(e))
            # tex_metallic.color_space="NONE"
            tex_metallic.hide = True
            tex_metallic.location = (-1 * 4 * (tex_metallic.width + marggin), 0)


            tex_specular = mat_nodes.new("ShaderNodeTexImage")
            try:
                tex_specular.image = bpy.data.images.load(os.path.join(tex_folder, (prefix + main_name + mSpecular + ext)), check_existing=True)
                tex_specular.image.colorspace_settings.name = 'Linear'
            except RuntimeError as e:
                print(prefix + main_name + " has no specular map.\n" + str(e))
            # tex_specular.color_space = "NONE"
            tex_specular.hide = True
            tex_specular.location = (-1 * 5 * (tex_specular.width + marggin), 0)


            tex_roughness = mat_nodes.new("ShaderNodeTexImage")
            try:
                tex_roughness.image = bpy.data.images.load(os.path.join(tex_folder, (prefix + main_name + mRoughness + ext)), check_existing=True)
                tex_roughness.image.colorspace_settings.name = 'Linear'
            except RuntimeError as e:
                print(prefix + main_name + " has no roughness map.\n" + str(e))
            # tex_roughness.color_space="NONE"
            tex_roughness.hide = True
            tex_roughness.location = (-1 * 6 * (tex_roughness.width + marggin), 0)


            opcity_exist = True
            tex_opacity = mat_nodes.new("ShaderNodeTexImage")
            try:
                tex_opacity.image = bpy.data.images.load(os.path.join(tex_folder, (prefix + main_name + mOpacity + ext)), check_existing=True)
                tex_opacity.image.colorspace_settings.name = 'Linear'
            except RuntimeError as e:
                opcity_exist = False
                print(prefix + main_name + " has no opacity map.\n" + str(e))
            # tex_opacity.color_space = "NONE"
            tex_opacity.hide = True
            tex_opacity.location = (-1 * 2 * (tex_opacity.width + marggin), 300)


            tex_normal = mat_nodes.new("ShaderNodeTexImage")
            try:
                tex_normal.image = bpy.data.images.load(os.path.join(tex_folder, (prefix + main_name + mNormal + ext)), check_existing=True)
                tex_normal.image.colorspace_settings.name = 'Non-Color'
            except RuntimeError as e:
                print(prefix + main_name + " has no normal map.\n" + str(e))
            # tex_normal.color_space = "NONE"
            tex_normal.hide = True
            tex_normal.location = (-1 * 6.5 * (tex_normal.width + marggin), -400)


            # unitity nodes
            bump = mat_nodes.new("ShaderNodeBump")
            bump.location = (-1 * 4 * (bump.width + marggin), -400)
            normal_map = mat_nodes.new("ShaderNodeNormalMap")
            normal_map.location = (-1 * 5 * (normal_map.width + marggin), -400)
            combin = mat_nodes.new("ShaderNodeCombineRGB")
            combin.location = (-1 * 6 * (combin.width + marggin), -400)
            invert = mat_nodes.new("ShaderNodeInvert")
            invert.location = (-1 * 7 *(invert.width + marggin), -400)
            sp = mat_nodes.new("ShaderNodeSeparateRGB")
            sp.location = (-1 * 8 * (sp.width + marggin), -400)

            # link

            mat_links.new(tex_base_color.outputs["Color"], main_shader.inputs["Base Color"])
            mat_links.new(tex_metallic.outputs["Color"], main_shader.inputs["Metallic"])
            mat_links.new(tex_specular.outputs["Color"], main_shader.inputs["Specular"])
            mat_links.new(tex_roughness.outputs["Color"], main_shader.inputs["Roughness"])
      
            if opcity_exist:
                mat_links.new(tex_opacity.outputs["Color"], mix.inputs[0])

            if mMaterialtype == 'Principle':
                mat_links.new(mix.outputs["Shader"], output_shader.inputs["Surface"])
                mat_links.new(transparent.outputs["BSDF"], mix.inputs[1])
                mat_links.new(main_shader.outputs["BSDF"], mix.inputs[2])
                mat_links.new(bump.outputs["Normal"], main_shader.inputs["Normal"])
                mat_links.new(normal_map.outputs["Normal"], bump.inputs["Normal"])
                mat_links.new(combin.outputs["Image"], normal_map.inputs["Color"])
                mat_links.new(sp.outputs["R"], combin.inputs["R"])
                mat_links.new(sp.outputs["B"], combin.inputs["B"])
                mat_links.new(sp.outputs["G"], invert.inputs["Color"])
                mat_links.new(invert.outputs["Color"], combin.inputs["G"])
                mat_links.new(tex_normal.outputs["Color"], sp.inputs["Image"])

            elif mMaterialtype == 'gltf' :
                mat_links.new(main_shader.outputs["BSDF"], output_shader.inputs["Surface"])
                mat_links.new(bump.outputs["Normal"], main_shader.inputs["Normal"])
                mat_links.new(normal_map.outputs["Normal"], bump.inputs["Normal"])
                mat_links.new(tex_normal.outputs["Color"], normal_map.inputs["Color"])
        
        else:
            print ("%s not exist" % (tempPathA))
            # print
            # print ( 'Material:{0} -- auto PBR assigned Success '.format(main_name) )

