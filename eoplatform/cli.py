from typing import cast

import typer

from eoplatform.baseClasses import Bands
from eoplatform.baseClasses import Platform
from eoplatform.console import console
from eoplatform.main import *
from eoplatform.main import EOP


app = typer.Typer()

@app.command("info")
def platform_info(
    name: str,
    only_bands: bool = typer.Option(False, "--only-bands /", "-b /"),
    show_description: bool = typer.Option(True, " /--no-description", " /-nd")) -> None:

    EOP.info(name=name, only_bands=only_bands, show_description=show_description)
    return None

@app.command("download")
def platform_download(name: str) -> None:
    
    EOP.download(name=name)
    return



if __name__ == "__main__":
    app()
