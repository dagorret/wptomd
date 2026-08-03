from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .converter import convert_html_file

app = typer.Typer(
    help="Convierte HTML exportado desde WordPress en Markdown limpio."
)

console = Console()


@app.command()
def convert(
    source: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Archivo HTML de entrada.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Archivo Markdown de salida.",
    ),
) -> None:
    """
    Convierte un archivo HTML individual.
    """
    destination = output or Path("output") / f"{source.stem}.md"

    try:
        convert_html_file(source, destination)
    except Exception as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1) from error

    console.print(
        f"[bold green]Convertido:[/bold green] "
        f"{source} -> {destination}"
    )


@app.command("convert-directory")
def convert_directory(
    source_directory: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        readable=True,
        help="Directorio que contiene archivos HTML.",
    ),
    output_directory: Path = typer.Option(
        Path("output"),
        "--output",
        "-o",
        help="Directorio de salida.",
    ),
) -> None:
    """
    Convierte todos los HTML de un directorio.
    """
    files = sorted(source_directory.glob("*.html"))

    if not files:
        console.print("[yellow]No se encontraron archivos HTML.[/yellow]")
        raise typer.Exit(code=0)

    successful = 0
    failed = 0

    for source in files:
        destination = output_directory / f"{source.stem}.md"

        try:
            convert_html_file(source, destination)
            successful += 1
            console.print(f"[green]OK[/green] {source.name}")
        except Exception as error:
            failed += 1
            console.print(
                f"[red]ERROR[/red] {source.name}: {error}"
            )

    console.print()
    console.print(f"Convertidos: [green]{successful}[/green]")
    console.print(f"Fallidos: [red]{failed}[/red]")

    if failed:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()