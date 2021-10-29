from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import List
from typing import Optional

from eoplatform.composites.visualizers import CompositeVisualizers
from eoplatform.console import console
from eoplatform.sharedClasses import ReturnRender
import numpy as np
import numpy.typing as npt
from rich.panel import Panel


class CompositeType(Enum):
    VEGETATION = auto()
    BURN = auto()
    WATER = auto()
    SNOW = auto()
    DROUGHT = auto()
    URBAN = auto()
    KERNEL = auto()


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

    @classmethod
    def create(cls, **kwargs: npt.NDArray) -> None:  # type: ignore[type-arg]
        f"""
        {cls.__doc__}
        """
        for band in cls.bands:
            if band not in kwargs:
                raise ValueError(f"{band} must be given as a kwarg")

        eval(cls.formula, {}, kwargs)

        ...

    def __str__(self) -> str:
        self.info()
        return ""
