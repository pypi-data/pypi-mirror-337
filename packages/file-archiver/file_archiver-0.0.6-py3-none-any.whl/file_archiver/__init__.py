import importlib

__version__ = importlib.metadata.version("file_archiver")

from file_archiver.archive import Archive
from file_archiver.folder import Folder

__all__ = ["Archive", "Folder"]
