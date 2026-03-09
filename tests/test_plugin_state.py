import unittest
from unittest.mock import MagicMock
import sys
import os

# Ensure the plugin can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import mocks before importing the plugin
import tests.qgis_mock

import copy_map_link_plugin
from copy_map_link_plugin import CopyMapLinkPlugin

class TestPluginState(unittest.TestCase):
    def setUp(self):
        self.iface = MagicMock()
        self.plugin = CopyMapLinkPlugin(self.iface)

    def test_no_global_state(self):
        """Verify that global variables iface and clicked_point_canvas_crs are removed from the module."""
        self.assertFalse(hasattr(copy_map_link_plugin, 'iface'), "Global 'iface' still exists")
        self.assertFalse(hasattr(copy_map_link_plugin, 'clicked_point_canvas_crs'), "Global 'clicked_point_canvas_crs' still exists")

    def test_instance_variables_initialized(self):
        """Verify that iface and clicked_point_canvas_crs are initialized as instance variables."""
        self.assertEqual(self.plugin.iface, self.iface)
        self.assertIsNone(self.plugin.clicked_point_canvas_crs)

    def test_prepare_canvas_context_menu_sets_instance_variable(self):
        """Verify prepare_canvas_context_menu sets the instance variable."""
        mock_event = MagicMock()
        mock_point = MagicMock()
        mock_point.x.return_value = 10.0
        mock_point.y.return_value = 20.0
        mock_event.mapPoint.return_value = mock_point

        mock_menu = MagicMock()

        self.plugin.prepare_canvas_context_menu(mock_menu, mock_event)

        self.assertIsNotNone(self.plugin.clicked_point_canvas_crs)
        self.assertEqual(self.plugin.clicked_point_canvas_crs.x(), 10.0)
        self.assertEqual(self.plugin.clicked_point_canvas_crs.y(), 20.0)

    def test_copy_link_clears_instance_variable(self):
        """Verify copy_link clears the instance variable after use."""
        # Manually set the clicked point
        from tests.qgis_mock import MockQgsPointXY
        self.plugin.clicked_point_canvas_crs = MockQgsPointXY(10.0, 20.0)

        # Mocking canvas and other dependencies to avoid failure before the finally block
        self.plugin.canvas.mapSettings().destinationCrs().isValid.return_value = True
        import qgis.core
        qgis.core.QgsCoordinateReferenceSystem().isValid.return_value = True

        # Call copy_link with a template
        self.plugin.copy_link("https://maps.com?lat={lat}&lon={lon}")

        self.assertIsNone(self.plugin.clicked_point_canvas_crs)

if __name__ == '__main__':
    unittest.main()
