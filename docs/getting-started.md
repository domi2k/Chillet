---
title: Getting Started
sidebar_title: Getting Started
show_datetime: true
order: 1
external_links:
  "Palworld docs": https://docs.palworldgame.com/api/rest-api/palwold-rest-api
---

Before you script anything fancy, install **Chillet** and ensure your Palworld server exposes the local REST API (default `http://127.0.0.1:8212`) with a password set for the `admin` user. Link to official Palworld documentation for more information above.

## Install

Add the package to your project.

=== "uv"

        :::bash
        uv pip install chillet


=== "pip"

        :::bash
        pip install chillet


After installation, you can talk to your local server immediately - defaults assume `http://127.0.0.1:8212` and username `admin` (you must provide the password). If your server runs elsewhere, override `base_url`.

!!! note "First request (sync)"

        :::python
        from chillet import PalworldClient

        with PalworldClient(password="YOUR_PASSWORD") as client:
            info = client.get_info()
            print(info.servername, info.version)

            metrics = client.get_metrics()
            print("FPS:", metrics.serverfps)
