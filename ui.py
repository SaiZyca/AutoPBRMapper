import bpy
from bpy.types import Operator, AddonPreferences, Panel, PropertyGroup
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty, EnumProperty

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

class AutoPBRMapper_PT_reAssign(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoPBRMapper"
    bl_label = "ReAssign Material"
    bl_parent_id = "AutoPBRMapper_PT_Panel"

    def draw(self,context):
        layout = self.layout
        row = layout.row(align = False)
        row.operator('material_tools.export_material_data')
        row.prop(context.scene.AutoPBRMapper_setting , "material_data_file") 
        row = layout.row(align = False)
        
        row.operator('material_tools.re_assign_material')


classes = (
    AutoPBRMapper_PT_Panel,
    AutoPBRMapper_PT_assigner,
    AutoPBRMapper_PT_renamer,
    AutoPBRMapper_PT_reAssign,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
