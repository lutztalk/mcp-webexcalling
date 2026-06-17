"""Tests for WebexClient HTTP behaviour: retries, pagination, errors.

These use httpx.MockTransport so no network access is required.
"""

import httpx
import pytest

from mcp_webexcalling.webex_client import WebexClient, WebexApiError


def make_client(handler, **kwargs):
    """Build a WebexClient wired to a mock transport."""
    client = WebexClient(access_token="test-token", retry_backoff=0.0, **kwargs)
    client._client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        headers=client.headers,
    )
    return client


@pytest.mark.asyncio
async def test_successful_get_returns_json():
    def handler(request):
        return httpx.Response(200, json={"displayName": "Ada"})

    client = make_client(handler)
    result = await client.get_my_info()
    assert result["displayName"] == "Ada"
    await client.aclose()


@pytest.mark.asyncio
async def test_retries_on_500_then_succeeds():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(500, json={"message": "boom"})
        return httpx.Response(200, json={"ok": True})

    client = make_client(handler, max_retries=3)
    result = await client._request("GET", "/organizations")
    assert result == {"ok": True}
    assert calls["n"] == 3
    await client.aclose()


@pytest.mark.asyncio
async def test_retries_on_429_honors_retry_after():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, headers={"Retry-After": "0"}, json={"message": "slow down"})
        return httpx.Response(200, json={"ok": True})

    client = make_client(handler, max_retries=2)
    result = await client._request("GET", "/people")
    assert result == {"ok": True}
    assert calls["n"] == 2
    await client.aclose()


@pytest.mark.asyncio
async def test_does_not_retry_on_400():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(400, json={"message": "bad input"})

    client = make_client(handler, max_retries=3)
    with pytest.raises(WebexApiError) as exc:
        await client._request("GET", "/people")
    assert exc.value.status_code == 400
    assert calls["n"] == 1  # no retries on client errors
    await client.aclose()


@pytest.mark.asyncio
async def test_exhausts_retries_then_raises():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(503, json={"message": "unavailable"})

    client = make_client(handler, max_retries=2)
    with pytest.raises(WebexApiError) as exc:
        await client._request("GET", "/organizations")
    assert exc.value.status_code == 503
    assert calls["n"] == 3  # initial + 2 retries
    await client.aclose()


@pytest.mark.asyncio
async def test_network_error_retried_then_raised():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        raise httpx.ConnectError("no route")

    client = make_client(handler, max_retries=2)
    with pytest.raises(WebexApiError):
        await client._request("GET", "/organizations")
    assert calls["n"] == 3
    await client.aclose()


@pytest.mark.asyncio
async def test_pagination_follows_link_header():
    def handler(request):
        page = request.url.params.get("page", "1")
        if "page" not in request.url.params and "cursor" not in str(request.url):
            # first page
            next_url = str(request.url.copy_set_param("page", "2"))
            return httpx.Response(
                200,
                json={"items": [{"id": 1}, {"id": 2}]},
                headers={"Link": f'<{next_url}>; rel="next"'},
            )
        # second page, no next link
        return httpx.Response(200, json={"items": [{"id": 3}]})

    client = make_client(handler)
    items = await client._get_items("/locations", {}, max_results=0)
    assert [i["id"] for i in items] == [1, 2, 3]
    await client.aclose()


@pytest.mark.asyncio
async def test_pagination_respects_max_results():
    def handler(request):
        next_url = str(request.url.copy_set_param("page", "2"))
        return httpx.Response(
            200,
            json={"items": [{"id": 1}, {"id": 2}, {"id": 3}]},
            headers={"Link": f'<{next_url}>; rel="next"'},
        )

    client = make_client(handler)
    items = await client._get_items("/locations", {}, max_results=2)
    assert len(items) == 2
    await client.aclose()


@pytest.mark.asyncio
async def test_204_returns_empty_dict():
    def handler(request):
        return httpx.Response(204)

    client = make_client(handler)
    result = await client._request("DELETE", "/devices/123")
    assert result == {}
    await client.aclose()


@pytest.mark.asyncio
async def test_create_device_by_mac_normalizes_and_validates():
    captured = {}

    def handler(request):
        import json
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json={"id": "dev1"})

    client = make_client(handler)
    await client.create_device_by_mac("aa:bb:cc:dd:ee:ff", "Cisco 8841")
    assert captured["body"]["mac"] == "AABBCCDDEEFF"

    with pytest.raises(ValueError):
        await client.create_device_by_mac("ZZZZ", "Cisco 8841")
    await client.aclose()


@pytest.mark.asyncio
async def test_test_connection_reports_ok():
    def handler(request):
        if request.url.path.endswith("/people/me"):
            return httpx.Response(200, json={"displayName": "Ada", "id": "x", "orgId": "o"})
        if request.url.path.endswith("/organizations"):
            return httpx.Response(200, json={"items": [{"id": "o", "displayName": "Acme"}]})
        return httpx.Response(404)

    client = make_client(handler)
    result = await client.test_connection()
    assert result["ok"] is True
    assert result["authenticatedAs"]["displayName"] == "Ada"
    assert result["adminAccess"] is True
    await client.aclose()


@pytest.mark.asyncio
async def test_test_connection_handles_bad_token():
    def handler(request):
        return httpx.Response(401, json={"message": "invalid token"})

    client = make_client(handler, max_retries=0)
    result = await client.test_connection()
    assert result["ok"] is False
    assert result["status_code"] == 401
    assert "hint" in result
    await client.aclose()
