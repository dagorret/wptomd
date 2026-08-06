#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


FRONT_MATTER_PATTERN = re.compile(
    r"\A---\s*\n(?P<yaml>.*?)\n---\s*\n?",
    flags=re.DOTALL,
)


class EnrichError(Exception):
    pass


def read_json(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise EnrichError(f"No existe el archivo: {path}") from error
    except json.JSONDecodeError as error:
        raise EnrichError(f"JSON inválido en {path}: {error}") from error

    if not isinstance(data, list):
        raise EnrichError(f"Se esperaba una lista JSON en {path}")

    return data


def split_document(source: str) -> tuple[dict[str, Any], str]:
    match = FRONT_MATTER_PATTERN.match(source)

    if match is None:
        raise EnrichError("El Markdown no contiene front matter YAML.")

    metadata = yaml.safe_load(match.group("yaml")) or {}

    if not isinstance(metadata, dict):
        raise EnrichError("El front matter no es un objeto YAML.")

    body = source[match.end():]

    return metadata, body


def render_document(metadata: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(
        metadata,
        allow_unicode=True,
        sort_keys=False,
    ).strip()

    return f"---\n{yaml_text}\n---\n\n{body.lstrip()}"


def normalize_slug(value: object) -> str:
    return str(value or "").strip().strip("/")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enriquece Markdown con metadatos de WordPress."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Directorio con los Markdown originales.",
    )

    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path("metadata"),
        help="Directorio con posts.json, categories.json y tags.json.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("markdown-ready"),
        help="Directorio de Markdown definitivo.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescribe archivos existentes.",
    )

    args = parser.parse_args()

    try:
        posts = read_json(args.metadata / "posts.json")
        categories = read_json(args.metadata / "categories.json")
        tags = read_json(args.metadata / "tags.json")

        posts_by_slug = {
            normalize_slug(post.get("slug")): post
            for post in posts
            if normalize_slug(post.get("slug"))
        }

        categories_by_id = {
            int(category["id"]): category
            for category in categories
        }

        tags_by_id = {
            int(tag["id"]): tag
            for tag in tags
        }

        args.output.mkdir(parents=True, exist_ok=True)

        converted = 0
        missing = 0
        failed = 0

        files = sorted(args.input.glob("*.md"))

        if not files:
            raise EnrichError(
                f"No se encontraron Markdown en {args.input}"
            )

        for source_path in files:
            try:
                source = source_path.read_text(encoding="utf-8")
                metadata, body = split_document(source)

                slug = normalize_slug(
                    metadata.get("slug") or source_path.stem
                )

                wordpress_post = posts_by_slug.get(slug)

                if wordpress_post is None:
                    print(f"NO ENCONTRADO: {source_path.name}")
                    missing += 1
                    continue

                category_ids = [
                    int(value)
                    for value in wordpress_post.get("categories", [])
                ]

                tag_ids = [
                    int(value)
                    for value in wordpress_post.get("tags", [])
                ]

                resolved_categories = [
                    {
                        "id": category_id,
                        "name": categories_by_id[category_id]["name"],
                        "slug": categories_by_id[category_id]["slug"],
                    }
                    for category_id in category_ids
                    if category_id in categories_by_id
                ]

                resolved_tags = [
                    {
                        "id": tag_id,
                        "name": tags_by_id[tag_id]["name"],
                        "slug": tags_by_id[tag_id]["slug"],
                    }
                    for tag_id in tag_ids
                    if tag_id in tags_by_id
                ]

                metadata["title"] = html.unescape(
                    str(
                        metadata.get("title")
                        or wordpress_post.get("title")
                        or slug
                    )
                )

                metadata["slug"] = slug
                metadata["status"] = "published"
                metadata["wordpress_id"] = int(wordpress_post["id"])
                metadata["published_at"] = wordpress_post.get("date")
                metadata["modified_at"] = wordpress_post.get("modified")
                metadata["legacy_url"] = wordpress_post.get("link")
                metadata["wordpress_category_ids"] = category_ids
                metadata["wordpress_tag_ids"] = tag_ids
                metadata["categories"] = resolved_categories
                metadata["tags"] = resolved_tags

                # FARO admite una sola categoría.
                # Se conserva toda la lista original, pero la primera queda
                # seleccionada como categoría principal.
                metadata["category"] = (
                    resolved_categories[0]
                    if resolved_categories
                    else None
                )

                destination = args.output / source_path.name

                if destination.exists() and not args.force:
                    raise EnrichError(
                        f"Ya existe {destination}; use --force."
                    )

                destination.write_text(
                    render_document(metadata, body),
                    encoding="utf-8",
                )

                converted += 1
                print(f"OK: {source_path.name}")

            except (
                EnrichError,
                OSError,
                UnicodeError,
                ValueError,
                yaml.YAMLError,
            ) as error:
                failed += 1
                print(
                    f"ERROR {source_path.name}: {error}",
                    file=sys.stderr,
                )

        print()
        print(f"Procesados:     {len(files)}")
        print(f"Enriquecidos:   {converted}")
        print(f"No encontrados: {missing}")
        print(f"Fallidos:       {failed}")

        return 1 if failed else 0

    except (EnrichError, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
