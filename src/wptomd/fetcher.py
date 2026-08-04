from __future__ import annotations

from urllib.parse import urlsplit

import httpx

USER_AGENT = "wptomd/0.1 (+https://github.com/dagorret/wptomd)"
DEFAULT_TIMEOUT = 10.0


class FetchError(Exception):
    """Error esperado al validar o descargar una página."""

    def __init__(self, message: str, *, reason: str | None = None) -> None:
        super().__init__(message)
        self.reason = reason or message


def validate_url(url: str) -> None:
    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname
    except ValueError as error:
        raise FetchError("La URL debe usar http o https.") from error

    if parsed.scheme not in {"http", "https"} or not hostname:
        raise FetchError("La URL debe usar http o https.")


def fetch_html(url: str) -> str:
    """Descarga una página HTTP y devuelve su HTML decodificado."""
    validate_url(url)

    try:
        with httpx.Client(
            headers={"User-Agent": USER_AGENT},
            timeout=DEFAULT_TIMEOUT,
            follow_redirects=True,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
    except httpx.HTTPStatusError as error:
        status_code = error.response.status_code
        raise FetchError(
            f"Error HTTP {status_code} al descargar {url}",
            reason=(
                f"HTTP {status_code} {error.response.reason_phrase}"
            ),
        ) from error
    except httpx.InvalidURL as error:
        raise FetchError("La URL debe usar http o https.") from error
    except httpx.TimeoutException as error:
        raise FetchError(
            f"No se pudo conectar con {url}",
            reason="Tiempo de espera agotado.",
        ) from error
    except httpx.RequestError as error:
        raise FetchError(
            f"No se pudo conectar con {url}",
            reason="No se pudo establecer la conexión.",
        ) from error

    return response.text
