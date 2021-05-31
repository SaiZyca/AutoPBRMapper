# coding=UTF-8

'''
2019/06/05 fix 2.8 api change
colorspace setting move to image node from shader node 
'''

import bpy
import os
import re
from bpy.types import Operator, AddonPreferences, Panel, PropertyGroup
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty, EnumProperty


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

class AutoPBRMapper_Preferences(bpy.types.AddonPreferences):
    bl_idname = get_addon_name()

    prefix : bpy.props.StringProperty(
        default = "",
        name = "Prefix",
    )
    suffix_basecolor: bpy.props.StringProperty(
        default="_BaseColor",
        name="BaseColor Suffix",
    )
    suffix_normal: bpy.props.StringProperty(
        default="_Normal",
        name="Normal Suffix"
    )
    suffix_metallic: bpy.props.StringProperty(
        default="_Metallic",
        name="Metallic Suffix"
    )
    suffix_roughnes: bpy.props.StringProperty(
        default="_Roughness",
        name="Roughnes Suffix"
    )
    suffix_specular: bpy.props.StringProperty(
        default="_Specular",
        name="Specular Suffix"
    )
    suffix_opacity: bpy.props.StringProperty(
        default="_Opacity",
        name="Opacity Suffix"
    )
    filename_ext : bpy.props.EnumProperty(
        items = [
            ('.png','.png','*.png'),
            ('.jpg','.jpg','*.jpg')
            
        ],
        name = 'File Extension'
    )
    materialtype: bpy.props.EnumProperty(
        items = [
            ('Principle','Principle','Principle for cycles or Eevee'),
            ('gltf','gltf','gltf for babylon js')
        
        ],
        name = 'Material Type'
    )

    preferences_tabs =  [("GENERAL", "General", ""),
                        ("KEYMAPS", "Keymaps", ""),
                        ("ABOUT", "About", "")]

    # tabs: bpy.props.EnumProperty(name="Tabs", items=preferences_tabs, default="GENERAL")

    # def draw(self, context):
    #     layout = self.layout
    #     layout.label(text="Auto PBR Map Importer Settings")

    #     column = layout.column(align=True)
    #     row = column.row()
    #     row.prop(self, "tabs", expand=True)

    #     box = column.box()
    #     split = box.split(factor = 0.75)
    #     groupBox = split.box()
    #     groupBox.label(text="Map FileName Setting")

    #     column = groupBox.column(align=True)
    #     column.prop(self, "suffix_basecolor")
    #     column.prop(self, "suffix_normal")
    #     column.prop(self, "suffix_metallic")
    #     column.prop(self, "suffix_roughnes")
    #     column.prop(self, "suffix_specular")
    #     column.prop(self, "suffix_opacity")
    #     row = groupBox.row(align=True)
    #     row.label(text="File Extension")
    #     row.prop(self, "filename_ext", expand=True)

    #     groupBox = split.box()
    #     groupBox.label(text="Material Type")
    #     column = groupBox.column(align=True)
    #     column.prop(self, "materialtype", expand=True)

class AutoPBRMapper_properties(bpy.types.PropertyGroup):

    filepath : bpy.props.StringProperty(
        default = "c:\\temp\\",
        subtype="FILE_PATH",
        name = "Texture Folder"
    )
    prefix : bpy.props.StringProperty(
        default = "",
        name = "Prefix",
    )
    suffix_basecolor : bpy.props.StringProperty(
        default = "_BaseColor",
        name = "BaseColor Suffix",
    )
    suffix_normal : bpy.props.StringProperty(
        default = "_Normal",
        name = "Normal Suffix",
    )
    suffix_metallic: bpy.props.StringProperty(
        default = "_Metallic",
        name = "Metallic Suffix",
    )
    suffix_roughness : bpy.props.StringProperty(
        default = "_Roughness",
        name = "Roughness Suffix",
    )
    suffix_specular: bpy.props.StringProperty(
        default = "_Specular",
        name = "Specular Suffix"
    )
    suffix_opacity: bpy.props.StringProperty(
        default = "_Opacity",
        name = "Opacity Suffix"
    )
    filename_ext : bpy.props.EnumProperty(
        items = [
            ('.png','.png','*.png'),
            ('.jpg','.jpg','*.jpg')
            
        ],
        name = 'File Extension'
    )
    materialtype : bpy.props.EnumProperty(
        items = [
            ('Principle','Principle','Principle for cycles or Eevee'),
            ('gltf','gltf','gltf for babylon js')
        
        ],
        name = 'Material Type'
    )
    assigntype : bpy.props.EnumProperty(
        items = [
            ('All','All','Assign to all object'),
            ('Selected','Selected','Assign selected object only')
        
        ],
        name = 'Assign Type'
    )
    objects_collection : bpy.props.EnumProperty(
        items = [
            ('ALL','All','All Objects'),
            ('SELECTION','Selection','Selecton only'),  
        ],
        default='ALL',
        name = 'OBJECT'
    )
    rename_type : bpy.props.EnumProperty(
        items = [
            ('COPY','Copy From','Copy From'),
            ('REPLACE','Find Replace','Find / Replace'),  
        ],
        default='COPY',
        name = ''
    )
    name_target: EnumProperty(
    name="",
    description="get name from data",
    items=[("OBJECT", "Object", "Object Name"),
            ("DATA", "Data", "Data Name"),
            ("MATERIAL", "Material", "Material Name"),
            ],
    default='MATERIAL',
    )
    name_from: EnumProperty(
    name="",
    description="get name from data",
    items=[("OBJECT", "Object", "Object Name"),
            ("DATA", "Data", "Data Name"),
            ("MATERIAL", "Material", "Material Name"),
            ],
    default='OBJECT',
    )
    string_find: bpy.props.StringProperty(
        default = "",
        name = "",
    )
    string_replace: bpy.props.StringProperty(
        default = "",
        name = "",
    )
    case_sensitive : BoolProperty(
        name="Case Sensitive",
        description="Case Sensitive",
        default = True) 

