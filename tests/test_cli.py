from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from wptomd import cli
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
