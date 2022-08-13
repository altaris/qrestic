"""
Restic output models
"""
__docformat__ = "google"

import logging
from datetime import datetime
from typing import Iterator, List, Optional, Type, Union

from pydantic import BaseModel, Extra


class BackupOutput(BaseModel, extra=Extra.ignore):
    """Output line model for command `backup`"""

    message_type: str = ""
    action: str = ""
    seconds_elapsed: int = 0
    seconds_remaining: int = 0
    percent_done: float = 0
    total_files: int = 0
    files_done: int = 0
    total_bytes: int = 0
    bytes_done: int = 0
    current_files: List[str] = []

    # message_type = verbose_status
    item: str = ""
    duration: float = 0
    data_size: int = 0
    metadata_size: int = 0
    # total_files: int = 0

    # message_type = summary
    files_new: int = 0
    files_changed: int = 0
    files_unmodified: int = 0
    dirs_new: int = 0
    dirs_changed: int = 0
    dirs_unmodified: int = 0
    data_blobs: int = 0
    tree_blobs: int = 0
    data_added: int = 0
    total_files_processed: int = 0
    total_bytes_processed: int = 0
    total_duration: float = 0
    snapshot_id: str = ""


class ResticOutputIterator:
    """
    Iterates over a list of items that are either strings or `BaseModel`. If an
    item is not of type `_ModelClass`, an error is logged and the item is
    skipped.
    """

    _iterator: Iterator[Union[str, BaseModel]]
    _ModelClass: Type[BaseModel]

    def __init__(
        self,
        data: Union[str, BaseModel, List[BaseModel]],
        ModelClass: Type[BaseModel],
    ) -> None:
        if not isinstance(data, list):
            self._iterator = iter([data])
        else:
            self._iterator = iter(data)
        self._ModelClass = ModelClass

    def __iter__(self):
        return self

    def __next__(self) -> BaseModel:
        while True:
            item = next(self._iterator)
            if isinstance(item, self._ModelClass):
                return item
            if isinstance(item, str) and item.startswith("Fatal: "):
                logging.error("Restic error: %s", item[7:])
            else:
                logging.error(
                    "Error: invalid item of type %s :%s",
                    item.__class__.__name__,
                    str(item),
                )


class SnapshotsOutput(BaseModel, extra=Extra.ignore):
    """Output line model for command `snapshots`"""

    time: datetime = datetime(2000, 1, 1)
    parent: Optional[str] = None
    tree: str = ""
    paths: List[str] = []
    hostname: str = ""
    username: str = ""
    short_id: str = ""
