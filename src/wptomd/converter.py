from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path

import yaml
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as html_to_markdown


def extract_content(soup: BeautifulSoup) -> Tag:
    """
    Obtiene solamente el cuerpo editorial del artículo.

    Admite:
    - HTML completo de WordPress.
    - HTML mínimo generado por Astro.
    - Fragmentos HTML.
    """
    selectors = (
        ".entry-content",
        ".wp-block-post-content",
        "article",
        "main",
        "body",
    )

    for selector in selectors:
        content = soup.select_one(selector)
        if isinstance(content, Tag):
            return content

    raise ValueError("No se encontró el contenido principal del documento.")


def normalize_latex_source(value: str) -> str:
    """
    Limpia el código LaTeX recuperado del atributo alt de QuickLaTeX.
    """
    value = html.unescape(value).strip()

    if value.startswith(r"\[") and value.endswith(r"\]"):
        value = value[2:-2].strip()

    if value.startswith("$$") and value.endswith("$$"):
        value = value[2:-2].strip()

    if value.startswith(r"\(") and value.endswith(r"\)"):
        value = value[2:-2].strip()

    if value.startswith("$") and value.endswith("$"):
        value = value[1:-1].strip()

    return value


def convert_quicklatex(content: Tag) -> None:
    """
    Convierte imágenes generadas por QuickLaTeX en LaTeX real.

    Inline:
        <img class="ql-img-inline-formula" alt="\\sigma(A)">
        -> $\\sigma(A)$

    Display:
        <img class="ql-img-displayed-equation" alt="\\[ ... \\]">
        -> $$ ... $$
    """
    images = list(content.find_all("img"))

    for image in images:
        classes = set(image.get("class", []))
        parent_classes = (
            set(image.parent.get("class", []))
            if isinstance(image.parent, Tag)
            else set()
        )
        source = image.get("src", "")
        alt = image.get("alt", "")

        is_quicklatex = (
            "quicklatex" in source
            or "ql-img-inline-formula" in classes
            or "ql-img-displayed-equation" in classes
        )

        if not is_quicklatex or not alt:
            continue

        latex = normalize_latex_source(alt)

        is_display = (
            "ql-img-displayed-equation" in classes
            or bool(
                parent_classes
                & {
                    "ql-center-displayed-equation",
                    "ql-left-displayed-equation",
                    "ql-right-displayed-equation",
                }
            )
        )

        if is_display:
            replacement = f"\n\n$$\n{latex}\n$$\n\n"
        else:
            replacement = f"${latex}$"

        image.replace_with(replacement)


def remove_quicklatex_wrappers(content: Tag) -> None:
    """
    Elimina contenedores vacíos que QuickLaTeX deja alrededor de ecuaciones.
    """
    selectors = (
        ".ql-center-displayed-equation",
        ".ql-left-displayed-equation",
        ".ql-right-displayed-equation",
    )

    for selector in selectors:
        for wrapper in list(content.select(selector)):
            text = wrapper.get_text("", strip=False).strip()

            if text:
                wrapper.replace_with(text)
            else:
                wrapper.decompose()


def remove_wordpress_residue(content: Tag) -> None:
    """
    Elimina elementos de maquetación sin contenido semántico.
    """
    for selector in (
        "script",
        "style",
        "noscript",
        ".separator",
        ".wp-block-spacer",
    ):
        for element in list(content.select(selector)):
            element.decompose()

    for paragraph in list(content.find_all("p")):
        text = paragraph.get_text(" ", strip=True).replace("\xa0", "")

        if not text and paragraph.find("img") is None:
            paragraph.decompose()

    for div in list(content.find_all("div")):
        text = div.get_text(" ", strip=True).replace("\xa0", "")

        if not text and not div.find(("img", "table", "blockquote")):
            div.decompose()


