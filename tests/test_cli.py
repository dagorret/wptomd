from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from wptomd import cli
from wptomd.converter import ConvertedDocument, slugify
from wptomd.fetcher import FetchError

FIXTURE = Path(__file__).parent / "fixtures" / "wordpress-sample.html"


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://example.com/el-modelo-base-00-2/", "el-modelo-base-00-2"),
        ("https://example.com/Artículo%20Útil/", "articulo-util"),
        ("https://example.com/", None),
        ("https://example.com/articulo/?p=42", None),
        ("https://example.com/index.php", None),
    ],
)
def test_slug_from_url(url: str, expected: str | None) -> None:
    assert cli.slug_from_url(url) == expected


def test_convert_url_uses_url_slug_and_shared_pipeline(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    html_source = FIXTURE.read_text(encoding="utf-8")
    url = "https://example.com/el-modelo-base-00-2/"
    monkeypatch.setattr(cli, "fetch_html", lambda requested: html_source)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "output").mkdir()

    result = CliRunner().invoke(cli.app, ["convert-url", url])

    assert result.exit_code == 0, result.output
    destination = tmp_path / "output" / "el-modelo-base-00-2.md"
    markdown = destination.read_text(encoding="utf-8")
    _, yaml_source, body = markdown.split("---", 2)
    metadata = yaml.safe_load(yaml_source)
    assert metadata == {
        "title": "Entrada de prueba",
        "slug": "el-modelo-base-00-2",
        "status": "published",
        "legacy_url": url,
    }
    assert "$x^2$" in body
    assert "$$\n\\frac{a}{b}\n$$" in body
    assert "| Columna A | Columna B |" in body
    assert "> Una cita." in body
    assert "![Una imagen](imagen.jpg)" in body
    assert "Primera línea  \nsegunda línea con entidad." in body
    assert "wp-block-spacer" not in body


def test_convert_url_falls_back_to_title_and_accepts_explicit_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    html_source = FIXTURE.read_text(encoding="utf-8")
    monkeypatch.setattr(cli, "fetch_html", lambda requested: html_source)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "output").mkdir()
    runner = CliRunner()

    automatic = runner.invoke(
        cli.app,
        ["convert-url", "https://example.com/?p=42"],
    )
    explicit_path = tmp_path / "elegido.md"
    explicit = runner.invoke(
        cli.app,
        [
            "convert-url",
            "https://example.com/otro/",
            "--output",
            str(explicit_path),
        ],
    )

    assert automatic.exit_code == 0, automatic.output
    assert (tmp_path / "output" / "entrada-de-prueba.md").is_file()
    assert explicit.exit_code == 0, explicit.output
    assert explicit_path.is_file()


def test_convert_url_reports_fetch_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(requested: str) -> str:
        raise FetchError(f"Error HTTP 404 al descargar {requested}")

    monkeypatch.setattr(cli, "fetch_html", fail)

    result = CliRunner().invoke(
        cli.app,
        ["convert-url", "https://example.com/falta/"],
    )

    assert result.exit_code == 1
    assert "Error HTTP 404 al descargar https://example.com/falta/" in result.output


