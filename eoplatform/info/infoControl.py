from typing import Optional
from typing import cast

from eoplatform.baseClasses import Bands
from eoplatform.baseClasses import Platform
from eoplatform.console import console
from eoplatform.factory import EOPlatformFactory


def info(name: str, only_bands: bool = False, show_description: bool = True) -> None:

    platform: Optional[Platform] = EOPlatformFactory.generate_platform(
        name.lower().strip()
    )
    # walrus operator on 3.8+
    if not platform:
        console.print(
            f"[red bold encircle]:x:  '{name}' platform not supported\n[/][yellow]Check your spelling and try again"
        )
        return

    if only_bands:
        cast(Bands, platform.bands).info()
        return

    platform.info(show_description=show_description)
