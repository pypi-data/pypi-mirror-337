"""
SHM Reader - A general-purpose shared memory reader SDK for Python.

This module provides functionality to list, read, and monitor shared memory segments.
It allows for custom data format parsing through a parser registration system.
"""

from .core import ShmReader, SharedMemorySegment

__version__ = "0.1.0"
__all__ = ["ShmReader", "SharedMemorySegment"] 