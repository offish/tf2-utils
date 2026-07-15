# tf2-utils
[![Stars](https://img.shields.io/github/stars/offish/tf2-utils.svg)](https://github.com/offish/tf2-utils/stargazers)
[![Issues](https://img.shields.io/github/issues/offish/tf2-utils.svg)](https://github.com/offish/tf2-utils/issues)
[![Size](https://img.shields.io/github/repo-size/offish/tf2-utils.svg)](https://github.com/offish/tf2-utils)
[![Discord](https://img.shields.io/discord/467040686982692865?color=7289da&label=Discord&logo=discord)](https://discord.gg/t8nHSvA)
[![Downloads](https://img.shields.io/pypi/dm/tf2-utils)](https://pypi.org/project/tf2-utils/)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

tf2-utils is a library of tools and utilities for TF2 trading.

tf2-utils is built on top of these dependencies:
- [backpack-tf](https://github.com/offish/backpack-tf)
- [tf2-sku](https://github.com/offish/tf2-sku)
- [tf2-data](https://github.com/offish/tf2-data)

tf2-utils is a key dependency of the trading bot [tf2-express](https://github.com/offish/tf2-express).

## Donate
- BTC: `bc1q9gmh5x2g9s0pw3282a5ypr6ms8qvuxh3fd7afh`
- [Steam Trade Offer](https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR)

You can reach me at [Steam](https://steamcommunity.com/id/confern), my [Discord server](https://discord.gg/t8nHSvA) or [Discord profile](https://discord.com/users/252183247843229696).

## Features
- Built-in currency picking (metal + keys) for sending offers 
- Interact with BackpackTF's API
- Get MarketplaceTF item prices and stocks
- Get SKUs directly from inventories/offers
- Convert names to SKUs and vice versa
- Fetch inventories using 3rd party providers or your own (avoid being rate-limited)
- Listen for Backpack.TF websocket events
- Get item properties (`is_craft_hat`, `get_paint`, `get_effect` and more)
- Fetch TF2 Schema data
- Convert SKU/defindex to item image URL
- Calculate scrap and refined prices
- Convert SteamIDs
- and more...


## Installing
```bash
pip install tf2-utils
# or 
python -m pip install tf2-utils
```

## Updating
```bash
pip install --upgrade tf2-utils tf2-sku tf2-data bptf
# or 
python -m pip install --upgrade tf2-utils tf2-sku tf2-data bptf
```

## Testing
```bash
# tf2-utils/
pytest
```

When submitting a pull request, please make sure to run the tests and add new ones where applicable. This repository uses [Ruff](https://github.com/astral-sh/ruff) for formatting and linting, so please use it as well.

## License
MIT License

Copyright (c) 2019 offish ([confern](https://steamcommunity.com/id/confern))

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.