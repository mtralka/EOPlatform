from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import Dict
from typing import Final
from typing import Iterator
from typing import Optional
from typing import Sized
from typing import cast

from eoplatform.console import console
from eoplatform.platforms.info.visualizers import InfoVisualizers
from eoplatform.shared_classes import ReturnRender
from rich.panel import Panel


class Base:
    @staticmethod
    def get_meta_unit(object: Any, attribute_name: str) -> str:
        return str(object.__dataclass_fields__[attribute_name].metadata.get("unit", ""))

    def info(self, show_description: bool = True, title: bool = False) -> None:

        VISUALIZERS: Final[Dict[type, Callable[..., ReturnRender]]] = {
            Band: InfoVisualizers.get_band_viz,
            Bands: InfoVisualizers.get_bands_viz,
            Platform: InfoVisualizers.get_platform_viz,
        }

        render: ReturnRender
        for k, v in VISUALIZERS.items():
            if isinstance(self, k):
                render = v(self, show_description=show_description, title=title)
                break

        console.print(
            Panel(
                render.renderable,
                expand=False,
                title=render.title,
                subtitle=render.subtitle,
                width=100,
            )
        )

        return None

    def __str__(self) -> str:
        self.info()
        return ""


@dataclass
class Band(Base):
    number: int
    name: str
    abbreviation: str
    wavelength: Optional[str] = field(metadata={"unit": "um"})
    description: Optional[str]
    sensor: Optional[str]
    resolution: Optional[int] = field(metadata={"unit": "m"})


@dataclass
class Bands(Base):
    def __len__(self) -> int:
        return len(self.__annotations__)

    def __iter__(self) -> Iterator[Band]:
        for band in self.__dict__.values():
            yield band


@dataclass()
class Platform(Base):
    abbreviation: str
    name: str
    var_name: str = field(default="NONE", init=False)
    number_bands: Optional[int] = field(default=None, init=False)
    bands: Optional[Bands] = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.var_name = self.name.replace(" ", "").lower()
        self.number_bands = len(cast(Sized, self.bands)) if self.bands else 0

        return None

    def __len__(self) -> Optional[int]:
        return self.number_bands
