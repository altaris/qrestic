"""
Configuration file utilities
"""
__docformat__ = "google"

from pathlib import Path

from pydantic import BaseModel


class RepositoryConfiguration(BaseModel):
    """Configuration schema for restic repository"""

    access_key: str
    password: str
    url: str
    secret_key: str


class ResticConfiguration(BaseModel):
    """Configuration schema for the restic invocation"""

    path: Path


class Configuration(BaseModel):
    """Global configuration schema"""

    repository: RepositoryConfiguration
    restic: ResticConfiguration
