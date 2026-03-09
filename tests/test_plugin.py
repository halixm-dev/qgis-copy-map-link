import unittest
import sys
import os
from unittest.mock import MagicMock

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from tests.qgis_mock import mock_qgis
mock_qgis_core = mock_qgis()

from copy_map_link_plugin import CopyMapLinkPlugin

class TestCopyMapLinkPlugin(unittest.TestCase):
    def setUp(self):
        self.iface = MagicMock()
        self.canvas = self.iface.mapCanvas()
        self.canvas.scale.return_value = 1000
        self.plugin = CopyMapLinkPlugin(self.iface)

    def test_zoom_level(self):
        self.assertEqual(self.plugin.get_zoom_level(1000), 19)
        self.assertEqual(self.plugin.get_zoom_level(591657550.5), 0)
        self.assertEqual(self.plugin.get_zoom_level(0), 0)
        self.assertEqual(self.plugin.get_zoom_level(-1), 0)

    def test_copy_link_format(self):
        import copy_map_link_plugin
        # Setup mock transform to return a known point
        mock_transform = MagicMock()
        mock_qgis_core.QgsCoordinateTransform.return_value = mock_transform

        point_wgs84 = MagicMock()
        point_wgs84.x.return_value = 10.0
        point_wgs84.y.return_value = 20.0
        mock_transform.transform.return_value = point_wgs84

        # Mock point for clicking
        copy_map_link_plugin.clicked_point_canvas_crs = mock_qgis_core.QgsPointXY(123, 456)

        # Mock QApplication clipboard
        mock_app = MagicMock()
        mock_qgis_core.QgsCoordinateReferenceSystem.QApplication = mock_app # This is a hack because of how I mocked it, let me fix qgis_mock.py

        # Actually, let's just mock QApplication.clipboard
        with unittest.mock.patch('copy_map_link_plugin.QApplication.clipboard') as mock_clipboard:
            clipboard_instance = MagicMock()
            mock_clipboard.return_value = clipboard_instance

            template = "https://example.com/?lat={lat}&lon={lon}&z={zoom}"
            self.plugin.copy_link(template)

            # zoom for scale 1000 is 19
            expected_link = "https://example.com/?lat=20.0&lon=10.0&z=19"
            clipboard_instance.setText.assert_called_with(expected_link)

if __name__ == "__main__":
    unittest.main()
