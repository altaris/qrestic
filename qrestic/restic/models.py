"""
Restic output models
"""
__docformat__ = "google"

import logging
from datetime import datetime
from typing import Iterator, List, Optional, Type, Union

from pydantic import BaseModel, Extra


class ResticOutputIterator:
    """
    Iterates over a list of items that are either strings or `BaseModel`. If an
    item is not of type `_model_type`, an error is logged and the item is
    skipped.
    """

    _iterator: Iterator[Union[str, BaseModel]]
    _model_type: Type[BaseModel]

    def __init__(
        self,
        data: Union[str, BaseModel, List[BaseModel]],
        model_type: Type[BaseModel],
    ) -> None:
        if not isinstance(data, list):
            self._iterator = iter([data])
        else:
            self._iterator = iter(data)
        self._model_type = model_type

    def __iter__(self):
        return self

    def __next__(self) -> BaseModel:
        while True:
            item = next(self._iterator)
            if isinstance(item, self._model_type):
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
