from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import Any
from typing import List
from typing import Optional
from typing import cast

from eoplatform.composites.safe_eval import safe_eval  # type: ignore[attr-defined]
from eoplatform.composites.visualizers import CompositeVisualizers
from eoplatform.console import console
from eoplatform.shared_classes import ReturnRender
from rich.panel import Panel


class CompositeType(Enum):
    VEGETATION = auto()
    BURN = auto()
    WATER = auto()
    SNOW = auto()
    DROUGHT = auto()
    URBAN = auto()
    KERNEL = auto()
    NONE = auto()


@dataclass
class Composite:
    abbreviation: str
    formula: str
    name: str
    reference: str
    description: Optional[str]
    type: CompositeType
    bands: List[str]

    def info(self) -> None:

        render: ReturnRender = CompositeVisualizers.get_composite_viz(self)

        console.print(
            Panel(
                render.renderable,
                expand=False,
                title=render.title,
                subtitle=render.subtitle,
            )
        )

        return None

    def create(self, **kwargs: Any) -> Any:

        for band in self.bands:
            if band not in kwargs:
                raise ValueError(f"{band} must be given as a kwarg")

        return safe_eval(self.formula, **kwargs)

    def __str__(self) -> str:
        self.info()
        return ""
