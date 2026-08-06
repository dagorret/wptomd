#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import httpx


USER_AGENT = "faro-wordpress-importer/1.0"
DEFAULT_TIMEOUT = httpx.Timeout(
    connect=20.0,
    read=120.0,
    write=30.0,
    pool=30.0,
)
PER_PAGE = 100


class ImportErrorExpected(Exception):
    pass


def fetch_collection(
    client: httpx.Client,
    base_url: str,
    endpoint: str,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    page = 1

    while True:
        url = f"{base_url.rstrip('/')}/wp-json/wp/v2/{endpoint}"

        response = client.get(
            url,
            params={
                "per_page": PER_PAGE,
                "page": page,
                "context": "view",
            },
        )

        if response.status_code == 400 and page > 1:
            break

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise ImportErrorExpected(
                f"Error HTTP {response.status_code} descargando {endpoint}, "
                f"página {page}: {response.text[:300]}"
            ) from error

        payload = response.json()

        if not isinstance(payload, list):
            raise ImportErrorExpected(
                f"La API devolvió un formato inesperado para {endpoint}."
            )

        if not payload:
            break

        results.extend(payload)

        total_pages = int(response.headers.get("X-WP-TotalPages", page))

        print(
            f"{endpoint}: página {page}/{total_pages} "
            f"({len(results)} registros)",
            flush=True,
        )

        if page >= total_pages:
            break

        page += 1

    return results


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_suffix(path.suffix + ".tmp")

    temporary.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Descarga metadatos de la API REST de WordPress."
    )

    parser.add_argument(
        "base_url",
        help="URL base del WordPress, por ejemplo https://dagorret.com.ar",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("metadata"),
        help="Directorio de salida. Predeterminado: metadata",
    )

    args = parser.parse_args()

    try:
        with httpx.Client(
            timeout=DEFAULT_TIMEOUT,
            follow_redirects=True,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        ) as client:
            posts = fetch_collection(client, args.base_url, "posts")
            categories = fetch_collection(client, args.base_url, "categories")
            tags = fetch_collection(client, args.base_url, "tags")

        posts_compact = [
            {
                "id": post["id"],
                "slug": post.get("slug", ""),
                "link": post.get("link"),
                "date": post.get("date"),
                "date_gmt": post.get("date_gmt"),
                "modified": post.get("modified"),
                "status": post.get("status"),
                "title": post.get("title", {}).get("rendered", ""),
                "categories": post.get("categories", []),
                "tags": post.get("tags", []),
            }
            for post in posts
        ]

        categories_compact = [
            {
                "id": category["id"],
                "name": category.get("name", ""),
                "slug": category.get("slug", ""),
                "parent": category.get("parent", 0),
                "count": category.get("count", 0),
            }
            for category in categories
        ]

        tags_compact = [
            {
                "id": tag["id"],
                "name": tag.get("name", ""),
                "slug": tag.get("slug", ""),
                "count": tag.get("count", 0),
            }
            for tag in tags
        ]

        write_json(args.output / "posts.json", posts_compact)
        write_json(args.output / "categories.json", categories_compact)
        write_json(args.output / "tags.json", tags_compact)

        print()
        print(f"Posts:      {len(posts_compact)}")
        print(f"Categorías: {len(categories_compact)}")
        print(f"Tags:       {len(tags_compact)}")
        print(f"Salida:     {args.output.resolve()}")

        return 0

    except (
        ImportErrorExpected,
        httpx.RequestError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
