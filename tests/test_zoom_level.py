import unittest
from unittest.mock import MagicMock

# Import the mock before the plugin
import tests.qgis_mock
from copy_map_link_plugin import CopyMapLinkPlugin

class TestZoomLevel(unittest.TestCase):
    def setUp(self):
        self.iface = MagicMock()
        self.plugin = CopyMapLinkPlugin(self.iface)

    def test_get_zoom_level_zero_scale(self):
        """Test that scale 0 returns zoom level 0."""
        self.assertEqual(self.plugin.get_zoom_level(0), 0)

    def test_get_zoom_level_negative_scale(self):
        """Test that negative scale returns zoom level 0."""
        self.assertEqual(self.plugin.get_zoom_level(-1), 0)
        self.assertEqual(self.plugin.get_zoom_level(-100), 0)

    def test_get_zoom_level_typical_scales(self):
        """Test zoom levels for typical map scales."""
        # 591657550.5 / 591657550.5 = 1, log2(1) = 0
        self.assertEqual(self.plugin.get_zoom_level(591657550.5), 0)

        # 591657550.5 / 295828775.25 = 2, log2(2) = 1
        self.assertEqual(self.plugin.get_zoom_level(295828775.25), 1)

        # A more typical scale, e.g., 1:50,000
        # log2(591657550.5 / 50000) = log2(11833.151) ≈ 13.53 -> rounded 14
        self.assertEqual(self.plugin.get_zoom_level(50000), 14)

    def test_get_zoom_level_clamping(self):
        """Test that zoom level is clamped between 0 and 21."""
        # Very large scale (small denominator)
        self.assertEqual(self.plugin.get_zoom_level(0.0001), 21)

        # Very small scale (large denominator)
        self.assertEqual(self.plugin.get_zoom_level(1e12), 0)

    def test_get_zoom_level_exception_handling(self):
        """Test that exceptions return the default fallback zoom level (12)."""
        # Passing None to math.log should raise a TypeError
        self.assertEqual(self.plugin.get_zoom_level(None), 12)

if __name__ == '__main__':
    unittest.main()
