import sys
from unittest.mock import MagicMock

def setup_qgis_mock():
    # Mock QGIS modules
    mock_qgis = MagicMock()
    mock_qgis_core = MagicMock()
    mock_qgis_gui = MagicMock()
    mock_pyqt = MagicMock()
    mock_pyqt_widgets = MagicMock()

    # Setup Qgis enum-like values
    mock_qgis_core.Qgis = MagicMock()
    mock_qgis_core.Qgis.Info = 0
    mock_qgis_core.Qgis.Warning = 1
    mock_qgis_core.Qgis.Critical = 2
    mock_qgis_core.Qgis.Success = 3

    # Inject into sys.modules
    sys.modules['qgis'] = mock_qgis
    sys.modules['qgis.core'] = mock_qgis_core
    sys.modules['qgis.gui'] = mock_qgis_gui
    sys.modules['qgis.PyQt'] = mock_pyqt
    sys.modules['qgis.PyQt.QtWidgets'] = mock_pyqt_widgets
    sys.modules['qgis.PyQt.QtCore'] = MagicMock()
    sys.modules['qgis.PyQt.QtGui'] = MagicMock()

    # Specific classes that might be needed
    mock_qgis_core.QgsProject = MagicMock()
    mock_qgis_core.QgsCoordinateReferenceSystem = MagicMock()
    mock_qgis_core.QgsCoordinateTransform = MagicMock()
    mock_qgis_core.QgsPointXY = MagicMock()
    mock_qgis_core.QgsMessageLog = MagicMock()

    mock_pyqt_widgets.QAction = MagicMock()
    mock_pyqt_widgets.QApplication = MagicMock()
    mock_pyqt_widgets.QMenu = MagicMock()

if 'qgis' not in sys.modules:
    setup_qgis_mock()
