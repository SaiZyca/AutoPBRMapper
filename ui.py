import bpy
from bpy.types import Operator, AddonPreferences, Panel, PropertyGroup
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, BoolVectorProperty, PointerProperty, EnumProperty

class AUTOPBR_PT_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoPBRMapper"
    bl_label = "AutoPBRMapper"
    # bl_options = {"DEFAULT_CLOSED"}   
    def draw(self,context):
        pass

class AUTOPBR_PT_assigner(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoPBRMapper"
    bl_label = "Assign PBR Materual"
    bl_parent_id = "AUTOPBR_PT_panel"
    # bl_options = {"DEFAULT_CLOSED"}   
    def draw(self,context):
        layout = self.layout
        row = layout.row(align = True)
        #layout.label('Mesh Tools')
        row.prop(bpy.context.scene.AUTOPBR_properties , "filepath")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AUTOPBR_properties , "prefix") 
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AUTOPBR_properties , "suffix_basecolor")       
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AUTOPBR_properties , "suffix_normal")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AUTOPBR_properties , "suffix_metallic")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AUTOPBR_properties , "suffix_roughness")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AUTOPBR_properties , "suffix_specular")
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AUTOPBR_properties , "suffix_opacity") 
        row = layout.row(align = True)
        row.prop(bpy.context.scene.AUTOPBR_properties , "filename_ext", expand=True)        
        row = layout.row(align = True) 
        row.prop(bpy.context.scene.AUTOPBR_properties , "materialtype", expand=True)        
        row = layout.row(align = True) 
        row.prop(bpy.context.scene.AUTOPBR_properties , "assigntype", expand=True)  
        row = layout.row(align = True) 
        row.operator('autopbrmapper.actions',text = 'Assign Materials').button = 'AssignMaterial'

class AUTOPBR_PT_renamer(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoPBRMapper"
    bl_label = "Quick Renamer"
    bl_parent_id = "AUTOPBR_PT_panel"
    # bl_options = {"DEFAULT_CLOSED"}   
    
    def draw(self,context):
        layout = self.layout
        row = layout.row(align = False)
        row.prop(context.scene.AUTOPBR_properties , "objects_collection", expand=True) 
        row = layout.row(align = True)
        row.label(text='Target Name')
        row.prop(context.scene.AUTOPBR_properties , "name_target", expand=False) 
        row = layout.row(align = True)
        row.label(text='Rename Type')
        row.prop(context.scene.AUTOPBR_properties , "rename_type", expand=False) 
        if context.scene.AUTOPBR_properties.rename_type == 'COPY':
            row = layout.row(align = False)
            row.prop(context.scene.AUTOPBR_properties , "name_from", expand=False)
            row = layout.row(align = False)
            row.operator('autopbrmapper.actions',text = 'Apply Name').button = 'Apply Name'
        elif context.scene.AUTOPBR_properties.rename_type == 'REPLACE':
            row = layout.row(align = False)
            row.label(text='Find')
            row.label(text='Replace to')
            row = layout.row(align = False)
            row.prop(context.scene.AUTOPBR_properties , "string_find")
            row.prop(context.scene.AUTOPBR_properties , "string_replace")
            row = layout.row(align = False)
            row.prop(context.scene.AUTOPBR_properties , "case_sensitive")
            row = layout.row(align = False)
            row.operator('autopbrmapper.actions',text = 'Find / Replace:').button = 'Find Replace'

class AUTOPBR_PT_reassign(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoPBRMapper"
    bl_label = "ReAssign Material"
    bl_parent_id = "AUTOPBR_PT_panel"

    def draw(self,context):
        layout = self.layout
        row = layout.row(align = False)
        row.operator('material_tools.export_material_data', icon='EXPORT')
        row = layout.row(align = False)
        row.operator('material_tools.append_material', icon='IMPORT')
        row = layout.row(align = False)
        row.prop(context.scene.AUTOPBR_properties , "material_data_file") 
        row = layout.row(align = False)
        split = row.split(factor=0.3, align=False)
        split.prop(context.scene.AUTOPBR_properties , "fuzzy_search")
        split.operator('material_tools.re_assign_material')


classes = (
    AUTOPBR_PT_panel,
    AUTOPBR_PT_assigner,
    AUTOPBR_PT_renamer,
    AUTOPBR_PT_reassign,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()
