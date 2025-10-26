---
title: Using Clients
sidebar_title: Using Clients
show_datetime: true
order: 2
---

Chillet exposes **two clients**:

- `PalworldClient` — synchronous, easy to script and cron.
- `AsyncPalworldClient` — asynchronous, ideal for apps/daemons that already use `asyncio`.


=== "Synchronous usage"

        :::python
        from chillet import PalworldClient

        with PalworldClient(password="YOUR_PASSWORD") as client:
            info = client.get_info()
            print(info.servername, info.version)
        
            metrics = client.get_metrics()
            print("FPS:", metrics.serverfps, "Players:", metrics.currentplayernum)

            client.post_announce("Welcome to the server!")

=== "Asynchronous usage"

        :::python
        from chillet import AsyncPalworldClient

        async with AsyncPalworldClient(password="YOUR_PASSWORD") as client:
            info = await client.get_info()
            print(info.servername, info.version)
    
            metrics = await client.get_metrics()
            print("FPS:", metrics.serverfps, "Players:", metrics.currentplayernum)

            await client.post_announce("Welcome to the server!")


### Customizing connection

Both clients share the same surface and sane defaults:

- Base URL: `http://127.0.0.1:8212`
- Username: `admin` (password **required**)
- Timeouts: connect `5s`, read `10s`, write `10s`, pool `10s`
- Headers: `Accept: application/json`


        :::python
        from chillet import PalworldClient
        
        client = PalworldClient(
            base_url="http://192.168.1.50:8212",
            username="admin",
            password="YOUR_PASSWORD",
        )
        with client:
            print(client.get_info().version)


## Endpoints at a glance

> **Note:** Names below reflect the actual SDK methods.

| SDK Method                           | HTTP   | Path                | Request model     | Response model     |
|:-------------------------------------|--------|:--------------------|-------------------|--------------------|
| `get_info()`                         | `GET`  | `/v1/api/info`      | —                 | `InfoResponse`     |
| `get_players()`                      | `GET`  | `/v1/api/players`   | —                 | `PlayersResponse`  |
| `get_settings()`                     | `GET`  | `/v1/api/settings`  | —                 | `SettingsResponse` |
| `get_metrics()`                      | `GET`  | `/v1/api/metrics`   | —                 | `MetricsResponse`  |
| `post_announce(message)`             | `POST` | `/v1/api/announce`  | `AnnounceRequest` | —                  |
| `post_kick(userid, message?)`        | `POST` | `/v1/api/kick`      | `KickRequest`     | —                  |
| `post_ban(userid, message?)`         | `POST` | `/v1/api/ban`       | `BanRequest`      | —                  |
| `post_unban(userid)`                 | `POST` | `/v1/api/unban`     | `UnbanRequest`    | —                  |
| `post_save()`                        | `POST` | `/v1/api/save`      | —                 | —                  |
| `post_shutdown(waittime, message?)`  | `POST` | `/v1/api/shutdown`  | `ShutdownRequest` | —                  |
| `post_stop()`                        | `POST` | `/v1/api/stop`      | —                 | —                  |

Async client provides the **same** methods with `await`.

## Error handling

All non-2xx responses raise `httpx.HTTPStatusError`. The exception message includes method, URL, status code, and body (JSON/text) when available.

    :::python
    from httpx import HTTPStatusError
    from chillet import PalworldClient
    
    try:
        with PalworldClient(password="YOUR_PASSWORD") as client:
            client.post_ban(userid="steam:12345", message="See you next time.")
    except HTTPStatusError as e:
        print(e)  # e.g. "POST http://127.0.0.1:8212/v1/api/ban -> 400: {...}"

**Typical causes**

* Wrong password or disabled REST API → `401`
* Invalid path/payload / endpoint unavailable → `400`
* Server not reachable / wrong base URL → connection error (before status)