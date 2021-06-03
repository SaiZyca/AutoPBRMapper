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




