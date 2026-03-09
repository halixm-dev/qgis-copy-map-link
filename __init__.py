# -*- coding: utf-8 -*-

def classFactory(iface):
    """
    Load the plugin class from the main plugin file.
    This function is called by QGIS when the plugin is loaded.
    """
    # Import the main plugin class
    from .copy_map_link_plugin import CopyMapLinkPlugin
    return CopyMapLinkPlugin(iface)
