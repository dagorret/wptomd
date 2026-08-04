from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlsplit

import typer
from rich.console import Console

from .converter import convert_html, convert_html_file, slugify
from .fetcher import FetchError, fetch_html

app = typer.Typer(
    help="Convierte artículos HTML de WordPress en documentos Markdown limpios."
)

console = Console()


class UserError(Exception):
    """Error esperado causado por una entrada o destino inválido."""


def print_error(message: str) -> None:
    console.print("ERROR", style="bold red")
    console.print(message, markup=False)


def _missing_file_error(path: Path) -> UserError:
    return UserError(
        "No se pudo abrir el archivo:\n\n"
        f"    {path}\n\n"
        "Motivo:\n\n"
        "    El archivo no existe."
    )


def _validate_source(source: Path) -> None:
    if not source.exists():
        raise _missing_file_error(source)
    if not source.is_file():
        raise UserError(
            "No se pudo abrir el archivo:\n\n"
            f"    {source}\n\n"
            "Motivo:\n\n"
            "    La ruta no corresponde a un archivo."
        )


def _missing_directory_error(directory: Path) -> UserError:
    return UserError(
        "No se pudo escribir el archivo.\n\n"
        "Directorio inexistente:\n\n"
        f"    {directory}"
    )


def _validate_directory(directory: Path) -> None:
    if not directory.exists():
        raise _missing_directory_error(directory)
    if not directory.is_dir():
        raise UserError(
            "No se pudo escribir el archivo.\n\n"
            "Motivo:\n\n"
            f"    La ruta no es un directorio: {directory}"
        )


def _validate_destination_parent(destination: Path) -> None:
    if not destination.parent.is_dir():
        raise _missing_directory_error(destination.parent)


def _has_directory_hint(path: str | Path) -> bool:
    return str(path).endswith(("/", "\\"))


def _resolve_single_destination(
    output: str | Path | None,
    default: Path,
    slug: str,
) -> Path:
    if output is None:
        destination = default
    else:
        output_path = Path(output)
        if output_path.exists() and output_path.is_dir():
            destination = output_path / f"{slug}.md"
        elif not output_path.exists() and _has_directory_hint(output):
            raise _missing_directory_error(output_path)
        else:
            destination = output_path

    _validate_destination_parent(destination)
    return destination


def _existing_output_error(destination: Path) -> UserError:
    return UserError(
        "El archivo de salida ya existe:\n\n"
        f"    {destination}\n\n"
        "Utilice --force para sobrescribirlo."
    )


def _conversion_error(source: Path, error: Exception) -> UserError:
    reason = str(error) or error.__class__.__name__
    return UserError(
        "No se pudo convertir el archivo:\n\n"
        f"    {source}\n\n"
        "Motivo:\n\n"
        f"    {reason}"
    )


def _report_fetch_error(url: str, error: FetchError) -> None:
    reason = getattr(error, "reason", str(error))
    print_error(
        "No se pudo descargar:\n\n"
        f"    {url}\n\n"
        "Motivo:\n\n"
        f"    {reason}"
    )


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


@app.command(help="Convierte un único archivo HTML a Markdown.")
def convert(
    source: Path = typer.Argument(
        ...,
        metavar="SOURCE",
        help="Archivo HTML a convertir.",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        metavar="PATH",
        help="Archivo o directorio de salida.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Sobrescribe el archivo de salida si ya existe.",
    ),
) -> None:
    """Convierte un único archivo HTML a Markdown."""
    try:
        _validate_source(source)
        destination = _resolve_single_destination(
            output,
            source.parent / f"{slugify(source.stem)}.md",
            slugify(source.stem),
        )
        convert_html_file(source, destination, force=force)
    except UserError as error:
        print_error(str(error))
        raise typer.Exit(code=1) from error
    except FileExistsError as error:
        user_error = _existing_output_error(destination)
        print_error(str(user_error))
        raise typer.Exit(code=1) from error
    except (OSError, UnicodeError, ValueError) as error:
        user_error = _conversion_error(source, error)
        print_error(str(user_error))
        raise typer.Exit(code=1) from error

    console.print(
        f"[bold green]Convertido:[/bold green] "
        f"{source} -> {destination}"
    )


@app.command(
    "convert-url",
    help="Descarga un artículo desde una URL y lo convierte a Markdown.",
)
def convert_url(
    url: str = typer.Argument(
        ...,
        metavar="URL",
        help="URL pública del artículo de WordPress.",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        metavar="PATH",
        help="Archivo o directorio de salida.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Sobrescribe el archivo existente.",
    ),
) -> None:
    """Descarga un artículo desde una URL y lo convierte a Markdown."""
    try:
        html_source = fetch_html(url)
        url_slug = slug_from_url(url)
        document = convert_html(
            html_source,
            source_name=url,
            slug=url_slug,
            source_url=url,
        )
        destination = _resolve_single_destination(
            output,
            Path("output") / f"{document.slug}.md",
            document.slug,
        )
        if destination.exists() and not force:
            raise _existing_output_error(destination)
        destination.write_text(document.markdown, encoding="utf-8")
    except FetchError as error:
        _report_fetch_error(url, error)
        raise typer.Exit(code=1) from error
    except UserError as error:
        print_error(str(error))
        raise typer.Exit(code=1) from error
    except (OSError, UnicodeError, ValueError) as error:
        user_error = UserError(
            "No se pudo convertir la URL:\n\n"
            f"    {url}\n\n"
            "Motivo:\n\n"
            f"    {str(error) or error.__class__.__name__}"
        )
        print_error(str(user_error))
        raise typer.Exit(code=1) from error

    console.print(
        f"[bold green]Convertido:[/bold green] "
        f"{url} -> {destination}"
    )


@app.command(
    "convert-directory",
    help="Convierte todos los archivos HTML de un directorio.",
)
def convert_directory(
    directory: Path = typer.Argument(
        ...,
        metavar="DIRECTORY",
        help="Directorio que contiene archivos HTML.",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        metavar="PATH",
        help="Directorio de salida.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Sobrescribe los Markdown existentes.",
    ),
) -> None:
    """Convierte todos los archivos HTML de un directorio."""
    try:
        _validate_directory(directory)
        output_directory = Path(output) if output is not None else None
        if output_directory is not None:
            _validate_directory(output_directory)
    except UserError as error:
        print_error(str(error))
        raise typer.Exit(code=1) from error

    files = sorted(directory.glob("*.html"))

    if not files:
        console.print("[yellow]No se encontraron archivos HTML.[/yellow]")
        raise typer.Exit(code=0)

    successful = 0
    failed = 0

    for source in files:
        destination = (
            (output_directory / f"{slugify(source.stem)}.md")
            if output_directory is not None
            else source.parent / f"{slugify(source.stem)}.md"
        )

        try:
            convert_html_file(source, destination, force=force)
            successful += 1
            console.print(f"[green]OK[/green] {source.name}")
        except FileExistsError:
            failed += 1
            print_error(str(_existing_output_error(destination)))
        except (OSError, UnicodeError, ValueError) as error:
            failed += 1
            print_error(str(_conversion_error(source, error)))

    processed = successful + failed
    console.print()
    console.print(f"Procesados:  {processed}")
    console.print(f"Convertidos: {successful}")
    console.print(f"Fallidos:    {failed}")

    if failed:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
