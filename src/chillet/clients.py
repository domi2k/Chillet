"""Palworld REST API clients (sync & async) built on top of httpx.

This module provides two thin, typed clients:
- `PalworldClient` - synchronous, using `httpx.Client`
- `AsyncPalworldClient` - asynchronous, using `httpx.AsyncClient`

Both expose small, typed methods for Palworld endpoints and a shared
`BaseClient.handle_response` that validates JSON responses into Pydantic models.
"""

from __future__ import annotations

from types import TracebackType
from typing import Literal, overload

import httpx

from .models import (
    AnnounceRequest,
    BanRequest,
    InfoResponse,
    KickRequest,
    MetricsResponse,
    PlayersResponse,
    RequestT,
    ResponseT,
    SettingsResponse,
    ShutdownRequest,
    UnbanRequest,
)

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
Scheme = Literal["http", "https"]


class BaseClient:
    """Base building block for both sync and async clients."""

    base_url: str
    """Base URL of the Palworld REST API (e.g. ``"http://127.0.0.1:8212"``)"""
    username: str
    """Username used for basic authentication"""
    password: str
    """Password used for basic authentication"""
    auth: tuple[str, str]
    """auth: Tuple used by httpx for basic authentication (``(username, password)``)"""
    timeout: httpx.Timeout
    """Default `httpx.Timeout` applied to all requests."""
    headers: dict[str, str]
    """Default headers sent with every request (defaults to ``{"Accept": "application/json"}``)"""

    def __init__(
        self,
        *,
        base_url: str,
        username: str,
        password: str,
        headers: dict[str, str] | None,
    ) -> None:
        self.base_url = base_url
        self.auth = (username, password)
        self.timeout = httpx.Timeout(connect=5.0, read=10.0, write=10.0, pool=10.0)
        self.headers = headers or {"Accept": "application/json"}

    @staticmethod
    @overload
    def handle_response(response: httpx.Response, response_model: type[ResponseT]) -> ResponseT: ...

    @staticmethod
    @overload
    def handle_response(response: httpx.Response, response_model: None = ...) -> None: ...

    @staticmethod
    def handle_response(
        response: httpx.Response, response_model: type[ResponseT] | None = None
    ) -> ResponseT | None:
        """Map an `httpx.Response` to a typed Pydantic model or `None`."""

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise httpx.HTTPStatusError(
                f"{e.request.method} {e.request.url} -> {response.status_code}: {detail}",
                request=e.request,
                response=response,
            ) from None

        if response_model is None:
            return None

        return response_model.model_validate(response.json())


