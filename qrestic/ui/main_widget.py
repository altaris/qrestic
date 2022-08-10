"""
Main widget UI handler
"""

import logging

from pydantic import ValidationError
from PySide6.QtCore import QModelIndex, QStandardPaths, Slot
from PySide6.QtWidgets import QFileDialog, QHeaderView, QMessageBox, QWidget
from qrestic.configuration import Configuration
from qrestic.restic import Restic
from qrestic.restic.models import ResticOutputIterator, SnapshotsOutput
from qrestic.ui.main_widget_ui import Ui_MainWidget
from qrestic.ui.models import SnapshotsTableModel


class MainWidget(QWidget):
    """Main widget class"""

    _configuration: Configuration
    _restic: Restic
    _ui: Ui_MainWidget

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._ui = Ui_MainWidget()
        self._ui.setupUi(self)
        self._ui.w_operations.setEnabled(False)
        self._ui.pb_configuration_file.clicked.connect(
            self._on_pb_configuration_file_clicked
        )
        self._ui.pb_folder.clicked.connect(self._on_pb_folder_clicked)
        self._ui.pb_snapshots.clicked.connect(self._on_pb_snapshots_clicked)
        self._ui.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

    def _enable_operations(self):
        """Enables the `tab_widget` if all the conditions are met"""
        if self._ui.le_configuration_file.text() and self._ui.le_folder.text():
            self._ui.w_operations.setEnabled(True)

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
        if not path:
            return
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
        self._enable_operations()

    @Slot()
    def _on_pb_folder_clicked(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "Open folder",
            QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[
                0
            ],
        )
        if not path:
            return
        self._ui.le_folder.setText(path)
        self._enable_operations()

    @Slot()
    def _on_pb_snapshots_clicked(self):
        self._ui.table_view.setModel(SnapshotsTableModel())
        self._restic = Restic(self._configuration)
        self._restic.readyRead.connect(self._on_restic_ready_read_snapshots)
        self._restic.finished.connect(self._on_restic_finished)
        self._restic.snapshots()
        self._on_restic_started()

    @Slot()
    def _on_restic_finished(self):
        """The restic process has finished"""
        self._ui.w_buttons.setEnabled(True)
        self._ui.progress_bar.setValue(100)

    def _on_restic_started(self):
        """Call this when you start a restic process"""
        self._ui.w_buttons.setEnabled(False)
        self._ui.progress_bar.setValue(0)

    @Slot()
    def _on_restic_ready_read_snapshots(self):
        """The restic process emitted the `readyRead` signal"""
        data = self._restic.get_line()
        model = self._ui.table_view.model()
        for item in ResticOutputIterator(data, SnapshotsOutput):
            model.insertRow(0, QModelIndex())
            for i, col in enumerate(SnapshotsTableModel.FIELDS):
                index = model.createIndex(0, i)
                model.setData(index, getattr(item, col))
