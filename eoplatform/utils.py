from importlib import resources
from pathlib import Path
import sys

if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final

ROOT_DIR: Final[Path]
with resources.path("eoplatform", "__main__.py") as file:
    ROOT_DIR = file.parent

PLATFORMS_DIR: Final[Path] = ROOT_DIR / "platforms"
