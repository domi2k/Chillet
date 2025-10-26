<br/>

<h3 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/domi2k/Chillet/.github/assets/chillet_logo_light.png" height="170">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/domi2k/Chillet/.github/assets/chillet_logo_dark.png" height="170">
    <img alt="Chillet" src="https://raw.githubusercontent.com/domi2k/Chillet/.github/assets/chillet_logo_light.png" height="170">
  </picture>
</h3>

<br/>

<p align="center">
Chillet is a modern, fully typed Python SDK designed for Palworld REST API.
</p>

<p align="center">
  <a href="https://github.com/domi2k/Chillet/stargazers"><img src="https://img.shields.io/github/stars/domi2k/Chillet?colorA=363a4f&colorB=ffffff&style=for-the-badge"></a>&nbsp;
  <a href="https://github.com/domi2k/Chillet/issues"><img src="https://img.shields.io/github/issues/domi2k/Chillet?colorA=363a4f&colorB=ffffff&style=for-the-badge"></a>&nbsp;

  <!-- Docs -->
  <a href="https://chillet.domi2k.space/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Docs-Website-ffffff?style=for-the-badge&colorA=363a4f&colorB=ffffff&logo=materialformkdocs&logoColor=black">
      <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/badge/Docs-Website-ffffff?style=for-the-badge&colorA=363a4f&colorB=ffffff&logo=materialformkdocs&logoColor=white">
      <img alt="Docs" src="https://img.shields.io/badge/Docs-Website-ffffff?style=for-the-badge&colorA=363a4f&colorB=ffffff&logo=materialformkdocs&logoColor=black"/>
    </picture>
  </a>&nbsp;

  <!-- PyPI -->
  <a href="https://pypi.org/project/Chillet/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/pypi/v/Chillet?style=for-the-badge&colorA=363a4f&colorB=ffffff&logo=pypi&logoColor=black">
      <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/pypi/v/Chillet?style=for-the-badge&colorA=363a4f&colorB=ffffff&logo=pypi&logoColor=white">
      <img alt="PyPI" src="https://img.shields.io/pypi/v/Chillet?style=for-the-badge&colorA=363a4f&colorB=ffffff&logo=pypi&logoColor=black"/>
    </picture>
  </a>
</p>

<br/>

##

**Chillet** provides both synchronous and asynchronous clients, allowing developers to manage servers, query metrics, and perform administrative actions with clean, predictable interfaces. Chillet is built with `httpx` and `pydantic`, so it focuses on reliability and type safety.

## Installation

### From PyPI (recommended)

```bash
pip install chillet
```

### From source (this repository)

```bash
# clone
git clone https://github.com/domi2k/Chillet.git
cd Chillet

# create env + install (uv)
uv sync --all-extras
```

## Quickstart

### Synchronous

```python
from chillet import PalworldClient

with PalworldClient(password="YOUR_PASSWORD") as client:
    info = client.get_info()
    print(info.servername, info.version)

    metrics = client.get_metrics()
    print("FPS:", metrics.serverfps, "Players:", metrics.currentplayernum)

    client.post_announce("Welcome to the server!")
```

### Asynchronous

```python
import asyncio
from chillet import AsyncPalworldClient

async def main():
    async with AsyncPalworldClient(password="YOUR_PASSWORD") as client:
        info = await client.get_info()
        print(info.servername, info.version)

        metrics = await client.get_metrics()
        print("FPS:", metrics.serverfps, "Players:", metrics.currentplayernum)

        await client.post_announce("Welcome to the server!")

asyncio.run(main())
```

## Documentation

Full documentation with tutorials and API reference is available [here](https://chillet.domi2k.space/).

## Contact

If you have any questions about this project, feel free to contact me on `Discord`.

<p align="center">
  <a href="https://discordapp.com/users/329876941631127554"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/-Discord-FFFFFF?style=for-the-badge&logo=Discord&logoColor=black">
    <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/badge/-Discord-000000?style=for-the-badge&logo=Discord&logoColor=white">
    <img src="https://img.shields.io/badge/-Discord-FFFFFF?style=for-the-badge&logo=Discord&logoColor=black"/>
  </picture></a>&nbsp;
</p>

## ⚠︎ Disclaimer ⚠︎

This project isn’t endorsed by Pocket Pair, Inc., and doesn’t reflect the views or opinions of Pocket Pair or anyone officially involved in producing or managing Pocket Pair’s products. Pocket Pair, Inc. and its products are trademarks or registered trademarks of Pocket Pair, Inc. Use at your own risk; provided **`AS IS`** per the license.

&nbsp;

<p align="center">
  <a href="LICENSE">
    <img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&colorA=363a4f&colorB=ffffff"/>
  </a>
</p>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/domi2k/Chillet/.github/assets/footer_light.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/domi2k/Chillet/.github/assets/footer_dark.png">
    <img alt="Footer" src="https://raw.githubusercontent.com/domi2k/Chillet/.github/assets/footer_light.png">
  </picture>
</p>