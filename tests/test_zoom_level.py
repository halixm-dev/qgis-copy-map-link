import unittest
from unittest.mock import MagicMock
import sys
import os

# Ensure the root directory is in sys.path so we can import the plugin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the mock before importing the plugin
import tests.qgis_mock
from copy_map_link_plugin import CopyMapLinkPlugin

class TestZoomLevel(unittest.TestCase):
    def setUp(self):
        self.iface = MagicMock()
        self.plugin = CopyMapLinkPlugin(self.iface)

    def test_get_zoom_level_zero_scale(self):
        """Test that a scale of 0 returns zoom level 0."""
        self.assertEqual(self.plugin.get_zoom_level(0), 0)

    def test_get_zoom_level_negative_scale(self):
        """Test that a negative scale returns zoom level 0."""
        self.assertEqual(self.plugin.get_zoom_level(-1), 0)
        self.assertEqual(self.plugin.get_zoom_level(-1000), 0)

    def test_get_zoom_level_large_scale(self):
        """Test that a very large scale returns the minimum zoom level (0)."""
        # zoom = log2(591657550.5 / 1,000,000,000) is negative, should be clamped to 0
        self.assertEqual(self.plugin.get_zoom_level(1000000000), 0)

    def test_get_zoom_level_small_scale(self):
        """Test that a very small scale returns the maximum zoom level (21)."""
        # zoom = log2(591657550.5 / 1) is ~29, should be clamped to 21
        self.assertEqual(self.plugin.get_zoom_level(1), 21)

    def test_get_zoom_level_standard_scales(self):
        """Test standard scales and their expected zoom levels."""
        # Exact match for zoom 0
        self.assertEqual(self.plugin.get_zoom_level(591657550.5), 0)

        # Exact match for zoom 1
        self.assertEqual(self.plugin.get_zoom_level(591657550.5 / 2), 1)

        # Test scale for zoom 15: 591657550.5 / (2^15) ≈ 18055.95
        self.assertEqual(self.plugin.get_zoom_level(18056), 15)
        self.assertEqual(self.plugin.get_zoom_level(18055), 15)

    def test_get_zoom_level_exception_handling(self):
        """Test that the function handles unexpected input types by returning the default zoom (12)."""
        # Passing None should trigger the try-except block
        self.assertEqual(self.plugin.get_zoom_level(None), 12)

if __name__ == '__main__':
    unittest.main()
