"""Chillet - Asynchronous and synchronous clients for interacting with the Palworld REST API."""

__version__ = "1.0.0"
__author__ = "domi2k"
__license__ = "MIT"

from .clients import (
    AsyncPalworldClient,
    PalworldClient,
)

__all__ = [
    "AsyncPalworldClient",
    "PalworldClient",
]
