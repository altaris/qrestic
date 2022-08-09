"""
Configuration file utilities
"""
__docformat__ = "google"

from pydantic import BaseModel


class ResticConfiguration(BaseModel):
    """Configuration schema for restic repository"""

    access_key: str
    password: str
    repository: str
    sectet_key: str


class Configuration(BaseModel):
    """Global configuration schema"""

    restic: ResticConfiguration
