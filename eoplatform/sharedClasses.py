from dataclasses import dataclass
from rich.console import RenderableType
from typing import Optional


@dataclass
class ReturnRender:
    """Dataclass of visualization options dervied from `Band`, `Bands`, and `Platform`"""

    renderable: RenderableType
    title: Optional[str]
    subtitle: Optional[str]
