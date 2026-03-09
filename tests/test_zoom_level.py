import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock QGIS modules
sys.modules['qgis'] = MagicMock()
sys.modules['qgis.PyQt'] = MagicMock()
sys.modules['qgis.PyQt.QtWidgets'] = MagicMock()
sys.modules['qgis.core'] = MagicMock()
from qgis.core import Qgis

# Add current directory to path so we can import the plugin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from copy_map_link_plugin import CopyMapLinkPlugin

class TestZoomLevel(unittest.TestCase):
    def setUp(self):
        self.iface = MagicMock()
        self.plugin = CopyMapLinkPlugin(self.iface)

    def test_get_zoom_level_positive(self):
        # log2(591657550.5 / 50000) approx 13.53 -> round to 14
        self.assertEqual(self.plugin.get_zoom_level(50000), 14)
        # log2(591657550.5 / 1000000) approx 9.21 -> round to 9
        self.assertEqual(self.plugin.get_zoom_level(1000000), 9)

    def test_get_zoom_level_zero_or_negative(self):
        self.assertEqual(self.plugin.get_zoom_level(0), 0)
        self.assertEqual(self.plugin.get_zoom_level(-100), 0)

    def test_get_zoom_level_clamping(self):
        # Very large scale should clamp to 0
        self.assertEqual(self.plugin.get_zoom_level(1e12), 0)
        # Very small scale should clamp to 21
        self.assertEqual(self.plugin.get_zoom_level(1), 21)

if __name__ == '__main__':
    unittest.main()
