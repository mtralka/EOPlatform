from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from dataclasses import make_dataclass
import sys
import types
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sized
from typing import Tuple
from typing import Union
from typing import cast

from rich.panel import Panel

from eoplatform.console import console
from eoplatform.info.visualizers import ReturnRender


if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final

from eoplatform.info.visualizers import InfoVisualizers


class Base:
    @staticmethod
    def get_meta_unit(object: Any, attribute_name: str) -> str:
        return str(object.__dataclass_fields__[attribute_name].metadata["unit"])

    def info(self, show_description: bool = True, title: bool = False) -> None:

        VISUALIZERS: Final[dict] = {
            Band: InfoVisualizers.get_band_viz,
            Platform: InfoVisualizers.get_platform_viz,
        }

        # TODO fix typing so this works smoothly with `Bands`
        render: ReturnRender
        if isinstance(self, Bands):
            render = InfoVisualizers.get_bands_viz(
                self, show_description=show_description, title=title
            )
        else:
            render = VISUALIZERS[type(self)](
                self, show_description=show_description, title=title
            )

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
    wavelength: str = field(metadata={"unit": "um"})
    description: str
    sensor: str
    resolution: int = field(metadata={"unit": "m"})


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
    var_name: str = field(default="", init=False)
    operator: str
    bands_list: InitVar[List[Dict[str, Union[str, int]]]]
    description: str
    revisit_time: int = field(metadata={"unit": "days"})
    orbit_time: int = field(metadata={"unit": "minutes"})
    altitude: int = field(metadata={"unit": "km"})
    scene_size: Tuple[str, str] = field(metadata={"unit": "km"})
    regime: str
    constellation: str
    launch_date: str = field(metadata={"unit": "MM/DD/YYYY"})
    number_bands: Optional[int] = field(default=None, init=False)
    bands: Optional[Bands] = field(default=None, init=False)
    data_source: Optional[str] = field(default=None)
    inclination: Optional[str] = field(default=None, metadata={"unit": "deg"})

    def __post_init__(self, bands_list: List[Dict[str, Any]]) -> None:
        platform_bands: type = make_dataclass(
            "Bands",
            [(b["abbreviation"], Band, field(default=Band(**b))) for b in bands_list],  # type: ignore
            bases=(Bands,),
        )
        self.bands = platform_bands()
        self.number_bands = len(cast(Sized, self.bands))
        self.var_name = self.name.replace(" ", "").lower()

        return None

    def __len__(self) -> Optional[int]:
        return self.number_bands
