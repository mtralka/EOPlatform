from eoplatform.baseClasses import Bands
from eoplatform.baseClasses import Platform
from eoplatform.console import console
from typing import cast
from eoplatform.platform import *


def info(name: str, only_bands: bool = False, show_description: bool = True) -> None:

    name: str = name.lower().strip()

    if name not in globals():
        console.print(
            f"[red bold encircle]:x:  '{name}' platform not supported\n[/][yellow]Check your spelling and try again"
        )
        return

    platform: Platform
    try:
        platform = globals()[name]
    except ValueError:
        raise NotImplementedError(f"{name} not implemented")

    if only_bands:
        cast(Bands, platform.bands).info()
        return

    platform.info(show_description=show_description)
