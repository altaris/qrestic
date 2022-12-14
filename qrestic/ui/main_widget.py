"""
Main widget UI handler
"""

import logging
from pathlib import Path
from typing import Callable, Type, Union

from pydantic import ValidationError
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QStandardPaths,
    Slot,
)
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFileDialog, QHeaderView, QMessageBox, QWidget
from qrestic.configuration import Configuration
from qrestic.restic import Restic
from qrestic.restic.models import (
    BackupOutput,
    ResticOutputIterator,
    SnapshotsOutput,
)
from qrestic.ui.main_widget_ui import Ui_MainWidget

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from qrestic.ui.models import *


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
        self._ui.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self._ui.progress_bar_busy.setVisible(False)
        # pylint: disable=no-member
        self._ui.pb_configuration_file.clicked.connect(
            self._on_pb_configuration_file_clicked
        )
        self._ui.pb_folder.clicked.connect(self._on_pb_folder_clicked)
        self._ui.pb_init.clicked.connect(self._on_pb_init_clicked)
        self._ui.pb_backup.clicked.connect(self._on_pb_backup_clicked)
        self._ui.pb_restore.clicked.connect(self._on_pb_restore_clicked)
        self._ui.pb_snapshots.clicked.connect(self._on_pb_snapshots_clicked)
        self._ui.progress_bar.valueChanged.connect(
            self._on_progress_bar_value_changed
        )

    def _append_raw_log(self, text: str):
        """Appends text to `_ui.te_raw`"""
        if not text:
            return
        logging.debug("%s", text)
        if not self._ui.te_raw.toPlainText():
            self._ui.te_raw.append(text)
        else:
            self._ui.te_raw.append("\n" + text)

    def _enable_operation_widgets(self):
        """Enables the `tab_widget` if all the conditions are met"""
        if self._ui.le_configuration_file.text() and self._ui.le_folder.text():
            self._ui.w_operations.setEnabled(True)

    def _new_restic_process(
        self,
        TableModelClass: Optional[Type[QAbstractTableModel]],
        on_ready_read_slot: Callable,
    ) -> Restic:
        """
        Sets `_restic` to a new restic process handler and connect it to the
        relevant slots. Also reinitializes the table model.
        """
        self._ui.table_view.setModel(
            None if TableModelClass is None else TableModelClass()
        )
        self._restic = Restic(self._configuration)
        # pylint: disable=no-member
        self._restic.started.connect(self._on_restic_started)  # type: ignore
        self._restic.readyRead.connect(on_ready_read_slot)  # type: ignore
        self._restic.finished.connect(self._on_restic_finished)  # type: ignore
        return self._restic

    @Slot()
    def _on_pb_backup_clicked(self):
        self._ui.tab_widget.setCurrentIndex(0)
        restic = self._new_restic_process(
            BackupTableModel, self._on_restic_ready_read_backup
        )
        restic.backup(self._ui.le_folder.text())

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
        try:
            self.load_configuration(path)
        except ValidationError as e:
            logging.error("Invalid configuration file: %s", e)
            QMessageBox.critical(
                self,
                "Configuration error",
                f"File '{path}' is not a valid configuration file",
            )
            return

    @Slot()
    def _on_pb_folder_clicked(self):
        path = QFileDialog.getExistingDirectory(
            self,
            self.tr("Open folder"),
            QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[
                0
            ],
        )
        if not path:
            return

    @Slot()
    def _on_pb_init_clicked(self):
        self._ui.tab_widget.setCurrentIndex(1)
        restic = self._new_restic_process(None, self._on_restic_ready_read_raw)
        restic.init()

    @Slot()
    def _on_pb_restore_clicked(self):
        self._ui.tab_widget.setCurrentIndex(1)
        restic = self._new_restic_process(None, self._on_restic_ready_read_raw)
        restic.restore("latest", self._ui.le_folder.text())

    @Slot()
    def _on_pb_snapshots_clicked(self):
        self._ui.tab_widget.setCurrentIndex(0)
        restic = self._new_restic_process(
            SnapshotsTableModel, self._on_restic_ready_read_snapshots
        )
        restic.snapshots()

    @Slot()
    def _on_progress_bar_value_changed(self):
        """
        When the progress bar value changes, hide `_ui.progress_bar_bury`, and
        make `_ui.progress_bar` visible.
        """
        self._ui.progress_bar.setVisible(True)
        self._ui.progress_bar_busy.setVisible(False)

    @Slot()
    def _on_restic_finished(self):
        """The restic process has finished"""
        self.setCursor(QCursor(Qt.ArrowCursor))
        self._ui.w_buttons.setEnabled(True)
        self._ui.w_conf.setEnabled(True)
        # This automatically hides the busy progress bar
        self._ui.progress_bar.setValue(100)

    @Slot()
    def _on_restic_started(self):
        self.setCursor(QCursor(Qt.BusyCursor))
        self._ui.w_buttons.setEnabled(False)
        self._ui.w_conf.setEnabled(False)
        self._ui.progress_bar.setValue(0)
        self._ui.progress_bar.setVisible(False)
        self._ui.progress_bar_busy.setVisible(True)
        self._ui.te_raw.setText("")

    @Slot()
    def _on_restic_ready_read_backup(self):
        """
        The restic process is running the `backup` command and emitted the
        `readyRead` signal.
        """
        items = self._restic.get_items(BackupOutput)
        model = self._ui.table_view.model()
        for item in ResticOutputIterator(items, BackupOutput):
            assert isinstance(item, BackupOutput)
            if item.message_type == "status":
                self._ui.progress_bar.setValue(int(item.percent_done * 100))
            elif item.message_type == "summary":
                logging.info(
                    (
                        "Backup complete. New %d, changed %d, processed %d "
                        "(%d bytes), duration %d"
                    ),
                    item.files_new,
                    item.files_changed,
                    item.total_files_processed,
                    item.total_bytes_processed,
                    item.total_duration,
                )
                tr = self.tr
                QMessageBox.information(
                    self,
                    tr("Backup complete"),
                    (
                        tr("Backup complete.")
                        + "\n"
                        + tr("New files: ")
                        + str(item.files_new)
                        + "\n"
                        + tr("Modified files: ")
                        + str(item.files_changed)
                        + "\n"
                        + tr("Processed files: ")
                        + str(item.total_files_processed)
                        + "\n"
                        + tr("Processed bytes: ")
                        + str(item.total_bytes_processed)
                        + "\n"
                        + tr("New directories: ")
                        + str(item.dirs_new)
                        + "\n"
                        + tr("Modified directories: ")
                        + str(item.dirs_changed)
                        + "\n"
                        + tr("Total duration: ")
                        + str(int(item.total_duration))
                        + tr(" seconds")
                    ),
                )
            elif item.message_type == "verbose_status":
                model.insertRow(0, QModelIndex())
                for i, col in enumerate(BackupTableModel.FIELDS):
                    index = model.createIndex(0, i)
                    model.setData(index, getattr(item, col))

    @Slot()
    def _on_restic_ready_read_raw(self):
        """
        The restic process is running the `init` command and emitted the
        `readyRead` signal.
        """
        for item in self._restic.get_items():
            # item should be a string anyway
            self._append_raw_log(str(item))

    @Slot()
    def _on_restic_ready_read_snapshots(self):
        """
        The restic process is running the `snapshots` command and emitted the
        `readyRead` signal.
        """
        items = self._restic.get_items(SnapshotsOutput)
        model = self._ui.table_view.model()
        for item in ResticOutputIterator(items, SnapshotsOutput):
            model.insertRow(0, QModelIndex())
            for i, col in enumerate(SnapshotsTableModel.FIELDS):
                index = model.createIndex(0, i)
                model.setData(index, getattr(item, col))

    def load_configuration(self, path: Union[Path, str]):
        """
        Loads a configuration file, and sets the path in UI if successful. If
        the configuration specifies a folder (`folder` key), then it is set in
        UI. Also calls `MainWidget._enable_operation_widgets`.
        """
        self._configuration = Configuration.parse_file(path)
        self._ui.le_configuration_file.setText(str(path))
        logging.info(
            "Loaded configuration file '%s': %s", path, self._configuration
        )
        if self._configuration.folder is not None:
            self._ui.le_folder.setText(str(self._configuration.folder))
            logging.info("Selected folder %s", self._configuration.folder)
        self._enable_operation_widgets()
