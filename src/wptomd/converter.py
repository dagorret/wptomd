from __future__ import annotations

import html
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import yaml
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from markdownify import markdownify as html_to_markdown


@dataclass(frozen=True)
class ConvertedDocument:
    title: str
    slug: str
    markdown: str


QUICKLATEX_DISPLAY_CLASSES = {
    "ql-center-displayed-equation",
    "ql-left-displayed-equation",
    "ql-right-displayed-equation",
    "ql-img-displayed-equation",
}


def _is_quicklatex_image(image: Tag) -> bool:
    classes = set(image.get("class", []))
    source = image.get("src", "")
    return (
        "quicklatex" in source
        or "ql-img-inline-formula" in classes
        or "ql-img-displayed-equation" in classes
    )


def _quicklatex_display_wrapper(image: Tag, content: Tag) -> Tag | None:
    current: Tag | None = image

    while isinstance(current, Tag) and current is not content:
        classes = set(current.get("class", []))
        if classes & QUICKLATEX_DISPLAY_CLASSES:
            return current
        current = current.parent if isinstance(current.parent, Tag) else None

    return None


def _code_language(element: Tag) -> str:
    code = element.find("code")
    tags = [element]
    if isinstance(code, Tag):
        tags.append(code)

    for tag in tags:
        for class_name in tag.get("class", []):
            match = re.fullmatch(r"(?:language|lang)-([a-z0-9_+-]+)", class_name)
            if match:
                return match.group(1)

        for attribute in ("data-language", "data-lang"):
            value = tag.get(attribute)
            if isinstance(value, str) and value.strip():
                return value.strip()

    sibling = element.previous_sibling
    checked = 0
    while sibling is not None and checked < 3:
        if isinstance(sibling, Comment):
            match = re.search(
                r'"language"\s*:\s*"([a-zA-Z0-9_+-]+)"',
                str(sibling),
            )
            if match:
                return match.group(1).lower()
        sibling = sibling.previous_sibling
        checked += 1

    return ""


def _serialize_code_node(node: object) -> str:
    if isinstance(node, NavigableString):
        return _replace_literal_quicklatex_images(str(node))

    if not isinstance(node, Tag):
        return str(node)

    if node.name == "img" and _is_quicklatex_image(node):
        return _code_quicklatex_value(str(node.get("alt", "")))

    if node.name == "span" and any(
        class_name.startswith("hljs") for class_name in node.get("class", [])
    ):
        return "".join(_serialize_code_node(child) for child in node.contents)

    if not node.contents:
        return str(node)

    if node.name in {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "source",
        "track",
        "wbr",
    }:
        return str(node)

    opening_tag = str(node).split(">", 1)[0] + ">"
    inner = "".join(_serialize_code_node(child) for child in node.contents)
    return f"{opening_tag}{inner}</{node.name}>"


def _code_quicklatex_value(value: str) -> str:
    value = html.unescape(value)
    if value.startswith("$"):
        return value

    if _is_code_variable(value):
        return f"${value}"

    return value


def _is_code_variable(value: str) -> bool:
    return bool(
        re.fullmatch(
            r"(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})",
            value,
        )
    )


def _replace_literal_quicklatex_images(value: str) -> str:
    image_with_end = re.compile(
        r'<img\b[^<]*?alt\s*=\s*["\'](?P<alt>.*?)["\'][^<]*?/>',
        flags=re.IGNORECASE | re.DOTALL,
    )

    def replace_closed(match: re.Match[str]) -> str:
        raw_alt = html.unescape(match.group("alt"))
        if _is_code_variable(raw_alt):
            return "$" if not raw_alt.startswith("$") else raw_alt
        return raw_alt

    value = image_with_end.sub(replace_closed, value)

    image_without_end = re.compile(
        r'<img\b[^<]*?alt\s*=\s*["\'](?P<alt>.*?)["\']',
        flags=re.IGNORECASE | re.DOTALL,
    )

    def replace_open(match: re.Match[str]) -> str:
        return f'{_code_quicklatex_value(match.group("alt"))}"'

    return image_without_end.sub(replace_open, value)


def _serialize_code_block(element: Tag) -> str:
    code = element.find("code")
    target = code if isinstance(code, Tag) else element

    flattened = target.get_text("", strip=False)
    if "quicklatex" in flattened or "ql-img-" in flattened:
        return _replace_literal_quicklatex_images(flattened)

    return "".join(_serialize_code_node(child) for child in target.contents)


def protect_code_blocks(content: Tag) -> dict[str, str]:
    """Reemplaza bloques de código por marcadores antes de normalizar el HTML."""
    blocks = list(content.find_all("pre"))
    blocks.extend(
        block
        for block in content.select(".wp-block-code")
        if block.name != "pre" and block.find("pre") is None
    )

    protected: dict[str, str] = {}

    for index, block in enumerate(blocks):
        marker = f"wptomd-code-block-{index}-placeholder"
        language = _code_language(block)
        code = _serialize_code_block(block).rstrip("\n")
        fence = f"```{language}\n{code}\n```"
        protected[marker] = fence
        block.replace_with(marker)

    return protected


def restore_code_blocks(markdown: str, protected: dict[str, str]) -> str:
    for marker, fence in protected.items():
        markdown = markdown.replace(marker, fence)
    return markdown


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
        if not _is_quicklatex_image(image):
            continue

        alt = image.get("alt", "")
        latex = normalize_latex_source(alt)
        wrapper = _quicklatex_display_wrapper(image, content)
        is_display = (
            "ql-img-displayed-equation" in set(image.get("class", []))
            or wrapper is not None
        )

        if not alt:
            image.decompose()
        elif is_display:
            replacement = f"\n\n$$\n{latex}\n$$\n\n"
            if wrapper is not None:
                wrapper.replace_with(replacement)
            else:
                image.replace_with(replacement)
        else:
            image.replace_with(f"${latex}$")


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
            wrapper.unwrap()


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
) -> ConvertedDocument:
    """Convierte texto HTML en un documento Markdown completo."""
    soup = BeautifulSoup(html_source, "lxml")

    content = extract_content(soup)
    title = extract_title(soup, content, source_name)
    resolved_slug = slugify(slug or title)

    protected_code = protect_code_blocks(content)
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

    markdown = restore_code_blocks(markdown, protected_code)
    markdown = clean_markdown(markdown)

    # Evita duplicar el título del artículo dentro del cuerpo.
    lines = markdown.splitlines(keepends=True)

    if lines and lines[0].strip() == f"# {title}":
        markdown = "".join(lines[1:]).lstrip()

    document = build_frontmatter(
        title,
        slug=resolved_slug,
        source_name=source_name,
        source_url=source_url,
    ) + markdown

    return ConvertedDocument(
        title=title,
        slug=resolved_slug,
        markdown=document,
    )


def convert_html_file(
    source: Path,
    destination: Path,
    *,
    force: bool = False,
) -> ConvertedDocument:
    html_source = source.read_text(encoding="utf-8")
    result = convert_html(
        html_source,
        source_name=source.name,
        slug=slugify(source.stem),
    )

    if destination.exists() and not force:
        raise FileExistsError(f"El archivo de salida ya existe: {destination}")

    destination.write_text(result.markdown, encoding="utf-8")
    return result
