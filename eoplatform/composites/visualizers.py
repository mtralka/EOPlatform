from dataclasses import fields
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import cast

from eoplatform.sharedClasses import ReturnRender
from rich.console import Group
from rich.console import RenderableType
from rich.table import Table
from rich.text import Text


if sys.version_info >= (3, 8, 0):
    from typing import Final  # type: ignore
else:
    from typing_extensions import Final


class CompositeVisualizers:
    @staticmethod
    def get_composite_viz(object: Any) -> ReturnRender:
        """Visualizer for `Composite`"""

        NO_PRINT_ATTRIBUTES: Final[List[str]] = [
            "abbreviation",
            "name",
            "reference",
            "description",
            "formula",
            "type",
            "bands",
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

        table.add_row(
            "Bands",
            ", ".join(list(object.bands)),
        )

        table.add_row(
            "Type",
            object.type.name.capitalize(),
        )

        table.add_row(
            "Formula",
            object.formula,
        )

        field_values: Dict[str, str] = {
            f.name: str(f.default)
            for f in fields(object)
            if f.name not in NO_PRINT_ATTRIBUTES
        }

        field_values = dict(sorted(field_values.items(), key=lambda kv: kv[0]))

        for name, value in field_values.items():

            table.add_row(
                name.capitalize().replace("_", " "),
                f"{value}",
            )

        description: Text = Text("")
        if object.description:
            description = Text(
                cast(str, object.description).strip(), justify="full", end="\n\n"
            )

        group: Group = Group(table, description, fit=True)

        subtitle: str = f"[blue underline][link={object.reference}]Source[/link]"

        title: str = f"[wheat4][bold] {object.name}[/bold] [italic]({object.abbreviation})[/italic]"

        return ReturnRender(renderable=group, title=title, subtitle=subtitle)
