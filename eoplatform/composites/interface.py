from typing import Optional

from eoplatform.composites.classes import Composite
from eoplatform.composites.factory import generate_composite
from eoplatform.console import console


def info(name: str) -> None:

    composite: Optional[Composite] = generate_composite(name.upper().strip())

    if not composite:
        console.print(
            f"[red bold encircle]:x:  '{name}' composite not supported\n[/][yellow]Check your spelling and try again"
        )
        return

    composite.info()
