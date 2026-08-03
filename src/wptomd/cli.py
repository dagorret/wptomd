from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlsplit

import typer
import yaml
from rich.console import Console

from .converter import convert_html, convert_html_file, slugify
from .fetcher import FetchError, fetch_html

app = typer.Typer(
    help="Convierte HTML exportado desde WordPress en Markdown limpio."
)

console = Console()


def slug_from_url(url: str) -> str | None:
    """Obtiene un slug seguro del último segmento de una URL sin parámetros."""
    parsed = urlsplit(url)

    if parsed.query:
        return None

    candidate = unquote(parsed.path.rstrip("/").rsplit("/", 1)[-1])

    if not candidate or candidate.lower() in {
        "index.htm",
        "index.html",
        "index.php",
    }:
        return None

    return slugify(candidate)


def frontmatter_slug(markdown: str) -> str:
    """Lee el slug generado por el conversor para elegir el destino."""
    _, yaml_source, _ = markdown.split("---", 2)
    metadata = yaml.safe_load(yaml_source)
    return str(metadata["slug"])


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


@app.command("convert-url")
def convert_url(
    url: str = typer.Argument(
        ...,
        help="URL pública del artículo de WordPress.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Archivo Markdown de salida.",
    ),
) -> None:
    """Descarga y convierte un artículo de WordPress."""
    try:
        html_source = fetch_html(url)
        url_slug = slug_from_url(url)
        markdown = convert_html(
            html_source,
            source_name=url,
            slug=url_slug,
            source_url=url,
        )
        destination = output or (
            Path("output") / f"{frontmatter_slug(markdown)}.md"
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(markdown, encoding="utf-8")
    except FetchError as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1) from error
    except Exception as error:
        console.print(f"[bold red]Error:[/bold red] {error}")
        raise typer.Exit(code=1) from error

    console.print(
        f"[bold green]Convertido:[/bold green] "
        f"{url} -> {destination}"
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