def test_existing_file_commands_still_work(tmp_path: Path) -> None:
    runner = CliRunner()
    single_output = tmp_path / "single.md"

    single = runner.invoke(
        cli.app,
        ["convert", str(FIXTURE), "--output", str(single_output)],
    )

    source_directory = tmp_path / "html"
    source_directory.mkdir()
    (source_directory / "uno.html").write_text(
        FIXTURE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    directory_output = tmp_path / "markdown"
    directory_output.mkdir()
    directory = runner.invoke(
        cli.app,
        [
            "convert-directory",
            str(source_directory),
            "--output",
            str(directory_output),
        ],
    )

    assert single.exit_code == 0, single.output
    assert single_output.is_file()
    assert directory.exit_code == 0, directory.output
    assert (directory_output / "uno.md").is_file()


def test_convert_uses_one_slug_policy_for_file_names(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source = tmp_path / "Artículo Útil.HTML"
    source.write_text(
        "<article><h1>Otro título</h1><p>Contenido.</p></article>",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(cli.app, ["convert", str(source)])

    assert result.exit_code == 0, result.output
    destination = tmp_path / "articulo-util.md"
    assert destination.is_file()
    assert "slug: articulo-util" in destination.read_text(encoding="utf-8")


def test_file_and_url_slugs_use_the_same_policy() -> None:
    source_stem = "Artículo Útil"
    url = "https://example.com/Artículo%20Útil/"

    assert slugify(source_stem) == cli.slug_from_url(url)


def test_convert_fails_for_existing_output_without_force(tmp_path: Path) -> None:
    source = tmp_path / "entrada.html"
    source.write_text(
        "<article><h1>Entrada</h1><p>Nuevo.</p></article>",
        encoding="utf-8",
    )
    destination = tmp_path / "salida.md"
    destination.write_text("contenido anterior", encoding="utf-8")

    result = CliRunner().invoke(
        cli.app,
        ["convert", str(source), "--output", str(destination)],
    )

    assert result.exit_code == 1
    assert "El archivo de salida ya existe" in result.output
    assert destination.read_text(encoding="utf-8") == "contenido anterior"


def test_convert_overwrites_existing_output_with_force(tmp_path: Path) -> None:
    source = tmp_path / "entrada.html"
    source.write_text(
        "<article><h1>Entrada</h1><p>Nuevo.</p></article>",
        encoding="utf-8",
    )
    destination = tmp_path / "salida.md"
    destination.write_text("contenido anterior", encoding="utf-8")

    result = CliRunner().invoke(
        cli.app,
        [
            "convert",
            str(source),
            "--output",
            str(destination),
            "--force",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Nuevo." in destination.read_text(encoding="utf-8")


def test_convert_url_uses_document_slug_without_parsing_markdown(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(cli, "fetch_html", lambda requested: "ignored")
    monkeypatch.setattr(
        cli,
        "convert_html",
        lambda *args, **kwargs: ConvertedDocument(
            title="Título",
            slug="slug-canonico",
            markdown="---\ntitle: Título --- raro\n---\n\nContenido --- aquí.\n",
        ),
    )
    monkeypatch.chdir(tmp_path)
    (tmp_path / "output").mkdir()

    result = CliRunner().invoke(
        cli.app,
        ["convert-url", "https://example.com/entrada/"],
    )

    assert result.exit_code == 0, result.output
    assert (tmp_path / "output" / "slug-canonico.md").is_file()
    assert not (tmp_path / "output" / "raro.md").exists()


def write_article(path: Path, title: str = "Artículo") -> None:
    path.write_text(
        f"<article><h1>{title}</h1><p>Contenido.</p></article>",
        encoding="utf-8",
    )


def test_convert_accepts_relative_path_and_writes_next_to_source(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    source = Path("input/articulo.html")
    source.parent.mkdir()
    write_article(source)

    result = CliRunner().invoke(cli.app, ["convert", str(source)])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "input/articulo.md").is_file()
    assert not (tmp_path / "output").exists()


def test_convert_accepts_absolute_path_and_writes_next_to_source(
    tmp_path: Path,
) -> None:
    source = tmp_path / "legacy/articulo.html"
    source.parent.mkdir()
    write_article(source)

    result = CliRunner().invoke(cli.app, ["convert", str(source)])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "legacy/articulo.md").is_file()


def test_convert_output_directory_must_already_exist(tmp_path: Path) -> None:
    source = tmp_path / "articulo.html"
    write_article(source)
    output = tmp_path / "content"

    result = CliRunner().invoke(
        cli.app,
        ["convert", str(source), "-o", str(output) + "/"],
    )

    assert result.exit_code == 1
    assert "Directorio inexistente" in result.output
    assert not output.exists()


def test_convert_output_directory_writes_slugged_file(tmp_path: Path) -> None:
    source = tmp_path / "articulo.html"
    write_article(source)
    output = tmp_path / "content"
    output.mkdir()

    result = CliRunner().invoke(
        cli.app,
        ["convert", str(source), "-o", str(output)],
    )

    assert result.exit_code == 0, result.output
    assert (output / "articulo.md").is_file()


def test_convert_directory_writes_next_to_each_html(tmp_path: Path) -> None:
    directory = tmp_path / "legacy"
    directory.mkdir()
    write_article(directory / "uno.html")
    write_article(directory / "dos.html")

    result = CliRunner().invoke(cli.app, ["convert-directory", str(directory)])

    assert result.exit_code == 0, result.output
    assert (directory / "uno.md").is_file()
    assert (directory / "dos.md").is_file()
    assert "Procesados:  2" in result.output
    assert "Convertidos: 2" in result.output
    assert "Fallidos:    0" in result.output


def test_convert_directory_continues_after_a_failed_file(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "legacy"
    directory.mkdir()
    (directory / "a-falla.html").write_text(
        "\xff",
        encoding="latin-1",
    )
    write_article(directory / "b-funciona.html")

    result = CliRunner().invoke(cli.app, ["convert-directory", str(directory)])

    assert result.exit_code == 1
    assert not (directory / "a-falla.md").exists()
    assert (directory / "b-funciona.md").is_file()
    assert "Procesados:  2" in result.output
    assert "Convertidos: 1" in result.output
    assert "Fallidos:    1" in result.output


def test_convert_directory_requires_existing_output_directory(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "legacy"
    directory.mkdir()
    write_article(directory / "articulo.html")
    output = tmp_path / "content"

    result = CliRunner().invoke(
        cli.app,
        ["convert-directory", str(directory), "-o", str(output)],
    )

    assert result.exit_code == 1
    assert "Directorio inexistente" in result.output
    assert not output.exists()


def test_convert_url_requires_existing_default_output_directory(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        cli,
        "fetch_html",
        lambda requested: FIXTURE.read_text(encoding="utf-8"),
    )
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(
        cli.app,
        ["convert-url", "https://example.com/articulo/"],
    )

    assert result.exit_code == 1
    assert "Directorio inexistente" in result.output
    assert not (tmp_path / "output").exists()


def test_convert_url_output_directory_must_exist(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        cli,
        "fetch_html",
        lambda requested: FIXTURE.read_text(encoding="utf-8"),
    )
    output = tmp_path / "content"

    result = CliRunner().invoke(
        cli.app,
        [
            "convert-url",
            "https://example.com/articulo/",
            "-o",
            str(output) + "/",
        ],
    )

    assert result.exit_code == 1
    assert "Directorio inexistente" in result.output
    assert not output.exists()


def test_convert_url_accepts_existing_output_directory(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        cli,
        "fetch_html",
        lambda requested: FIXTURE.read_text(encoding="utf-8"),
    )
    output = tmp_path / "content"
    output.mkdir()

    result = CliRunner().invoke(
        cli.app,
        [
            "convert-url",
            "https://example.com/articulo/",
            "-o",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output
    assert (output / "articulo.md").is_file()


def test_existing_output_fails_without_force_and_is_unchanged(
    tmp_path: Path,
) -> None:
    source = tmp_path / "articulo.html"
    write_article(source)
    destination = tmp_path / "articulo.md"
    destination.write_text("contenido manual", encoding="utf-8")

    result = CliRunner().invoke(cli.app, ["convert", str(source)])

    assert result.exit_code == 1
    assert "El archivo de salida ya existe" in result.output
    assert "Utilice --force" in result.output
    assert destination.read_text(encoding="utf-8") == "contenido manual"


def test_force_overwrites_without_overwrite_message(tmp_path: Path) -> None:
    source = tmp_path / "articulo.html"
    write_article(source)
    destination = tmp_path / "articulo.md"
    destination.write_text("contenido manual", encoding="utf-8")

    result = CliRunner().invoke(
        cli.app,
        ["convert", str(source), "--force"],
    )

    assert result.exit_code == 0, result.output
    assert "Sobrescribiendo" not in result.output
    assert "Contenido." in destination.read_text(encoding="utf-8")


def test_missing_source_has_contextual_error(tmp_path: Path) -> None:
    source = tmp_path / "articulo.html"

    result = CliRunner().invoke(cli.app, ["convert", str(source)])

    assert result.exit_code == 1
    assert "No se pudo abrir el archivo" in result.output
    assert str(source) in result.output
    assert "El archivo no existe" in result.output
    assert "Traceback" not in result.output


def test_http_404_has_contextual_error(monkeypatch: pytest.MonkeyPatch) -> None:
    url = "https://example.com/falta/"
    monkeypatch.setattr(
        cli,
        "fetch_html",
        lambda requested: (_ for _ in ()).throw(
            FetchError("Error HTTP 404 al descargar " + requested,
                       reason="HTTP 404 Not Found")
        ),
    )

    result = CliRunner().invoke(cli.app, ["convert-url", url])

    assert result.exit_code == 1
    assert "No se pudo descargar" in result.output
    assert url in result.output
    assert "HTTP 404 Not Found" in result.output
    assert "Traceback" not in result.output


def test_timeout_has_contextual_error(monkeypatch: pytest.MonkeyPatch) -> None:
    url = "https://example.com/lento/"
    monkeypatch.setattr(
        cli,
        "fetch_html",
        lambda requested: (_ for _ in ()).throw(
            FetchError("No se pudo conectar con " + requested,
                       reason="Tiempo de espera agotado.")
        ),
    )

    result = CliRunner().invoke(cli.app, ["convert-url", url])

    assert result.exit_code == 1
    assert "No se pudo descargar" in result.output
    assert url in result.output
    assert "Tiempo de espera agotado." in result.output
    assert "Traceback" not in result.output


@pytest.mark.parametrize(
    "arguments",
    [
        ["--help"],
        ["convert", "--help"],
        ["convert-directory", "--help"],
        ["convert-url", "--help"],
    ],
)
def test_cli_help_describes_commands_and_arguments(arguments: list[str]) -> None:
    result = CliRunner().invoke(cli.app, arguments)

    assert result.exit_code == 0, result.output
    assert "--help" in result.output
    if arguments == ["--help"]:
        assert "convert" in result.output
        assert "convert-directory" in result.output
        assert "convert-url" in result.output
    elif arguments[0] == "convert":
        assert "SOURCE" in result.output
        assert "Convierte un único archivo HTML a Markdown." in result.output
        assert "--force" in result.output
    elif arguments[0] == "convert-directory":
        assert "DIRECTORY" in result.output
        assert "Convierte todos los archivos HTML de un directorio." in result.output
        assert "--force" in result.output
    else:
        assert "URL" in result.output
        assert "Descarga un artículo desde una URL" in result.output
        assert "--force" in result.output
