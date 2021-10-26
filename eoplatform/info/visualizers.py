from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from eoplatform.console import console
from typing import Any, cast


def visualize_band(object: Any, **kwargs) -> None:
    table: Table = Table(show_header=False, show_edge=False)
    table.add_column(justify="right")
    table.add_column(justify="left")
    table.add_row("Sensor", f"{object.sensor}")
    table.add_row(
        "Wavelength", f"{object.wavelength} {object.get_meta_unit(object,'wavelength')}"
    )
    table.add_row(
        "Resolution",
        f"{object.resolution} {object.get_meta_unit(object, 'resolution')}",
    )
    console.print(
        Panel(
            table,
            expand=False,
            title=f"[wheat4][bold]#{object.number} - {object.name}[/bold] [italic]({object.abbreviation})[/italic]",
        )
    )

    return None


def visualize_bands(object: Any, title: bool = False, **kwargs) -> None:
    def _generate_title(object) -> str:

        title: str = f"{str(len(object))} Band"
        if len(object) > 0:
            title += "s"

        return title

    table = Table(row_styles=["yellow", "cyan"])

    if title:
        table.title = object._generate_title()

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

    console.print(Panel(table, expand=False, title=_generate_title()))


def visualize_platform(object: Any, show_description: bool, **kwargs) -> None:
    print(object.__dict__)
    table = Table(
        show_header=False,
        show_lines=False,
        show_edge=False,
        expand=True,
        row_styles=["", "dim"],
    )

    table.add_column(justify="right", width=30)
    table.add_column(justify="left", width=30)
    table.add_row("Operator", f"{object.operator}")
    table.add_row("Constellation", f"{object.constellation}")
    table.add_row("Launch Date", f"{object.launch_date}")
    table.add_row("Regime", f"{object.regime}")
    table.add_row(
        "Orbit Time", f"{object.orbit_time} {object.get_meta_unit(object,'orbit_time')}"
    )

    if object.inclination:
        table.add_row(
            "Inclination",
            f"{object.inclination} {object.get_meta_unit(object,'inclination')}",
        )

    table.add_row(
        "Revisit Time",
        f"{object.revisit_time} {object.get_meta_unit(object,'revisit_time')}",
    )
    table.add_row(
        "Altitude", f"{object.altitude} {object.get_meta_unit(object, 'altitude')}"
    )
    table.add_row(
        "Scene Size",
        f"{object.scene_size} {object.get_meta_unit(object, 'scene_size')}",
    )
    Panel(
        f"""
        [wheat4 center][bold]{object.name}[/bold] [italic]({object.abbreviation})[/italic]
    
        """
    )

    band_table = object.bands.info(title=True)

    description: Text = Text("")
    if show_description:
        description = Text(object.description, justify="full", end="\n\n")

    group: Group = Group(Align.center(table), band_table, description, fit=False)
    panel: Panel = Panel(
        group,
        expand=False,
        title=f"[wheat4][bold]🛰️ {object.name}[/bold] [italic]({object.abbreviation})[/italic]",
        width=100,
    )
    if object.data_source:
        panel.subtitle = f"[blue underline][link={object.data_source}]Source[/link]"

    console.print(panel)
