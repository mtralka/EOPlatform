from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import Optional

from rich.console import RenderableType


@dataclass
class ReturnRender:
    """Dataclass of visualization options dervied from `Band`, `Bands`, and `Platform`"""

    renderable: RenderableType
    title: Optional[str]
    subtitle: Optional[str]


class AutoImport(Enum):
    YES = auto()
    NO = auto()


class AutoImportControl:
    def __init__(self) -> None:
        self._status: AutoImport = AutoImport.YES

    @property
    def status(self) -> AutoImport:
        return self._status

    def set_status(self, status: AutoImport) -> None:

        if not isinstance(status, AutoImport):
            raise ValueError("Incorrect value ", status)

        self._status = status

        return None
