"""
Models for the main widget's table view
"""

import logging
from typing import Any, List, Tuple, Type, Union

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QPersistentModelIndex,
    QModelIndex,
)
from PySide6.QtGui import QColor
from pydantic import BaseModel

from qrestic.restic.models import RawOutput, SnapshotsOutput

_Index = Union[QModelIndex, QPersistentModelIndex]


def _make_table_model(
    model_type: Type[BaseModel], fields: List[Tuple[str, str]]
) -> Type[QAbstractTableModel]:
    """
    Creates a `QAbstractTableModel` type for a given `BaseModel` type. The
    fields (in the form of a field name and a display string tuple) that will
    be used as columns must be listed in order.
    """

    class _TableModel(QAbstractTableModel):

        FIELDS: List[str] = [f[0] for f in fields]
        """Field names"""

        FIELD_DISPLAY_NAMES: List[str] = [f[1] for f in fields]
        """Field display names to use for the header of the table view"""

        MODEL_TYPE: Type[BaseModel] = model_type

        _data: List[BaseModel]

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self._data = []

        def _index_valid(self, index: _Index) -> bool:
            return (
                index.isValid()
                and 0 <= index.column() < len(self.FIELDS)
                and 0 <= index.row() < len(self._data)
            )

        def columnCount(self, _: _Index = QModelIndex()) -> int:
            """Override"""
            return len(self.FIELDS)

        def data(self, index: _Index, role: int = Qt.DisplayRole) -> Any:
            """Override"""
            if not self._index_valid(index):
                return None
            if role == Qt.DisplayRole:
                column, row = index.column(), index.row()
                return str(getattr(self._data[row], self.FIELDS[column]))
            if role == Qt.BackgroundRole:
                return QColor(Qt.white)
            return None  # role == Qt.TextAlignmentRole

        def headerData(
            self,
            section: int,
            orientation: Qt.Orientation,
            role: int = Qt.DisplayRole,
        ) -> Any:
            if role != Qt.DisplayRole:
                return None
            if orientation == Qt.Horizontal:
                return self.FIELD_DISPLAY_NAMES[section]
            return str(section)

        def insertRows(
            self, row: int, count: int, parent: _Index = QModelIndex()
        ) -> bool:
            """Override"""
            self.beginInsertRows(parent, row, row + count - 1)
            for i in range(count):
                self._data.insert(row + i, self.MODEL_TYPE())
            self.endInsertRows()
            return True

        def rowCount(self, _: _Index = QModelIndex()) -> int:
            """Override"""
            return len(self._data)

        def setData(
            self,
            index: _Index,
            value: Any,
            role: int = Qt.EditRole,
        ) -> bool:
            """Override"""
            if not (self._index_valid(index) and role == Qt.EditRole):
                return False
            column, row = index.column(), index.row()
            try:
                setattr(self._data[row], self.FIELDS[column], value)
            except Exception as e:  # pylint: disable=broad-except
                logging.error(
                    "Couldn't update index (%d, %d): %s", row, column, e
                )
                return False
            return True

    return _TableModel


InitTableModel = _make_table_model(RawOutput, [("output", "Output")])
SnapshotsTableModel = _make_table_model(
    SnapshotsOutput,
    [
        ("time", "Time"),
        ("short_id", "ID"),
        ("username", "User"),
        ("hostname", "Host"),
        ("paths", "Paths"),
    ],
)
