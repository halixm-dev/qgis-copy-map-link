import sys
from unittest.mock import MagicMock

def mock_qgis():
    # Mock PyQt
    mock_pyqt = MagicMock()
    sys.modules["qgis.PyQt"] = mock_pyqt
    sys.modules["qgis.PyQt.QtWidgets"] = mock_pyqt.QtWidgets
    sys.modules["qgis.PyQt.QtCore"] = mock_pyqt.QtCore
    sys.modules["qgis.PyQt.QtGui"] = mock_pyqt.QtGui

    # Setup QApplication
    mock_pyqt.QtWidgets.QApplication = MagicMock()

    # Mock qgis.core
    mock_qgis_core = MagicMock()
    sys.modules["qgis.core"] = mock_qgis_core

    # Setup some basic classes
    class QgsPointXY:
        def __init__(self, x=0, y=0):
            if hasattr(x, 'x') and callable(x.x):
                self._x = x.x()
                self._y = x.y()
            else:
                self._x = x
                self._y = y
        def x(self): return self._x
        def y(self): return self._y

    mock_qgis_core.QgsPointXY = QgsPointXY

    # Track CRS instantiations
    crs_instantiation_count = 0

    class QgsCoordinateReferenceSystem:
        def __init__(self, authid=""):
            nonlocal crs_instantiation_count
            crs_instantiation_count += 1
            self.authid = authid
        def isValid(self):
            return True
        @staticmethod
        def get_count():
            return crs_instantiation_count
        @staticmethod
        def reset_count():
            nonlocal crs_instantiation_count
            crs_instantiation_count = 0

    mock_qgis_core.QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem

    # Other necessary classes
    mock_qgis_core.Qgis.Info = 0
    mock_qgis_core.Qgis.Warning = 1
    mock_qgis_core.Qgis.Critical = 2
    mock_qgis_core.Qgis.Success = 3

    return mock_qgis_core
