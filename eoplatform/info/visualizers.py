from dataclasses import dataclass
from dataclasses import fields
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from rich.console import Group
from rich.console import RenderableType
from rich.table import Table
from rich.text import Text


if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final


@dataclass
class ReturnRender:
    """Dataclass of visualization options dervied from `Band`, `Bands`, and `Platform`"""

    renderable: RenderableType
    title: Optional[str]
    subtitle: Optional[str]


class InfoVisualizers:
    @staticmethod
    def get_band_viz(object: Any, **kwargs: Any) -> ReturnRender:
        """Visualizer for `Band`"""

        table: Table = Table(show_header=False, show_edge=False)
        table.add_column(justify="right")
        table.add_column(justify="left")
        table.add_row("Sensor", f"{object.sensor}")
        table.add_row(
            "Wavelength",
            f"{object.wavelength} {object.get_meta_unit(object,'wavelength')}",
        )
        table.add_row(
            "Resolution",
            f"{object.resolution} {object.get_meta_unit(object, 'resolution')}",
        )

        title: str = f"[wheat4][bold]#{object.number} - {object.name}[/bold] [italic]({object.abbreviation})[/italic]"

        return ReturnRender(renderable=table, title=title, subtitle=None)

    @staticmethod
    def get_bands_viz(object: Any, **kwargs: Any) -> ReturnRender:
        """Visualizer for `Bands`"""

        table = Table(row_styles=["yellow", "cyan"])

        title: str = f"{str(len(object))} Band"
        if len(object) > 0:
            title += "s"

        table.add_column("Number", justify="right")
        table.add_column("Abbreviation", justify="left")
        table.add_column("Name")
        table.add_column(
            f"Resolution ({object.get_meta_unit(list(object.__dict__.values())[0],'resolution')})",
            justify="right",
        )
        table.add_column(
            f"Wavelength ({object.get_meta_unit(list(object.__dict__.values())[0],'wavelength')})",
            justify="right",
        )
        table.add_column("Sensor", justify="right")

        for band in object:
            table.add_row(
                str(band.number),
                str(band.abbreviation),
                str(band.name),
                str(band.resolution),
                str(band.wavelength),
                str(band.sensor),
            )

        return ReturnRender(renderable=table, title=title, subtitle=None)

    @staticmethod
    def get_platform_viz(
        object: Any, show_description: bool, **kwargs: Any
    ) -> ReturnRender:
        """Visualizer for `Platform`"""

        NO_PRINT_ATTRIBUTES: Final[List[str]] = [
            "description",
            "var_name",
            "abbreviation",
            "name",
            "bands",
            "data_source",
            "number_bands",
        ]

        table = Table(
            show_header=False,
            show_lines=False,
            show_edge=False,
            expand=True,
            row_styles=["", "dim"],
        )

        table.add_column(justify="right", width=30)
        table.add_column(justify="left", width=30)

        field_values: Dict[str, str] = {
            f.name: str(f.default)
            for f in fields(object)
            if f.name not in NO_PRINT_ATTRIBUTES
        }
        field_values = dict(sorted(field_values.items(), key=lambda kv: kv[0]))

        for name, value in field_values.items():

            table.add_row(
                name.capitalize().replace("_", " "),
                f"{value} {object.get_meta_unit(object,name)}",
            )

        description: Text = Text("")
        if show_description:
            description = Text(object.description, justify="full", end="\n\n")

        band_table: ReturnRender = InfoVisualizers.get_bands_viz(object.bands)

        group: Group = Group(table, band_table.renderable, description, fit=False)

        if object.data_source:
            subtitle: str = f"[blue underline][link={object.data_source}]Source[/link]"

        title: str = f"[wheat4][bold]🛰️ {object.name}[/bold] [italic]({object.abbreviation})[/italic]"

        return ReturnRender(renderable=group, title=title, subtitle=subtitle)
