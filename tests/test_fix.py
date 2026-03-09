import unittest
import sys
from unittest.mock import MagicMock, patch

# Mock the QGIS and PyQt modules before importing the plugin
mock_qgis = MagicMock()
mock_pyqt = MagicMock()

sys.modules['qgis'] = mock_qgis
sys.modules['qgis.core'] = mock_qgis.core
sys.modules['qgis.PyQt'] = mock_pyqt
sys.modules['qgis.PyQt.QtWidgets'] = mock_pyqt.QtWidgets
sys.modules['qgis.PyQt.QtCore'] = mock_pyqt.QtCore

# Define necessary constants and classes for mocking
mock_qgis.core.Qgis.Info = 0
mock_qgis.core.Qgis.Warning = 1
mock_qgis.core.Qgis.Critical = 2
mock_qgis.core.Qgis.Success = 3

class MockQgsPointXY:
    def __init__(self, *args):
        self.args = args
mock_qgis.core.QgsPointXY = MockQgsPointXY

class MockQgsMessageLog:
    @staticmethod
    def logMessage(msg, tag, level):
        pass
mock_qgis.core.QgsMessageLog = MockQgsMessageLog

# Now import the plugin class
from copy_map_link_plugin import CopyMapLinkPlugin

class TestGlobalStateFix(unittest.TestCase):
    def test_isolated_state(self):
        # Create two separate iface mocks
        iface1 = MagicMock()
        iface2 = MagicMock()

        # Instantiate the plugin twice
        plugin1 = CopyMapLinkPlugin(iface1)
        plugin2 = CopyMapLinkPlugin(iface2)

        # Verify initial state
        self.assertIsNone(plugin1.clicked_point_canvas_crs)
        self.assertIsNone(plugin2.clicked_point_canvas_crs)
        self.assertEqual(plugin1.iface, iface1)
        self.assertEqual(plugin2.iface, iface2)

        # Simulate context menu event for plugin1
        event1 = MagicMock()
        event1.mapPoint.return_value = "Point1"
        menu1 = MagicMock()
        plugin1.prepare_canvas_context_menu(menu1, event1)

        # Verify plugin1's state is updated and plugin2's remains unchanged
        self.assertIsNotNone(plugin1.clicked_point_canvas_crs)
        self.assertIsNone(plugin2.clicked_point_canvas_crs)

        # Simulate context menu event for plugin2
        event2 = MagicMock()
        event2.mapPoint.return_value = "Point2"
        menu2 = MagicMock()
        plugin2.prepare_canvas_context_menu(menu2, event2)

        # Verify both have their own state
        self.assertIsNotNone(plugin1.clicked_point_canvas_crs)
        self.assertIsNotNone(plugin2.clicked_point_canvas_crs)
        self.assertNotEqual(plugin1.clicked_point_canvas_crs, plugin2.clicked_point_canvas_crs)

        # Simulate copy link for plugin1 (which should reset its clicked_point_canvas_crs)
        with patch('copy_map_link_plugin.QApplication'):
            # Mock the parts needed for copy_link to not crash
            plugin1.canvas.mapSettings().destinationCrs().isValid.return_value = True
            plugin1.copy_link("https://maps.com/{lat},{lon}")

        self.assertIsNone(plugin1.clicked_point_canvas_crs)
        self.assertIsNotNone(plugin2.clicked_point_canvas_crs)

if __name__ == '__main__':
    unittest.main()
