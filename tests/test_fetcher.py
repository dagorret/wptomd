from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from wptomd import fetcher


def install_mock_transport(
    monkeypatch: pytest.MonkeyPatch,
    handler: Callable[[httpx.Request], httpx.Response],
) -> None:
    real_client = httpx.Client
    transport = httpx.MockTransport(handler)

    def client_factory(**kwargs: object) -> httpx.Client:
        assert kwargs["headers"] == {"User-Agent": fetcher.USER_AGENT}
        assert kwargs["timeout"] == fetcher.DEFAULT_TIMEOUT
        assert kwargs["follow_redirects"] is True
        return real_client(transport=transport, **kwargs)

    monkeypatch.setattr(fetcher.httpx, "Client", client_factory)


def test_fetch_html_returns_decoded_html(monkeypatch: pytest.MonkeyPatch) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["User-Agent"] == fetcher.USER_AGENT
        content = "<html><body><p>Título en español</p></body></html>".encode(
            "iso-8859-1"
        )
        return httpx.Response(
            200,
            content=content,
            headers={"Content-Type": "text/html; charset=iso-8859-1"},
        )

    install_mock_transport(monkeypatch, handler)

    html_source = fetcher.fetch_html("https://example.com/articulo/")

    assert "Título en español" in html_source


def test_fetch_html_reports_404(monkeypatch: pytest.MonkeyPatch) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="No encontrado")

    install_mock_transport(monkeypatch, handler)

    with pytest.raises(
        fetcher.FetchError,
        match=r"Error HTTP 404 al descargar https://example.com/falta/",
    ):
        fetcher.fetch_html("https://example.com/falta/")


def test_fetch_html_reports_connection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("Tiempo agotado", request=request)

    install_mock_transport(monkeypatch, handler)

    with pytest.raises(
        fetcher.FetchError,
        match=r"No se pudo conectar con https://example.com/lento/",
    ):
        fetcher.fetch_html("https://example.com/lento/")


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com/articulo/",
        "example.com/articulo/",
        "https:///sin-host/",
    ],
)
def test_fetch_html_rejects_non_http_urls(url: str) -> None:
    with pytest.raises(
        fetcher.FetchError,
        match="La URL debe usar http o https.",
    ):
        fetcher.fetch_html(url)
