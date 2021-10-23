from typing import cast

import typer

from eoplatform.baseClasses import Bands
from eoplatform.baseClasses import Platform
from eoplatform.console import console
from eoplatform.main import *


app = typer.Typer()

@app.command("info")
def platform_info(
    name: str,
    only_bands: bool = typer.Option(False, "--bands/", "-b/"),
    show_description: bool = typer.Option(True, "--description/--no-description", "-d/-nd")) -> None:

    if name not in globals():
        console.print(f"[red bold encircle]:x:  '{name}' platform not supported\n[/][yellow]Check your spelling and try again")
        return

    platform: Platform
    try:
        platform = globals()[name]
    except ValueError:
        raise NotImplementedError(f"{name} not implemented")

    if only_bands:
        cast(Bands,platform.bands).info()
        return

    platform.info(show_description=show_description)

@app.command("download")
def platform_download(platform: str) -> None:
    console.print("[red bold encircle]:x:  downloading not yet implemented. Stay tuned!")
    return



if __name__ == "__main__":
    app()
