from typing import Optional
from typing import cast

from eoplatform.console import console
from eoplatform.platforms.classes import Bands
from eoplatform.platforms.classes import Platform
from eoplatform.platforms.factory import generate_platform


def info(name: str, only_bands: bool = False, show_description: bool = True) -> None:

    platform: Optional[Platform] = generate_platform(name.upper().strip())

    if platform is None:

        console.print(
            f"[red bold encircle]:x:  '{name}' platform not supported\n[/][yellow]Check your spelling and try again"
        )
        return

    if only_bands:
        cast(Bands, platform.bands).info()
        return

    platform.info(show_description=show_description)
