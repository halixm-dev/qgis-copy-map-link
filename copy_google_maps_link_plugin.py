# Import necessary QGIS and Qt modules
from qgis.PyQt.QtWidgets import QAction, QApplication, QMenu
from qgis.core import QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsPointXY, QgsMessageLog, Qgis
import math
import functools

# This is a common way to store a reference to the QGIS interface
iface = None

# Global variable to store the clicked point
clicked_point_canvas_crs = None

def plugin_path():
    """Helper function to get the plugin's directory (optional, but good practice for icons etc.)"""
    import os
    return os.path.dirname(os.path.realpath(__file__))

class CopyMapLinkPlugin:
    """
    This class defines the QGIS plugin.
    """
    PROVIDERS = {
        "Google Maps": "https://www.google.com/maps?q={lat},{lon}&z={zoom}",
        "OpenStreetMap": "https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map={zoom}/{lat}/{lon}",
        "Bing Maps": "https://www.bing.com/maps?cp={lat}~{lon}&lvl={zoom}",
        "Yandex Maps": "https://yandex.com/maps/?text={lat},{lon}&z={zoom}",
        "Geo URI": "geo:{lat},{lon}?z={zoom}"
    }

    def __init__(self, qgis_iface):
        """
        Constructor.
        """
        global iface
        iface = qgis_iface
        self.plugin_name = "Copy Map Link"
        self.canvas = iface.mapCanvas()

        # We don't create a persistent QMenu/QAction here because we will build it dynamically
        # or add to the existing context menu.
        # However, to be safe and manage memory, we can track actions we create.
        self.actions = []

        QgsMessageLog.logMessage(f"{self.plugin_name}: __init__ completed.", self.plugin_name, Qgis.Info)

    def initGui(self):
        """
        This method is called when the plugin is loaded into QGIS.
        """
        self.canvas.contextMenuAboutToShow.connect(self.prepare_canvas_context_menu)
        QgsMessageLog.logMessage(f"{self.plugin_name}: initGui completed and signal connected.", self.plugin_name, Qgis.Info)

    def prepare_canvas_context_menu(self, menu, event):
        """
        Called when the map canvas context menu is about to be shown.
        """
        global clicked_point_canvas_crs

        # Clear previous actions to avoid memory leak
        self.actions = []

        if event and event.mapPoint():
            # Store the clicked point
            clicked_point_canvas_crs = QgsPointXY(event.mapPoint())

            menu.addSeparator()
            # Create a submenu
            submenu = menu.addMenu("Copy Map Link")

            # Add actions for each provider
            for provider_name, url_template in self.PROVIDERS.items():
                action = submenu.addAction(provider_name)
                # Use functools.partial to pass the template to the handler
                action.triggered.connect(functools.partial(self.copy_link, url_template))
                self.actions.append(action)
        else:
            QgsMessageLog.logMessage(f"{self.plugin_name}: prepare_canvas_context_menu called without a valid event or mapPoint.", self.plugin_name, Qgis.Warning)

    def get_zoom_level(self, scale):
        """
        Approximates the Web Mercator zoom level from the map scale.
        zoom = log2(591657550.5 / scale)
        """
        try:
            if scale <= 0:
                return 0
            zoom = math.log(591657550.5 / scale, 2)
            # Clamp zoom level between 0 and 21 (typical web map limits)
            return max(0, min(21, int(round(zoom))))
        except Exception:
            return 12 # Default fallback

    def copy_link(self, url_template, checked=False):
        """
        Generates the link based on the template and copies it to clipboard.
        Accepts 'checked' argument because QAction.triggered emits a boolean.
        """
        global clicked_point_canvas_crs
        if not clicked_point_canvas_crs:
            iface.messageBar().pushMessage("Error", "Could not get clicked point.", level=Qgis.Critical, duration=4)
            return

        try:
            canvas_crs = self.canvas.mapSettings().destinationCrs()
            if not canvas_crs.isValid():
                iface.messageBar().pushMessage("Error", "Invalid Canvas CRS.", level=Qgis.Critical, duration=5)
                return

            target_crs = QgsCoordinateReferenceSystem("EPSG:4326")
            if not target_crs.isValid():
                iface.messageBar().pushMessage("Error", "Could not define target CRS (EPSG:4326).", level=Qgis.Critical, duration=5)
                return

            transform = QgsCoordinateTransform(canvas_crs, target_crs, QgsProject.instance())
            point_wgs84 = transform.transform(clicked_point_canvas_crs)

            if not (point_wgs84.x() == point_wgs84.x() and point_wgs84.y() == point_wgs84.y()) or \
               abs(point_wgs84.x()) == float('inf') or abs(point_wgs84.y()) == float('inf') or \
               not (-90 <= point_wgs84.y() <= 90 and -180 <= point_wgs84.x() <= 180):
                 iface.messageBar().pushMessage("Error", "Invalid WGS84 coordinates.", level=Qgis.Critical, duration=5)
                 return

            # Get current zoom level
            scale = self.canvas.scale()
            zoom = self.get_zoom_level(scale)

            # Format the URL
            link = url_template.format(lat=point_wgs84.y(), lon=point_wgs84.x(), zoom=zoom)

            clipboard = QApplication.clipboard()
            clipboard.setText(link)

            iface.messageBar().pushMessage("Success", f"Link copied: {link}", level=Qgis.Success, duration=5)

        except Exception as e:
            iface.messageBar().pushMessage("Error", f"Error copying link: {str(e)}", level=Qgis.Critical, duration=5)
            QgsMessageLog.logMessage(f"Error copying link: {str(e)}", self.plugin_name, Qgis.Critical)
        finally:
            clicked_point_canvas_crs = None

    def unload(self):
        try:
            if self.canvas:
                self.canvas.contextMenuAboutToShow.disconnect(self.prepare_canvas_context_menu)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error disconnecting signal in unload: {str(e)}", self.plugin_name, Qgis.Warning)

        self.actions = []

# Standard QGIS plugin functions:

def classFactory(iface_obj):
    global iface
    iface = iface_obj
    return CopyMapLinkPlugin(iface_obj)

def name():
    return "Copy Map Link"

def description():
    return "Right-click on the map canvas to copy a map link (Google, OSM, Bing, etc.)."

def version():
    return "0.3.0"

def qgisMinimumVersion():
    return "3.0"

def authorName():
    return "AI Assistant (with user feedback)"

def icon():
    return ""

def about():
    return """
    This plugin adds an option to the map canvas context menu to copy a link
    to various map services (Google Maps, OpenStreetMap, Bing Maps, Yandex Maps, Geo URI).
    Version: 0.3.0
    """

def category():
    return "Map Tools"

def type():
    return Qgis.PluginType.UI
