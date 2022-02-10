import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty, BoolVectorProperty

class AUTOPBR_properties(bpy.types.PropertyGroup):

    filepath : StringProperty(
        default = "//texture",
        subtype="DIR_PATH",
        name = "Texture Folder"
    )
    prefix : StringProperty(
        default = "",
        name = "Prefix",
    )
    suffix_basecolor : StringProperty(
        default = "_BaseColor",
        name = "BaseColor Suffix",
    )
    suffix_emission : StringProperty(
        default = "_Emission",
        name = "Emission Suffix",
    )
    suffix_height : StringProperty(
        default = "_Height",
        name = "Height Suffix",
    )
    suffix_normal : StringProperty(
        default = "_Normal",
        name = "Normal Suffix",
    )
    suffix_displace : StringProperty(
        default = "_Displace",
        name = "Displace Suffix",
    )
    suffix_metallic: StringProperty(
        default = "_Metallic",
        name = "Metallic Suffix",
    )
    suffix_roughness : StringProperty(
        default = "_Roughness",
        name = "Roughness Suffix",
    )
    suffix_specular: StringProperty(
        default = "_Specular",
        name = "Specular Suffix"
    )
    suffix_opacity: StringProperty(
        default = "_Opacity",
        name = "Opacity Suffix"
    )
    filename_ext : EnumProperty(
        items = [
            ('.png','.png','*.png'),
            ('.jpg','.jpg','*.jpg'),
            ('.exr','.exr','*.exr'),
            
        ],
        name = 'File Extension'
    )
    exportfolder : StringProperty(
        default = r"//texture/convert\\",
        subtype="DIR_PATH",
        name = "Export Folder"
    )
    export_ext : EnumProperty(
        items = [
            ('.png','.png','*.png'),
            ('.jpg','.jpg','*.jpg'),
            ('.exr','.exr','*.exr'),
        ],
        name = 'Export File Extension'
    )
    export_scale : IntProperty(
        description="Scale image size",
        subtype = 'PERCENTAGE',
        default = 100,
        min = 1,
        max = 100,
        step = 100,
        name = 'Scale'
    )
    filp_normal_map : BoolVectorProperty(
        name="Flip Normal",
        description="Flip normal map channel for D3D <--> OpenGL",
        size=3,
        default = (False, False, False)
    ) 
    materialtype : EnumProperty(
        items = [
            ('Mix','Mix','Mix Opacity map with Glass Shader'),
            ('Principle','Principle','All Map with one Principle Shader'),   
        ],
        name = 'Material Type'
    )
    assigntype : EnumProperty(
        items = [
            ('All','All','Assign to all object'),
            ('Selected','Selected','Assign selected object only')
        
        ],
        name = 'Assign Type'
    )
    objects_collection : EnumProperty(
        items = [
            ('ALL','All','All Objects'),
            ('SELECTION','Selection','Selecton only'),  
        ],
        default='ALL',
        name = 'OBJECT'
    )
    rename_type : EnumProperty(
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
    string_find: StringProperty(
        default = "",
        name = "",
    )
    string_replace: StringProperty(
        default = "",
        name = "",
    )
    case_sensitive : BoolProperty(
        name="Case Sensitive",
        description="Case Sensitive",
        default = True
    ) 
    material_data_file : StringProperty(
        default = "/temp/data.json",
        subtype="FILE_PATH",
        name = "mapping file"
    )
    fuzzy_search : BoolProperty(
        name="Fuzzy search",
        description="Fuzzy Search",
        default = True
    ) 

classes = (
    AUTOPBR_properties,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.AUTOPBR_properties = bpy.props.PointerProperty(type=AUTOPBR_properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.AUTOPBR_properties

if __name__ == '__main__':
    register()
