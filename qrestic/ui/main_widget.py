"""
Main widget UI handler
"""

import logging

from PySide6.QtCore import QStandardPaths, Slot
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget
from pydantic import ValidationError

from qrestic.ui.main_widget_ui import Ui_MainWidget

from qrestic.configuration import Configuration


class MainWidget(QWidget):
    """Main widget class"""

    _configuration: Configuration
    _ui: Ui_MainWidget

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._ui = Ui_MainWidget()
        self._ui.setupUi(self)
        self._ui.pb_configuration_file.clicked.connect(
            self._on_pb_configuration_file_clicked
        )

    @Slot()
    def _on_pb_configuration_file_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open configuration file",
            QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[
                0
            ],
            "JSON Files (*.json)",
        )
        logging.debug("Loading configuration file '%s'", path)
        try:
            self._configuration = Configuration.parse_file(path)
        except ValidationError:
            QMessageBox.critical(
                self,
                "Configuration error",
                f"File '{path}' is not a valid configuration file",
            )
            return
        self._ui.le_configuration_file.setText(path)