class PalworldClient(BaseClient):
    """Synchronous client for the Palworld REST API.

    Example:
        ```python
        from chillet.clients import PalworldClient

        with PalworldClient(username="admin", password="pass") as client:
            metrics = client.get_metrics()
            print(metrics.serverfps)
        ```
    """

    client: httpx.Client

    def __init__(
        self,
        *,
        base_url: str = "http://127.0.0.1:8212",
        username: str = "admin",
        password: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(base_url=base_url, username=username, password=password, headers=headers)
        self.client = httpx.Client(
            base_url=self.base_url, auth=self.auth, timeout=self.timeout, headers=self.headers
        )

    def __enter__(self) -> PalworldClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        self.close()
        return None

    def close(self) -> None:
        """Close the underlying `httpx.Client`."""

        self.client.close()

    @overload
    def invoke(
        self,
        method: HttpMethod,
        path_template: str,
        *,
        payload: RequestT | None = ...,
        response_model: type[ResponseT],
    ) -> ResponseT: ...

    @overload
    def invoke(
        self,
        method: HttpMethod,
        path_template: str,
        *,
        payload: RequestT | None = ...,
        response_model: None = ...,
    ) -> None: ...

    def invoke(
        self,
        method: HttpMethod,
        path_template: str,
        *,
        payload: RequestT | None = None,
        response_model: type[ResponseT] | None = None,
    ) -> ResponseT | None:
        """Low-level request helper used by high-level methods.

        Args:
            method: HTTP method.
            path_template: Path part under `base_url` (e.g. ``"/v1/api/info"``).
            payload: Optional Pydantic request model; serialized as JSON.
            response_model: Optional response model type to validate into.

        Returns:
            Parsed response model or `None` (see `handle_response` contract).
        """

        json_data = None
        if payload:
            json_data = payload.model_dump(exclude_none=True)

        response = self.client.request(
            method,
            url=path_template,
            json=json_data,
        )
        return self.handle_response(response, response_model)

    def get_info(self) -> InfoResponse:
        return self.invoke("GET", "/v1/api/info", response_model=InfoResponse)

    def get_players(self) -> PlayersResponse:
        return self.invoke("GET", "/v1/api/players", response_model=PlayersResponse)

    def get_settings(self) -> SettingsResponse:
        return self.invoke("GET", "/v1/api/settings", response_model=SettingsResponse)

    def get_metrics(self) -> MetricsResponse:
        return self.invoke("GET", "/v1/api/metrics", response_model=MetricsResponse)

    def post_announce(self, message: str) -> None:
        payload = AnnounceRequest(message=message)
        self.invoke("POST", "/v1/api/announce", payload=payload)

    def post_kick(self, *, userid: str, message: str | None = None) -> None:
        payload = KickRequest(userid=userid, message=message)
        self.invoke("POST", "/v1/api/kick", payload=payload)

    def post_ban(self, *, userid: str, message: str | None = None) -> None:
        payload = BanRequest(userid=userid, message=message)
        self.invoke("POST", "/v1/api/ban", payload=payload)

    def post_unban(self, userid: str) -> None:
        payload = UnbanRequest(userid=userid)
        self.invoke("POST", "/v1/api/unban", payload=payload)

    def post_save(self) -> None:
        self.invoke("POST", "/v1/api/save")

    def post_shutdown(self, *, waittime: int, message: str | None = None) -> None:
        payload = ShutdownRequest(waittime=waittime, message=message)
        self.invoke("POST", "/v1/api/shutdown", payload=payload)

    def post_stop(self) -> None:
        self.invoke("POST", "/v1/api/stop")


class AsyncPalworldClient(BaseClient):
    """Asynchronous client for the Palworld REST API.

    Example:
        ```python
        from chillet.clients import AsyncPalworldClient

        async with AsyncPalworldClient(username="admin", password="pass") as client:
            metrics = await client.get_metrics()
            print(metrics.serverfps)
        ```
    """

    client: httpx.AsyncClient

    def __init__(
        self,
        *,
        base_url: str = "http://127.0.0.1:8212",
        username: str = "admin",
        password: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(base_url=base_url, username=username, password=password, headers=headers)
        self.client = httpx.AsyncClient(
            base_url=self.base_url, auth=self.auth, timeout=self.timeout, headers=self.headers
        )

    async def __aenter__(self) -> AsyncPalworldClient:
        await self.client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        await self.aclose()
        return None

    async def aclose(self) -> None:
        """Close the underlying `httpx.AsyncClient`."""

        await self.client.aclose()

    @overload
    async def invoke(
        self,
        method: HttpMethod,
        path_template: str,
        *,
        payload: RequestT | None = ...,
        response_model: type[ResponseT],
    ) -> ResponseT: ...

    @overload
    async def invoke(
        self,
        method: HttpMethod,
        path_template: str,
        *,
        payload: RequestT | None = ...,
        response_model: None = ...,
    ) -> None: ...

    async def invoke(
        self,
        method: HttpMethod,
        path_template: str,
        *,
        payload: RequestT | None = None,
        response_model: type[ResponseT] | None = None,
    ) -> ResponseT | None:
        """Low-level request helper used by high-level methods.

        Args:
            method: HTTP method.
            path_template: Path part under `base_url` (e.g. ``"/v1/api/info"``).
            payload: Optional Pydantic request model; serialized as JSON.
            response_model: Optional response model type to validate into.

        Returns:
            Parsed response model or `None` (see `handle_response` contract).
        """

        json_data = None
        if payload:
            json_data = payload.model_dump(exclude_none=True)

        response = await self.client.request(
            method,
            url=path_template,
            json=json_data,
        )
        return self.handle_response(response, response_model)

    async def get_info(self) -> InfoResponse:
        return await self.invoke("GET", "/v1/api/info", response_model=InfoResponse)

    async def get_players(self) -> PlayersResponse:
        return await self.invoke("GET", "/v1/api/players", response_model=PlayersResponse)

    async def get_settings(self) -> SettingsResponse:
        return await self.invoke("GET", "/v1/api/settings", response_model=SettingsResponse)

    async def get_metrics(self) -> MetricsResponse:
        return await self.invoke("GET", "/v1/api/metrics", response_model=MetricsResponse)

    async def post_announce(self, message: str) -> None:
        payload = AnnounceRequest(message=message)
        await self.invoke("POST", "/v1/api/announce", payload=payload)

    async def post_kick(self, *, userid: str, message: str | None = None) -> None:
        payload = KickRequest(userid=userid, message=message)
        await self.invoke("POST", "/v1/api/kick", payload=payload)

    async def post_ban(self, *, userid: str, message: str | None = None) -> None:
        payload = BanRequest(userid=userid, message=message)
        await self.invoke("POST", "/v1/api/ban", payload=payload)

    async def post_unban(self, userid: str) -> None:
        payload = UnbanRequest(userid=userid)
        await self.invoke("POST", "/v1/api/unban", payload=payload)

    async def post_save(self) -> None:
        await self.invoke("POST", "/v1/api/save")

    async def post_shutdown(self, *, waittime: int, message: str | None = None) -> None:
        payload = ShutdownRequest(waittime=waittime, message=message)
        await self.invoke("POST", "/v1/api/shutdown", payload=payload)

    async def post_stop(self) -> None:
        await self.invoke("POST", "/v1/api/stop")