class AutoPBRMapper_Actions(bpy.types.Operator):
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
                assignMaterial()

            elif button == 'Apply Name':
                data_rename()

            elif button == 'Find Replace':
                find_replace()

            else:
                print ('Not defined !')
        except Exception as e:
            print ('Execute Error:',e)
        
        return {"FINISHED"}

class AutoPBRMapper_PT_Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoPBRMapper"
    bl_label = "AutoPBRMapper"
    # bl_options = {"DEFAULT_CLOSED"}   
    def draw(self,context):
        pass

class AutoPBRMapper_PT_assigner(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoPBRMapper"
    bl_label = "Assign PBR Materual"
    bl_parent_id = "AutoPBRMapper_PT_Panel"
    # bl_options = {"DEFAULT_CLOSED"}   
    def draw(self,context):
        layout = self.layout
        row = layout.row(align = True)
        #layout.label('Mesh Tools')
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "filepath")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "prefix") 
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "suffix_basecolor")       
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "suffix_normal")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "suffix_metallic")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "suffix_roughness")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "suffix_specular")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "suffix_opacity") 
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "filename_ext", expand=True)        
        row = layout.row(align = True) 
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "materialtype", expand=True)        
        row = layout.row(align = True) 
        row.prop(bpy.context.scene.AutoPBRMapper_setting , "assigntype", expand=True)  
        row = layout.row(align = True) 
        row.operator('autopbrmapper.actions',text = 'Assign Materials').button = 'AssignMaterial'
class AutoPBRMapper_PT_renamer(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoPBRMapper"
    bl_label = "Quick Renamer"
    bl_parent_id = "AutoPBRMapper_PT_Panel"
    # bl_options = {"DEFAULT_CLOSED"}   
    
    def draw(self,context):
        layout = self.layout
        row = layout.row(align = False)
        row.prop(context.scene.AutoPBRMapper_setting , "objects_collection", expand=True) 
        row = layout.row(align = True)
        row.label(text='Target Name')
        row.prop(context.scene.AutoPBRMapper_setting , "name_target", expand=False) 
        row = layout.row(align = True)
        row.label(text='Rename Type')
        row.prop(context.scene.AutoPBRMapper_setting , "rename_type", expand=False) 
        if context.scene.AutoPBRMapper_setting.rename_type == 'COPY':
            row = layout.row(align = False)
            row.prop(context.scene.AutoPBRMapper_setting , "name_from", expand=False)
            row = layout.row(align = False)
            row.operator('autopbrmapper.actions',text = 'Apply Name').button = 'Apply Name'
        elif context.scene.AutoPBRMapper_setting.rename_type == 'REPLACE':
            row = layout.row(align = False)
            row.label(text='Find')
            row.label(text='Replace to')
            row = layout.row(align = False)
            row.prop(context.scene.AutoPBRMapper_setting , "string_find")
            row.prop(context.scene.AutoPBRMapper_setting , "string_replace")
            row = layout.row(align = False)
            row.prop(context.scene.AutoPBRMapper_setting , "case_sensitive")
            row = layout.row(align = False)
            row.operator('autopbrmapper.actions',text = 'Find / Replace:').button = 'Find Replace'
