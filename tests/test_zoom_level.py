import unittest
from unittest.mock import MagicMock
import sys
import os

# Add the repository root to the python path so we can import the plugin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock QGIS before importing the plugin
from tests.qgis_mock import mock_qgis
mock_qgis()

from copy_map_link_plugin import CopyMapLinkPlugin

class TestZoomLevel(unittest.TestCase):
    def setUp(self):
        self.iface = MagicMock()
        self.plugin = CopyMapLinkPlugin(self.iface)

    def test_get_zoom_level_standard_scales(self):
        # zoom = log2(591657550.5 / scale)
        # scale = 591657550.5 / 2^zoom

        # Zoom 0: scale ~ 591657550.5
        self.assertEqual(self.plugin.get_zoom_level(591657550.5), 0)

        # Zoom 1: scale ~ 295828775.25
        self.assertEqual(self.plugin.get_zoom_level(295828775.25), 1)

        # Zoom 10: scale ~ 577790.576
        self.assertEqual(self.plugin.get_zoom_level(577790.576), 10)

        # Zoom 18: scale ~ 2257.0
        self.assertEqual(self.plugin.get_zoom_level(2257.0), 18)

    def test_get_zoom_level_edge_cases(self):
        # Scale <= 0 should return 0
        self.assertEqual(self.plugin.get_zoom_level(0), 0)
        self.assertEqual(self.plugin.get_zoom_level(-100), 0)

    def test_get_zoom_level_clamping(self):
        # Very large scale should clamp to 0
        self.assertEqual(self.plugin.get_zoom_level(10**12), 0)

        # Very small scale should clamp to 21
        self.assertEqual(self.plugin.get_zoom_level(0.0001), 21)

    def test_get_zoom_level_error_handling(self):
        # Passing invalid type should return fallback value 12
        self.assertEqual(self.plugin.get_zoom_level("invalid"), 12)
        self.assertEqual(self.plugin.get_zoom_level(None), 12)

if __name__ == "__main__":
    unittest.main()
