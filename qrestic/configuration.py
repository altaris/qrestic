"""
Configuration file utilities
"""
__docformat__ = "google"

from pathlib import Path

from pydantic import BaseModel, SecretStr


class RepositoryConfiguration(BaseModel):
    """Configuration schema for restic repository"""

    access_key: str
    password: SecretStr
    url: str
    secret_key: SecretStr


class ResticConfiguration(BaseModel):
    """Configuration schema for the restic invocation"""

    path: Path


class Configuration(BaseModel):
    """Global configuration schema"""

    repository: RepositoryConfiguration
    restic: ResticConfiguration
