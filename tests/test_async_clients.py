from __future__ import annotations

import httpx
import pytest

from chillet import AsyncPalworldClient
from chillet.models import InfoResponse, MetricsResponse, PlayersResponse, SettingsResponse

# GET


async def test_get_info_async(async_client, api_payloads):
    response = await async_client.get_info()
    assert isinstance(response, InfoResponse)
    assert response.version == api_payloads["info"]["version"]


async def test_get_players_async(async_client, api_payloads):
    response = await async_client.get_players()
    assert isinstance(response, PlayersResponse)
    assert len(response.players) == len(api_payloads["players"])
    assert response.players[0].name == api_payloads["players"][0]["name"]


async def test_get_settings_async(async_client, api_payloads):
    response = await async_client.get_settings()
    assert isinstance(response, SettingsResponse)
    assert response.ServerPlayerMaxNum == api_payloads["settings"]["ServerPlayerMaxNum"]


async def test_get_metrics_async(async_client, api_payloads):
    response = await async_client.get_metrics()
    assert isinstance(response, MetricsResponse)
    assert response.serverfps == api_payloads["metrics"]["serverfps"]


async def test_get_info_http_error_async(async_client, palworld_api_autouse):
    palworld_api_autouse["get_info"].mock(return_value=httpx.Response(401, text="unauthorized"))
    with pytest.raises(httpx.HTTPStatusError):
        await async_client.get_info()


# POST


async def test_post_announce_async(async_client, palworld_api_autouse):
    response = await async_client.post_announce("Hello!")
    assert response is None
    assert palworld_api_autouse["post_announce"].called


async def test_post_kick_with_message_async(async_client, palworld_api_autouse):
    response = await async_client.post_kick(userid="u1", message="bye")
    assert response is None
    assert palworld_api_autouse["post_kick"].called


async def test_post_ban_without_message_async(async_client, palworld_api_autouse):
    response = await async_client.post_ban(userid="u2", message=None)
    assert response is None
    assert palworld_api_autouse["post_ban"].called


async def test_post_unban_async(async_client, palworld_api_autouse):
    response = await async_client.post_unban("u3")
    assert response is None
    assert palworld_api_autouse["post_unban"].called


async def test_post_save_async(async_client, palworld_api_autouse):
    response = await async_client.post_save()
    assert response is None
    assert palworld_api_autouse["post_save"].called


async def test_post_shutdown_async(async_client, palworld_api_autouse):
    response = await async_client.post_shutdown(waittime=10, message="shutdown soon")
    assert response is None
    assert palworld_api_autouse["post_shutdown"].called


async def test_post_stop_async(async_client, palworld_api_autouse):
    response = await async_client.post_stop()
    assert response is None
    assert palworld_api_autouse["post_stop"].called


async def test_async_aclose_closes():
    client = AsyncPalworldClient(password="pass")
    await client.aclose()
    assert client.client.is_closed
