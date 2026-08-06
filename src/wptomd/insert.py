#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import secrets
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


class FaroImportError(Exception):
    pass


def split_document(source: str) -> tuple[dict[str, Any], str]:
    if not source.startswith("---\n"):
        raise FaroImportError("El archivo no contiene front matter.")

    try:
        _, yaml_source, body = source.split("---", 2)
    except ValueError as error:
        raise FaroImportError("Front matter incompleto.") from error

    metadata = yaml.safe_load(yaml_source) or {}

    if not isinstance(metadata, dict):
        raise FaroImportError("El front matter no es un objeto YAML.")

    return metadata, body.lstrip()


def editorjs_markdown(markdown: str) -> str:
    document = {
        "time": int(time.time() * 1000),
        "blocks": [
            {
                "id": secrets.token_urlsafe(8)[:10],
                "type": "markdown",
                "data": {
                    "source": markdown,
                },
            }
        ],
        "version": "2.28.2",
    }

    return json.dumps(
        document,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def table_exists(connection: sqlite3.Connection, table: str) -> bool:
    row = connection.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        LIMIT 1
        """,
        (table,),
    ).fetchone()

    return row is not None


def table_columns(
    connection: sqlite3.Connection,
    table: str,
) -> set[str]:
    return {
        str(row["name"])
        for row in connection.execute(f"PRAGMA table_info({table})")
    }


def require_schema(connection: sqlite3.Connection) -> None:
    required_tables = {
        "sites",
        "posts",
        "categories",
        "tags",
        "post_tag",
    }

    missing = [
        table
        for table in required_tables
        if not table_exists(connection, table)
    ]

    if missing:
        raise FaroImportError(
            "Faltan tablas requeridas: " + ", ".join(missing)
        )

    required_columns = {
        "posts": {
            "id",
            "site_id",
            "title",
            "slug",
            "body",
            "type",
            "category_id",
            "status",
            "published_at",
            "created_at",
            "updated_at",
        },
        "categories": {
            "id",
            "site_id",
            "name",
            "slug",
        },
        "tags": {
            "id",
            "site_id",
            "name",
            "slug",
        },
        "post_tag": {
            "post_id",
            "tag_id",
        },
    }

    for table, expected in required_columns.items():
        current = table_columns(connection, table)
        missing_columns = sorted(expected - current)

        if missing_columns:
            raise FaroImportError(
                f"Faltan columnas en {table}: "
                + ", ".join(missing_columns)
            )


def resolve_site(
    connection: sqlite3.Connection,
    short_name: str,
) -> sqlite3.Row:
    site = connection.execute(
        """
        SELECT *
        FROM sites
        WHERE short_name = ?
        LIMIT 1
        """,
        (short_name,),
    ).fetchone()

    if site is None:
        raise FaroImportError(
            f"No existe el sitio FARO [{short_name}]."
        )

    return site


def upsert_category(
    connection: sqlite3.Connection,
    *,
    site_id: int,
    name: str,
    slug: str,
    timestamp: str,
) -> int:
    existing = connection.execute(
        """
        SELECT id
        FROM categories
        WHERE site_id = ?
          AND slug = ?
        LIMIT 1
        """,
        (site_id, slug),
    ).fetchone()

    if existing is not None:
        connection.execute(
            """
            UPDATE categories
            SET name = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (name, timestamp, existing["id"]),
        )

        return int(existing["id"])

    cursor = connection.execute(
        """
        INSERT INTO categories (
            site_id,
            name,
            slug,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            site_id,
            name,
            slug,
            timestamp,
            timestamp,
        ),
    )

    return int(cursor.lastrowid)


def upsert_tag(
    connection: sqlite3.Connection,
    *,
    site_id: int,
    name: str,
    slug: str,
    timestamp: str,
) -> int:
    existing = connection.execute(
        """
        SELECT id
        FROM tags
        WHERE site_id = ?
          AND slug = ?
        LIMIT 1
        """,
        (site_id, slug),
    ).fetchone()

    if existing is not None:
        connection.execute(
            """
            UPDATE tags
            SET name = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (name, timestamp, existing["id"]),
        )

        return int(existing["id"])

    cursor = connection.execute(
        """
        INSERT INTO tags (
            site_id,
            name,
            slug,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            site_id,
            name,
            slug,
            timestamp,
            timestamp,
        ),
    )

    return int(cursor.lastrowid)


def upsert_post(
    connection: sqlite3.Connection,
    *,
    site_reference: str,
    title: str,
    slug: str,
    body: str,
    category_id: int | None,
    published_at: str,
    timestamp: str,
) -> int:
    existing = connection.execute(
        """
        SELECT id
        FROM posts
        WHERE site_id = ?
          AND slug = ?
        LIMIT 1
        """,
        (site_reference, slug),
    ).fetchone()

    values = (
        title,
        body,
        "post",
        category_id,
        "published",
        published_at,
        published_at,
        timestamp,
    )

    if existing is not None:
        connection.execute(
            """
            UPDATE posts
            SET title = ?,
                body = ?,
                type = ?,
                category_id = ?,
                status = ?,
                published_at = ?,
                created_at = ?,
                updated_at = ?,
                static_built_at = NULL
            WHERE id = ?
            """,
            values + (existing["id"],),
        )

        return int(existing["id"])

    cursor = connection.execute(
        """
        INSERT INTO posts (
            site_id,
            title,
            slug,
            body,
            type,
            category_id,
            status,
            published_at,
            created_at,
            updated_at,
            static_built_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
        """,
        (
            site_reference,
            title,
            slug,
            body,
            "post",
            category_id,
            "published",
            published_at,
            published_at,
            timestamp,
        ),
    )

    return int(cursor.lastrowid)


def normalize_datetime(value: object) -> str:
    raw = str(value or "").strip()

    if not raw:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    raw = raw.replace("T", " ")

    if raw.endswith("Z"):
        raw = raw[:-1]

    return raw[:19]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inserta Markdown enriquecido dentro de FARO CMS."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Directorio markdown-ready.",
    )

    parser.add_argument(
        "--database",
        type=Path,
        default=Path("database/database.sqlite"),
        help="Base SQLite de FARO.",
    )

    parser.add_argument(
        "--site",
        default="ensayos",
        help="short_name del sitio FARO.",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=500,
        help="Cantidad de archivos por transacción.",
    )

    args = parser.parse_args()

    if args.batch_size < 1:
        print("ERROR: --batch-size debe ser positivo.", file=sys.stderr)
        return 1

    files = sorted(args.input.glob("*.md"))

    if not files:
        print(
            f"ERROR: no se encontraron Markdown en {args.input}",
            file=sys.stderr,
        )
        return 1

    if not args.database.is_file():
        print(
            f"ERROR: no existe la base {args.database}",
            file=sys.stderr,
        )
        return 1

    connection = sqlite3.connect(args.database)
    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = NORMAL")

        require_schema(connection)

        site = resolve_site(connection, args.site)
        site_id = int(site["id"])
        site_reference = str(site["short_name"])

        imported = 0
        failed = 0

        for offset in range(0, len(files), args.batch_size):
            batch = files[offset:offset + args.batch_size]

            try:
                connection.execute("BEGIN")

                for path in batch:
                    source = path.read_text(encoding="utf-8")
                    metadata, markdown = split_document(source)

                    title = str(metadata.get("title") or "").strip()
                    slug = str(metadata.get("slug") or path.stem).strip()

                    if not title:
                        raise FaroImportError(
                            f"{path.name}: falta title."
                        )

                    if not slug:
                        raise FaroImportError(
                            f"{path.name}: falta slug."
                        )

                    timestamp = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    published_at = normalize_datetime(
                        metadata.get("published_at")
                    )

                    category_id: int | None = None
                    category = metadata.get("category")

                    if isinstance(category, dict):
                        category_name = str(
                            category.get("name") or ""
                        ).strip()

                        category_slug = str(
                            category.get("slug") or ""
                        ).strip()

                        if category_name and category_slug:
                            category_id = upsert_category(
                                connection,
                                site_id=site_id,
                                name=category_name,
                                slug=category_slug,
                                timestamp=timestamp,
                            )

                    body = editorjs_markdown(markdown)

                    post_id = upsert_post(
                        connection,
                        site_reference=site_reference,
                        title=title,
                        slug=slug,
                        body=body,
                        category_id=category_id,
                        published_at=published_at,
                        timestamp=timestamp,
                    )

                    connection.execute(
                        "DELETE FROM post_tag WHERE post_id = ?",
                        (post_id,),
                    )

                    tags = metadata.get("tags", [])

                    if isinstance(tags, list):
                        for tag in tags:
                            if not isinstance(tag, dict):
                                continue

                            tag_name = str(
                                tag.get("name") or ""
                            ).strip()

                            tag_slug = str(
                                tag.get("slug") or ""
                            ).strip()

                            if not tag_name or not tag_slug:
                                continue

                            tag_id = upsert_tag(
                                connection,
                                site_id=site_id,
                                name=tag_name,
                                slug=tag_slug,
                                timestamp=timestamp,
                            )

                            connection.execute(
                                """
                                INSERT OR IGNORE INTO post_tag (
                                    post_id,
                                    tag_id
                                )
                                VALUES (?, ?)
                                """,
                                (post_id, tag_id),
                            )

                    imported += 1

                connection.commit()

                print(
                    f"OK {min(offset + len(batch), len(files))}"
                    f"/{len(files)}"
                )

            except (
                FaroImportError,
                OSError,
                UnicodeError,
                ValueError,
                yaml.YAMLError,
                sqlite3.DatabaseError,
            ) as error:
                connection.rollback()
                failed += len(batch)

                print(
                    f"ERROR lote {offset + 1}: {error}",
                    file=sys.stderr,
                )

                return 1

        print()
        print(f"Importados: {imported}")
        print(f"Fallidos:   {failed}")
        print(f"Base:       {args.database.resolve()}")
        print(f"Sitio:      {site_reference}")

        return 0

    finally:
        connection.close()


if __name__ == "__main__":
    raise SystemExit(main())
