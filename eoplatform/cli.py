import typer

from eoplatform.main import info
from eoplatform.platforms.download.downloadControl import download


app = typer.Typer()


@app.command("info")
def info_controller(
    name: str,
    only_bands: bool = typer.Option(False, "--only-bands /", "-b /"),
    show_description: bool = typer.Option(True, " /--no-description", " /-nd"),
) -> None:

    info(
        name=name.upper().strip(),
        only_bands=only_bands,
        show_description=show_description,
    )
    return None


@app.command("download")
def platform_download(name: str) -> None:

    download(name=name)
    return


if __name__ == "__main__":
    app()
