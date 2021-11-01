from importlib import resources
from pathlib import Path
from typing import Final


with resources.path("eoplatform", "__main__.py") as file:
    ROOT_DIR: Final[Path] = file.parent

PLATFORMS_DIR: Final[Path] = ROOT_DIR / "data" / "platforms"

COMPOSITES_DIR: Final[Path] = ROOT_DIR / "data" / "composites"
