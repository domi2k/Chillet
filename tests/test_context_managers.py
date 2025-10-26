from __future__ import annotations

from chillet import AsyncPalworldClient, PalworldClient


def test_sync_context_manager_closes_client():
    with PalworldClient(password="password") as session:
        assert not session.client.is_closed

    assert session.client.is_closed


async def test_async_context_manager_closes_client():
    async with AsyncPalworldClient(password="password") as session:
        assert not session.client.is_closed

    assert session.client.is_closed
