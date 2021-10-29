from typing import Optional
from typing import cast

from eoplatform.composites.baseClasses import Composite
from eoplatform.composites.factory import EOCompositeFactory
from eoplatform.console import console


def info(name: str) -> None:

    composite: Optional[Composite] = EOCompositeFactory.generate_composite(
        name.upper().strip()
    )
    # walrus operator on 3.8+
    if not composite:
        console.print(
            f"[red bold encircle]:x:  '{name}' composite not supported\n[/][yellow]Check your spelling and try again"
        )
        return

    composite.info()
