import sys
from unittest.mock import MagicMock

# Mock the entire qgis module hierarchy
qgis = MagicMock()
sys.modules['qgis'] = qgis

pyqt = MagicMock()
sys.modules['qgis.PyQt'] = pyqt

qtwidgets = MagicMock()
sys.modules['qgis.PyQt.QtWidgets'] = qtwidgets

core = MagicMock()
sys.modules['qgis.core'] = core

# Setup QgsPointXY as a class that stores its arguments
class MockQgsPointXY:
    def __init__(self, x, y=None):
        if y is None: # Assuming it was passed a QgsPointXY or similar
             try:
                 self._x = x.x()
                 self._y = x.y()
             except AttributeError:
                 # Fallback for mock objects
                 self._x = 0.0
                 self._y = 0.0
        else:
             self._x = x
             self._y = y
    def x(self): return self._x
    def y(self): return self._y

core.QgsPointXY = MockQgsPointXY
core.QgsCoordinateReferenceSystem = MagicMock()
core.QgsCoordinateTransform = MagicMock()
core.QgsProject = MagicMock()
core.QgsMessageLog = MagicMock()
core.Qgis = MagicMock()
core.Qgis.Info = 0
core.Qgis.Warning = 1
core.Qgis.Critical = 2
core.Qgis.Success = 3
