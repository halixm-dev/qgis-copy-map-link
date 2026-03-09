import sys
from unittest.mock import MagicMock

# Mocking qgis.PyQt.QtWidgets
QtWidgets = MagicMock()
QtWidgets.QAction = MagicMock()
QtWidgets.QApplication = MagicMock()
QtWidgets.QMenu = MagicMock()

# Mocking qgis.core
core = MagicMock()
core.QgsProject = MagicMock()
core.QgsCoordinateReferenceSystem = MagicMock()
core.QgsCoordinateTransform = MagicMock()
core.QgsPointXY = MagicMock()
core.QgsMessageLog = MagicMock()
core.Qgis = MagicMock()

# Mocking the hierarchy
qgis = MagicMock()
qgis.PyQt = MagicMock()
qgis.PyQt.QtWidgets = QtWidgets
qgis.core = core

sys.modules['qgis'] = qgis
sys.modules['qgis.PyQt'] = qgis.PyQt
sys.modules['qgis.PyQt.QtWidgets'] = QtWidgets
sys.modules['qgis.core'] = core
