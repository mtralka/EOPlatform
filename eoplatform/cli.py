import typer

from eoplatform.main import *
from eoplatform.platforms.download.downloadControl import download
from eoplatform.platforms.info.info import info


app = typer.Typer()


@app.command("info")
def platform_info(
    name: str,
    only_bands: bool = typer.Option(False, "--only-bands /", "-b /"),
    show_description: bool = typer.Option(True, " /--no-description", " /-nd"),
) -> None:

    info(name=name, only_bands=only_bands, show_description=show_description)
    return None


@app.command("download")
def platform_download(name: str) -> None:

    download(name=name)
    return


if __name__ == "__main__":
    app()
