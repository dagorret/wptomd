from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from dataclasses import FrozenInstanceError

import yaml

from wptomd.converter import ConvertedDocument, convert_html, convert_html_file


FIXTURES = Path(__file__).parent / "fixtures"


class ConverterTests(unittest.TestCase):
    def convert(self, html_source: str, name: str = "entrada.html") -> str:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            source = directory / name
            destination = directory / "salida.md"
            source.write_text(html_source, encoding="utf-8")
            convert_html_file(source, destination)
            return destination.read_text(encoding="utf-8")

    def split_document(self, document: str) -> tuple[dict[str, object], str]:
        _, yaml_source, body = document.split("---", 2)
        return yaml.safe_load(yaml_source), body.lstrip("\n")

    def test_converts_wordpress_content_to_clean_markdown(self) -> None:
        document = self.convert(
            """
            <html>
              <head><title>Prueba &amp; limpieza - Dagorret</title></head>
              <body>
                <article class="entry-content">
                  <h1>Prueba &amp; limpieza</h1>
                  <p>Texto&nbsp;útil<br>segunda línea &lt; 3.</p>
                  <p>Inline <img class="ql-img-inline-formula"
                    src="https://quicklatex.com/a.png"
                    alt="\\(x^2 &amp; y\\)"> final.</p>
                  <div class="ql-center-displayed-equation">
                    <img src="https://quicklatex.com/b.png"
                      alt="\\[\\frac{a}{b}\\]">
                  </div>
                  <table>
                    <thead><tr><th>Uno</th><th>Dos</th></tr></thead>
                    <tbody><tr><td>A</td><td>B</td></tr></tbody>
                  </table>
                  <blockquote><p>Cita <strong>fuerte</strong></p></blockquote>
                  <figure class="wp-block-image">
                    <img src="foto.jpg" alt="Foto &amp; pie">
                    <figcaption>Un pie</figcaption>
                  </figure>
                  <div class="wp-block-spacer" style="height: 20px"></div>
                  <script>residuo()</script>
                </article>
              </body>
            </html>
            """
        )

        metadata, body = self.split_document(document)

        self.assertEqual(metadata["title"], "Prueba & limpieza")
        self.assertEqual(metadata["slug"], "entrada")
        self.assertNotIn("# Prueba & limpieza", body)
        self.assertIn("Texto útil  \nsegunda línea < 3.", body)
        self.assertIn("Inline $x^2 & y$ final.", body)
        self.assertIn("$$\n\\frac{a}{b}\n$$", body)
        self.assertIn("| Uno | Dos |\n| --- | --- |\n| A | B |", body)
        self.assertIn("> Cita __fuerte__", body)
        self.assertIn("![Foto & pie](foto.jpg)", body)
        self.assertIn("Un pie", body)
        self.assertNotIn("residuo", body)
        self.assertNotIn("wp-block", body)

    def test_removes_the_exact_first_heading(self) -> None:
        document = self.convert(
            """
            <html><head><title>Título</title></head><body>
              <article><h1>Título extendido</h1><p>Contenido.</p></article>
            </body></html>
            """
        )

        _, body = self.split_document(document)
        self.assertTrue(body.startswith("Contenido."))

    def test_uses_editorial_heading_instead_of_site_header(self) -> None:
        document = self.convert(
            """
            <html><body>
              <header><h1>Nombre del sitio</h1></header>
              <article><h1>Título editorial</h1><p>Contenido.</p></article>
            </body></html>
            """,
            name="titulo-editorial.html",
        )

        metadata, body = self.split_document(document)
        self.assertEqual(metadata["title"], "Título editorial")
        self.assertNotIn("# Título editorial", body)

    def test_convert_html_returns_immutable_document_with_normalized_slug(self) -> None:
        document = convert_html(
            "<article><h1>Artículo útil</h1><p>Contenido.</p></article>",
            source_name="entrada.html",
            slug="Artículo útil",
        )

        self.assertIsInstance(document, ConvertedDocument)
        self.assertEqual(document.slug, "articulo-util")
        with self.assertRaises(FrozenInstanceError):
            document.slug = "otro"  # type: ignore[misc]

    def test_frontmatter_and_content_can_include_triple_dash(self) -> None:
        document = convert_html(
            """
            <html><head><title>Título --- edición</title></head><body>
              <article><h1>Título --- edición</h1>
                <p>Contenido --- permanente.</p>
              </article>
            </body></html>
            """,
            source_name="entrada.html",
        )

        self.assertIn("title: Título --- edición", document.markdown)
        self.assertIn("Contenido --- permanente.", document.markdown)
        self.assertEqual(document.slug, "titulo-edicion")

    def test_quicklatex_inside_code_is_literal_and_fenced(self) -> None:
        html_source = (FIXTURES / "quicklatex-code.html").read_text(
            encoding="utf-8"
        )

        document = convert_html(
            html_source,
            source_name="quicklatex-code.html",
        )

        self.assertIn(
            '```bash\nmkdir -p $DEST\nrsync "$SOURCE" "${NOTEBOOK}"\n```',
            document.markdown,
        )
        self.assertIn(
            '```\n<div class="example">\n  <span>texto</span>\n</div>\n```',
            document.markdown,
        )
        self.assertNotIn("$${DEST}$$", document.markdown)
        self.assertNotIn("ql-img-", document.markdown)
        self.assertNotIn("wp-content/ql-cache", document.markdown)

    def test_escaped_quicklatex_image_inside_code_becomes_literal_variable(self) -> None:
        document = convert_html(
            """
            <article><h1>Shell</h1>
              <pre><code class="language-bash">mkdir -p "&lt;img
                src="quicklatex.png" class="ql-img-inline-formula"
                alt="DEST" /&gt;DEST"</code></pre>
            </article>
            """,
            source_name="shell.html",
        )

        self.assertIn("mkdir -p \"$DEST\"", document.markdown)
        self.assertNotIn("ql-img-", document.markdown)

    def test_syntax_highlighter_wrappers_are_not_kept_in_code(self) -> None:
        document = convert_html(
            """
            <article><h1>Code</h1>
              <pre><code class="language-bash">echo
                <span class="hljs-string">"literal"</span>
                <span class="example">&lt;div&gt;texto&lt;/div&gt;</span></code></pre>
            </article>
            """,
            source_name="code.html",
        )

        self.assertNotIn("hljs-", document.markdown)
        self.assertIn('"literal"', document.markdown)
        self.assertIn('<span class="example"><div>texto</div></span>', document.markdown)

    def test_quicklatex_display_detects_image_and_parent_wrapper(self) -> None:
        html_source = (FIXTURES / "quicklatex-display.html").read_text(
            encoding="utf-8"
        )

        document = convert_html(
            html_source,
            source_name="quicklatex-display.html",
        )

        self.assertEqual(document.markdown.count("$$"), 4)
        self.assertIn("$$\nx^2 + y^2\n$$", document.markdown)
        self.assertIn("$$\na+b\n$$", document.markdown)
        self.assertNotIn("ql-img-", document.markdown)
        self.assertNotIn("ql-center-displayed-equation", document.markdown)
        self.assertNotIn("<img", document.markdown)
        self.assertNotIn("wp-content/ql-cache", document.markdown)

    def test_quicklatex_display_without_wrapper_is_converted(self) -> None:
        document = convert_html(
            """
            <article><h1>Math</h1>
              <p><img class="ql-img-displayed-equation"
                alt="\\[x^2\\]"></p>
            </article>
            """,
            source_name="math.html",
        )

        self.assertIn("$$\nx^2\n$$", document.markdown)
        self.assertNotIn("ql-img-displayed-equation", document.markdown)

    def test_tables_quotes_images_and_links_remain_after_code_protection(self) -> None:
        document = convert_html(
            """
            <article><h1>Contenido</h1>
              <table><tr><th>A</th></tr><tr><td>B</td></tr></table>
              <blockquote><p>Cita.</p></blockquote>
              <p><a href="https://example.com">Enlace</a>
                <img src="imagen.jpg" alt="Imagen"></p>
            </article>
            """,
            source_name="contenido.html",
        )

        self.assertIn("| A |\n| --- |\n| B |", document.markdown)
        self.assertIn("> Cita.", document.markdown)
        self.assertIn("[Enlace](https://example.com)", document.markdown)
        self.assertIn("![Imagen](imagen.jpg)", document.markdown)


if __name__ == "__main__":
    unittest.main()
