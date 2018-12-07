# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "AutoPBRMapper",
    "author" : "Sai Ling",
    "description": "Auto PBR Mapper",
    "blender" : (2, 80, 0),
    "location": "SpaceBar Search -> Addon Preferences Example",
    "warning" : "",
    "wiki_url": "https://blog.xuite.net/ptsblog/news",
    "category" : "Generic"
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty


class App_Preferences(AddonPreferences):
    bl_idname = __name__

    suffix_basecolor = StringProperty(
        default="_BaseColor",
        name="BaseColor Suffix"
    )
    suffix_normal = StringProperty(
        default="_Normal",
        name="Normal Suffix"
    )
    suffix_metallic = StringProperty(
        default="_Metallic",
        name="Metallic Suffix"
    )
    suffix_roughnes = StringProperty(
        default="_Roughness",
        name="Roughnes Suffix"
    )
    suffix_specular = StringProperty(
        default="_Specular",
        name="Specular Suffix"
    )
    suffix_opacity = StringProperty(
        default="_Opacity",
        name="Opacity Suffix"
    )
    number = IntProperty(
        name="Example Number",
        default=4,
    )
    boolean = BoolProperty(
        name="Example Boolean",
        default=False,
    )

    preferences_tabs = [("GENERAL", "General", ""),
                        ("KEYMAPS", "Keymaps", ""),
                        ("ABOUT", "About", "")]

    tabs: EnumProperty(name="Tabs", items=preferences_tabs, default="GENERAL")

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our addon")
        layout.prop(self, "suffix_basecolor")
        layout.prop(self, "suffix_normal")
        layout.prop(self, "suffix_metallic")
        layout.prop(self, "suffix_roughnes")
        layout.prop(self, "suffix_specular")
        layout.prop(self, "suffix_opacity")
        layout.prop(self, "number")
        layout.prop(self, "boolean")


class AutoPBRMapper_prefs(Operator):
    """PBR maps setting"""
    bl_idname = "pbrmapper.addon_prefs"
    bl_label = "PBR Mapper Preferences "
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        info = ("Path: %s, Number: %d, Boolean %r" %
                (addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}


# Registration
def register():
    bpy.utils.register_class(AutoPBRMapper_prefs)
    bpy.utils.register_class(App_Preferences)


def unregister():
    bpy.utils.unregister_class(AutoPBRMapper_prefs)
    bpy.utils.unregister_class(App_Preferences)