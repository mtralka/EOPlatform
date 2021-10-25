from typing import Union
from typing import cast

from eoplatform.baseClasses import Bands
from eoplatform.baseClasses import Platform
from eoplatform.console import console
from eoplatform.factory import EOPlatformFactory as factory


for platform in factory.generate_platform():
    locals()[platform.var_name] = platform


def info(name: str, only_bands: bool = False, show_description: bool = True) -> None:

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


def download(name: str) -> None:
    console.print(
        "[red bold encircle]:x:  downloading not yet implemented. Stay tuned!"
    )
    return
