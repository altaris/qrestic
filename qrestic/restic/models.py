"""
Restic output models
"""
__docformat__ = "google"

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra


class SnapshotsOutput(BaseModel, extra=Extra.ignore):
    """Output line model for command `snapshots`"""

    time: datetime
    parent: Optional[str]
    tree: str
    paths: List[str]
    hostname: str
    username: str
    short_id: str
