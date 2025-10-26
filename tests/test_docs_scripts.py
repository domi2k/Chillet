from __future__ import annotations

from httpx import HTTPStatusError

from chillet import AsyncPalworldClient, PalworldClient


def test_readme_sync():
    with PalworldClient(password="YOUR_PASSWORD") as client:
        info = client.get_info()
        print(info.servername, info.version)

        metrics = client.get_metrics()
        print("FPS:", metrics.serverfps, "Players:", metrics.currentplayernum)

        client.post_announce("Welcome to the server!")


async def test_readme_async():
    async with AsyncPalworldClient(password="YOUR_PASSWORD") as client:
        info = await client.get_info()
        print(info.servername, info.version)

        metrics = await client.get_metrics()
        print("FPS:", metrics.serverfps, "Players:", metrics.currentplayernum)

        await client.post_announce("Welcome to the server!")


def test_clients_exception():
    try:
        with PalworldClient(password="YOUR_PASSWORD") as client:
            client.post_ban(userid="steam:12345", message="See you next time.")
    except HTTPStatusError as e:
        print(e)
