import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the current directory to sys.path so we can import the plugin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock QGIS modules
mock_qgis = MagicMock()
mock_pyqt = MagicMock()
sys.modules['qgis.PyQt.QtWidgets'] = mock_pyqt.QtWidgets
sys.modules['qgis.core'] = mock_qgis.core
sys.modules['qgis.utils'] = MagicMock()

# Import the plugin class after mocking
from copy_map_link_plugin import CopyMapLinkPlugin

class TestUnloadException(unittest.TestCase):
    def setUp(self):
        self.iface = MagicMock()
        self.canvas = MagicMock()
        self.iface.mapCanvas.return_value = self.canvas
        self.plugin = CopyMapLinkPlugin(self.iface)

    def test_unload_handles_typeerror(self):
        # Mock disconnect to raise TypeError (simulating signal not connected)
        self.canvas.contextMenuAboutToShow.disconnect.side_effect = TypeError("signal not connected")

        # This should not raise an exception because we're catching TypeError
        try:
            self.plugin.unload()
        except Exception as e:
            self.fail(f"unload() raised {type(e).__name__} unexpectedly!")

    def test_unload_raises_other_exceptions(self):
        # Mock disconnect to raise a different exception
        self.canvas.contextMenuAboutToShow.disconnect.side_effect = RuntimeError("Something went wrong")

        # This SHOULD raise RuntimeError because we only catch TypeError
        with self.assertRaises(RuntimeError):
            self.plugin.unload()

if __name__ == '__main__':
    unittest.main()
