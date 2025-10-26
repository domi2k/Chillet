from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import respx

from chillet import AsyncPalworldClient, PalworldClient

BASE_URL = "http://127.0.0.1:8212"
DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def api_payloads():
    with (DATA_DIR / "api_samples.json").open("r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def sync_client():
    client = PalworldClient(base_url=BASE_URL, password="password")
    yield client
    client.close()


@pytest.fixture
async def async_client():
    client = AsyncPalworldClient(base_url=BASE_URL, password="password")
    async with client:
        yield client


@pytest.fixture(autouse=True)
def palworld_api_autouse(api_payloads):
    with respx.mock(base_url=BASE_URL, assert_all_mocked=True, assert_all_called=False) as router:
        router.get("/v1/api/info", name="get_info").mock(
            return_value=httpx.Response(200, json=api_payloads["info"])
        )
        router.get("/v1/api/players", name="get_players").mock(
            return_value=httpx.Response(200, json={"players": api_payloads["players"]})
        )
        router.get("/v1/api/settings", name="get_settings").mock(
            return_value=httpx.Response(200, json=api_payloads["settings"])
        )
        router.get("/v1/api/metrics", name="get_metrics").mock(
            return_value=httpx.Response(200, json=api_payloads["metrics"])
        )

        for path, name in [
            ("/v1/api/announce", "post_announce"),
            ("/v1/api/kick", "post_kick"),
            ("/v1/api/ban", "post_ban"),
            ("/v1/api/unban", "post_unban"),
            ("/v1/api/save", "post_save"),
            ("/v1/api/shutdown", "post_shutdown"),
            ("/v1/api/stop", "post_stop"),
        ]:
            router.post(path, name=name).mock(
                return_value=httpx.Response(
                    200,
                    headers={
                        "content-type": "text/plain;charset=utf-8",
                        "WWW-Authenticate": 'Basic realm="Pal"',
                        "keep-alive": "timeout=15.000000",
                        "content-length": "0",
                    },
                    content=b"",
                )
            )

        yield router
