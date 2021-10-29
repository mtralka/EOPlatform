from eoplatform.composites.factory import EOCompositeFactory as CompositeFactory
from eoplatform.composites.interface import info as composite_info
from eoplatform.console import console
from eoplatform.platforms.factory import EOPlatformFactory as PlatformFactory
from eoplatform.platforms.interface import info as platform_info


def info(name: str, only_bands: bool = False, show_description: bool = True) -> None:

    name = name.upper().strip()

    if name in PlatformFactory.find_platform_names():
        platform_info(
            name=name, only_bands=only_bands, show_description=show_description
        )

    elif name in CompositeFactory.find_composite_names():
        composite_info(name=name)

    else:
        console.print(
            f"[red bold encircle]:x:  '{name}' not recognized\n[/][yellow]Check your spelling and try again"
        )

    return None
