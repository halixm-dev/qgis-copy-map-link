import sys
from unittest.mock import MagicMock

def mock_qgis():
    """Mocks the qgis and PyQt modules for testing in environments where QGIS is not installed."""
    mock_qt_widgets = MagicMock()
    mock_qt_gui = MagicMock()
    mock_qt_core = MagicMock()
    mock_qgis_core = MagicMock()
    mock_qgis_gui = MagicMock()

    sys.modules["qgis"] = MagicMock()
    sys.modules["qgis.PyQt"] = MagicMock()
    sys.modules["qgis.PyQt.QtWidgets"] = mock_qt_widgets
    sys.modules["qgis.PyQt.QtGui"] = mock_qt_gui
    sys.modules["qgis.PyQt.QtCore"] = mock_qt_core
    sys.modules["qgis.core"] = mock_qgis_core
    sys.modules["qgis.gui"] = mock_qgis_gui

    # Common classes/enums needed for the plugin
    mock_qgis_core.Qgis = MagicMock()
    mock_qgis_core.QgsProject = MagicMock()
    mock_qgis_core.QgsCoordinateReferenceSystem = MagicMock()
    mock_qgis_core.QgsCoordinateTransform = MagicMock()
    mock_qgis_core.QgsPointXY = MagicMock()
    mock_qgis_core.QgsMessageLog = MagicMock()

    return {
        "QtWidgets": mock_qt_widgets,
        "QtGui": mock_qt_gui,
        "QtCore": mock_qt_core,
        "QgisCore": mock_qgis_core,
        "QgisGui": mock_qgis_gui,
    }
