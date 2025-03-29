import os
from pathlib import Path

from attrs import define, field


@define
class Folder:
    """A context manager to handle chdir transparently."""

    root: Path = field(converter=Path)
    original_dir: Path = field(init=False, converter=Path)

    def ensure_dir(self):
        self.root.mkdir(parents=True, exist_ok=True)

    def chdir(self):
        self.ensure_dir()

        self.original_dir = Path.cwd()
        os.chdir(self.root)

    def reset_dir(self):
        os.chdir(self.original_dir)

    def __enter__(self):
        self.chdir()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset_dir()
        return False

    def __truediv__(self, other: str | Path) -> "Folder":
        other = Path(other)
        return Folder(self.root / other)

    def __str__(self) -> str:
        return str(self.root)

    def __call__(self, subpath: str | Path) -> Path:
        return self.root / Path(subpath)
