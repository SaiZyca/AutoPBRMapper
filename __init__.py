# coding=UTF-8

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
    "version": (0, 0, 1),
    "blender" : (2, 80, 0),
    "location": "View3D > Sidebar",
    "warning" : "",
    "wiki_url": "https://blog.xuite.net/ptsblog/news",
    "category" : "Generic"
}

import bpy
import importlib
from . import addon_classes

importlib.reload(addon_classes)


classes = (
    addon_classes.AutoPBRMapper_Preferences,
    addon_classes.AutoPBRMapper_properties,
    addon_classes.AutoPBRMapper_Actions,
    addon_classes.AutoPBRMapper_PT_Panel,
    addon_classes.AutoPBRMapper_PT_assigner,
    addon_classes.AutoPBRMapper_PT_renamer
)

# Registration

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.AutoPBRMapper_setting = bpy.props.PointerProperty(type=addon_classes.AutoPBRMapper_properties)
    print ("AutoPBRMapper coming")

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.AutoPBRMapper_setting
    
    print ("AutoPBRMapper leaving")


if __name__ == '__main__':
    main()