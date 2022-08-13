"""
Main widget UI handler
"""

import logging
from typing import Callable, Type

from pydantic import ValidationError
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QStandardPaths,
    Slot,
)
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

        # pylint: disable=no-member
        self._ui.pb_configuration_file.clicked.connect(
            self._on_pb_configuration_file_clicked
        )
        self._ui.pb_folder.clicked.connect(self._on_pb_folder_clicked)
        self._ui.pb_init.clicked.connect(self._on_pb_init_clicked)
        self._ui.pb_backup.clicked.connect(self._on_pb_backup_clicked)
        self._ui.pb_restore.clicked.connect(self._on_pb_restore_clicked)
        self._ui.pb_search.clicked.connect(self._on_pb_search_clicked)
        self._ui.pb_snapshots.clicked.connect(self._on_pb_snapshots_clicked)

    def _append_raw_log(self, text: str):
        """Appends text to `_ui.te_raw`"""
        if not text:
            return
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
        self._enable_operation_widgets()

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
        self._enable_operation_widgets()

    @Slot()
    def _on_pb_init_clicked(self):
        self._ui.tab_widget.setCurrentIndex(1)
        restic = self._new_restic_process(
            None, self._on_restic_ready_read_init
        )
        restic.init()

    @Slot()
    def _on_pb_restore_clicked(self):
        self._ui.tab_widget.setCurrentIndex(0)

    @Slot()
    def _on_pb_search_clicked(self):
        self._ui.tab_widget.setCurrentIndex(0)

    @Slot()
    def _on_pb_snapshots_clicked(self):
        self._ui.tab_widget.setCurrentIndex(0)
        restic = self._new_restic_process(
            SnapshotsTableModel, self._on_restic_ready_read_snapshots
        )
        restic.snapshots()

    @Slot()
    def _on_restic_finished(self):
        """The restic process has finished"""
        self._ui.w_buttons.setEnabled(True)
        self._ui.progress_bar.setValue(100)
        while line := self._restic.readLine():
            print(line)

    @Slot()
    def _on_restic_started(self):
        self._ui.w_buttons.setEnabled(False)
        self._ui.progress_bar.setValue(0)
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
                QMessageBox.information(
                    self,
                    "Backup complete",
                    (
                        "Backup complete.\n"
                        f"New files: {item.files_new}\n"
                        f"Modified files: {item.files_changed}\n"
                        # f"Unmodified files: {item.files_unmodified}\n"
                        f"Processed files: {item.total_files_processed}\n"
                        f"Processed bytes: {item.total_bytes_processed}\n"
                        f"New directories: {item.dirs_new}\n"
                        f"Modified directories: {item.dirs_changed}\n"
                        # f"Unmodified directories: {item.dirs_unmodified}\n"
                        f"Total duration: {int(item.total_duration)} seconds"
                    ),
                )
            elif item.message_type == "verbose_status":
                model.insertRow(0, QModelIndex())
                for i, col in enumerate(BackupTableModel.FIELDS):
                    index = model.createIndex(0, i)
                    model.setData(index, getattr(item, col))

    @Slot()
    def _on_restic_ready_read_init(self):
        """
        The restic process is running the `init` command and emitted the
        `readyRead` signal.
        """
        for item in self._restic.get_items():
            # item should be a string anyway
            self._append_raw_log(str(item))

    @Slot()
    def _on_restic_ready_read_restore(self):
        """
        The restic process is running the `restore` command and emitted the
        `readyRead` signal.
        """

    @Slot()
    def _on_restic_ready_read_search(self):
        """
        The restic process is running the `search` command and emitted the
        `readyRead` signal.
        """

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
