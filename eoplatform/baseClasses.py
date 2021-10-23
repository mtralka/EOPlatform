from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sized
from typing import Tuple
from typing import Union
from typing import cast

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from eoplatform.console import console


def get_meta_unit(object: Any, attribute_name: str) -> str:
    return str(object.__dataclass_fields__[attribute_name].metadata["unit"])


@dataclass
class Band:
    number: int
    name: str
    abbreviation: str
    wavelength: str = field(metadata={"unit": "um"})
    description: str
    sensor: str
    resolution: int = field(metadata={"unit": "m"})

    def __str__(self) -> str:
        self.info()

        return ""

    def info(self) -> None:
        table: Table = Table(show_header=False, show_edge=False)
        table.add_column(justify="right")
        table.add_column(justify="left")
        table.add_row("Sensor", f"{self.sensor}")
        table.add_row(
            "Wavelength", f"{self.wavelength} {get_meta_unit(self,'wavelength')}"
        )
        table.add_row(
            "Resolution", f"{self.resolution} {get_meta_unit(self, 'resolution')}"
        )
        console.print(
            Panel(
                table,
                expand=False,
                title=f"[wheat4][bold]#{self.number} - {self.name}[/bold] [italic]({self.abbreviation})[/italic]",
            )
        )


@dataclass
class Bands:

    def info(self) -> None:
        table = self._as_table()
        console.print(Panel(table, expand=False, title=self._generate_title()))

    def _generate_title(self) -> str:

        title: str = f"{str(len(self))} Band"
        if len(self) > 0:
            title += "s"

        return title

    def _as_table(self, title: bool = False) -> Table:

        table = Table(row_styles=["yellow", "cyan"])

        if title:
            table.title = self._generate_title()

        table.add_column("Number", justify="right")
        table.add_column("Abbreviation", justify="left")
        table.add_column("Name")
        table.add_column(
            f"Resolution ({get_meta_unit(list(self.__dict__.values())[0],'resolution')})",
            justify="right",
        )
        table.add_column(
            f"Wavelength ({get_meta_unit(list(self.__dict__.values())[0],'wavelength')})",
            justify="right",
        )
        table.add_column("Sensor", justify="right")

        for band in self:
            table.add_row(
                str(band.number),
                str(band.abbreviation),
                str(band.name),
                str(band.resolution),
                str(band.wavelength),
                str(band.sensor),
            )

        return table

    def __len__(self) -> int:
        return len(self.__annotations__)

    def __str__(self) -> str:

        self.info()
        return ""

    def __iter__(self) -> Iterator[Band]:
        for band in self.__dict__.values():
            yield band


@dataclass()
class Platform:
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
            frozen=True,
            bases=(Bands,),
        )
        self.bands = platform_bands()
        self.number_bands = len(cast(Sized, self.bands))
        self.var_name = self.name.replace(" ", "")

        return None

    def info(self, show_description: bool = True) -> None:

        table = Table(
            show_header=False,
            show_lines=False,
            show_edge=False,
            expand=True,
            row_styles=["", "dim"],
        )

        table.add_column(justify="right", width=30)
        table.add_column(justify="left", width=30)
        table.add_row("Operator", f"{self.operator}")
        table.add_row("Constellation", f"{self.constellation}")
        table.add_row("Launch Date", f"{self.launch_date}")
        table.add_row("Regime", f"{self.regime}")
        table.add_row(
            "Orbit Time", f"{self.orbit_time} {get_meta_unit(self,'orbit_time')}"
        )

        if self.inclination:
            table.add_row(
            "Inclination", f"{self.inclination} {get_meta_unit(self,'inclination')}"
        )

        table.add_row(
            "Revisit Time", f"{self.revisit_time} {get_meta_unit(self,'revisit_time')}"
        )
        table.add_row("Altitude", f"{self.altitude} {get_meta_unit(self, 'altitude')}")
        table.add_row(
            "Scene Size", f"{self.scene_size} {get_meta_unit(self, 'scene_size')}"
        )
        Panel(
            f"""
            [wheat4 center][bold]{self.name}[/bold] [italic]({self.abbreviation})[/italic]
        
            """
        )

        band_table = cast(Bands, self.bands)._as_table(title=True)  

        description: Text = Text("")
        if show_description:
            description = Text(self.description, justify="full", end="\n\n")


        group: Group = Group(Align.center(table), band_table, description, fit=False)
        panel: Panel = Panel(
            group,
            expand=False,
            title=f"[wheat4][bold]🛰️ {self.name}[/bold] [italic]({self.abbreviation})[/italic]",
            width=100
        )
        if self.data_source:
            panel.subtitle = f"[blue underline][link={self.data_source}]Source[/link]"

        console.print(panel)

        return None

    def metadata(self, attribute_name: str) -> str:
        return str(self.__dataclass_fields__[attribute_name].metadata)  # type: ignore

    def __len__(self) -> Optional[int]:
        return self.number_bands

    def __str__(self) -> str:

        self.info()
        return ""
