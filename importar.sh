#!/usr/bin/env bash
set -euo pipefail

SITEMAP="${1:-sitemap.html}"

python3 - "$SITEMAP" <<'PY' \
    | sort -u \
    | while read -r url; do
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit


BASE_URL = "https://dagorret.com.ar/"
EXCLUDED_PATHS = (
    "/feed/",
    "/comments/feed/",
    "/wp-content/",
    "/wp-json/",
    "/author/",
    "/category/",
    "/tag/",
)


class SitemapLinkParser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return

        for name, value in attrs:
            if name.lower() != "href" or not value:
                continue

            if not value.startswith(BASE_URL):
                continue

            path = urlsplit(value).path
            if (
                path.startswith(EXCLUDED_PATHS)
                or path == "/xmlrpc.php"
                or re.fullmatch(r"/(about|sitemap|politica-privacidad)/?", path)
            ):
                continue

            print(value)


parser = SitemapLinkParser()
with open(sys.argv[1], encoding="utf-8") as sitemap:
    parser.feed(sitemap.read())
PY
        echo "==> $url"
        wptomd convert-url "$url" --force
      done