def normalize_entities(content: Tag) -> None:
    """
    Sustituye espacios no separables y entidades heredadas.
    """
    for text_node in list(content.find_all(string=True)):
        normalized = html.unescape(str(text_node))
        normalized = normalized.replace("\xa0", " ")
        text_node.replace_with(normalized)


def remove_wordpress_attributes(content: Tag) -> None:
    """
    Conserva atributos con valor semántico y elimina atributos propios
    de WordPress o de presentación.
    """
    allowed_attributes = {
        "a": {"href", "title"},
        "img": {"src", "alt", "title", "width", "height"},
        "th": {"colspan", "rowspan"},
        "td": {"colspan", "rowspan"},
    }

    for tag in content.find_all(True):
        allowed = allowed_attributes.get(tag.name, set())

        for attribute in list(tag.attrs):
            if attribute not in allowed:
                del tag.attrs[attribute]


def extract_title(
    soup: BeautifulSoup,
    content: Tag,
    source_name: str,
) -> str:
    h1 = content.find("h1")

    if h1:
        title = h1.get_text(" ", strip=True)
        if title:
            return title

    title_element = soup.find("title")

    if title_element:
        title = title_element.get_text(" ", strip=True)
        title = re.sub(r"\s+-\s+Dagorret\s*$", "", title)

        if title:
            return title

    fallback = Path(source_name).stem.replace("-", " ").strip()
    return fallback.title() or "Artículo"


def slugify(value: str) -> str:
    """Crea un slug ASCII seguro para nombres de archivo."""
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")
    return slug or "articulo"


def clean_markdown(markdown: str) -> str:
    """
    Aplica limpieza final sobre el Markdown generado.
    """
    markdown = html.unescape(markdown)
    markdown = markdown.replace("\xa0", " ")

    # Reduce exceso de líneas vacías.
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    # Limpia espacios al final, salvo dos espacios Markdown usados como <br>.
    lines: list[str] = []

    for line in markdown.splitlines():
        if line.endswith("  "):
            lines.append(line.rstrip() + "  ")
        else:
            lines.append(line.rstrip())

    return "\n".join(lines).strip() + "\n"


def build_frontmatter(
    title: str,
    *,
    slug: str,
    source_name: str,
    source_url: str | None = None,
) -> str:
    metadata = {
        "title": title,
        "slug": slug,
        "status": "published",
    }

    if source_url is not None:
        metadata["legacy_url"] = source_url
    else:
        metadata["legacy_source"] = source_name

    yaml_text = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
    ).strip()

    return f"---\n{yaml_text}\n---\n\n"


def convert_html(
    html_source: str,
    *,
    source_name: str,
    slug: str | None = None,
    source_url: str | None = None,
) -> str:
    """Convierte texto HTML en un documento Markdown completo."""
    soup = BeautifulSoup(html_source, "lxml")

    content = extract_content(soup)
    title = extract_title(soup, content, source_name)
    resolved_slug = slug or slugify(title)

    convert_quicklatex(content)
    remove_quicklatex_wrappers(content)
    normalize_entities(content)
    remove_wordpress_residue(content)
    remove_wordpress_attributes(content)

    markdown = html_to_markdown(
        str(content),
        heading_style="ATX",
        bullets="-",
        strong_em_symbol="_",
        strip=("div", "span"),
    )

    markdown = clean_markdown(markdown)

    # Evita duplicar el título del artículo dentro del cuerpo.
    lines = markdown.splitlines(keepends=True)

    if lines and lines[0].strip() == f"# {title}":
        markdown = "".join(lines[1:]).lstrip()

    return build_frontmatter(
        title,
        slug=resolved_slug,
        source_name=source_name,
        source_url=source_url,
    ) + markdown


def convert_html_file(source: Path, destination: Path) -> None:
    html_source = source.read_text(encoding="utf-8")
    result = convert_html(
        html_source,
        source_name=source.name,
        slug=source.stem,
    )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(result, encoding="utf-8")
