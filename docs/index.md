---
title: Chillet
summary: Python SDK for Palworld REST API 
sidebar_title: Home
show_datetime: true
order: 0
extra_css:
  - css/logo.css
---

![Chillet Logo Light](./assets/chillet_logo_light.png){ .logo .only-dark }
![Chillet Logo Dark](./assets/chillet_logo_dark.png){ .logo .only-light }


**Chillet** provides both synchronous and asynchronous clients, allowing developers to manage servers, query metrics, and perform administrative actions with clean, predictable interfaces. Chillet is built with `httpx` and `pydantic`, so it focuses on reliability and type safety.

- **Typed models** - safer code completion and refactoring.
- **Sync & Async** - use the style that fits your app.

!!! info
    Chillet targets the **local Palworld REST API** (typically `http://127.0.0.1:8212`) and Basic Auth (`admin` / password).

## When should I use it?

* You run a **Palworld dedicated server** and want typed, scriptable control.
* You need to **read metrics**, list **players**, or **automate admin actions** (announce, save, kick/ban, shutdown/stop).

## ⚠︎ Disclaimer ⚠︎

This project isn’t endorsed by Pocket Pair, Inc., and doesn’t reflect the views or opinions of Pocket Pair or anyone officially involved in producing or managing Pocket Pair’s products. Pocket Pair, Inc. and its products are trademarks or registered trademarks of Pocket Pair, Inc. Use at your own risk; provided **`AS IS`** per the license.