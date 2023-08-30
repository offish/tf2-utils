# tf2-utils
[![License](https://img.shields.io/github/license/offish/tf2-utils.svg)](https://github.com/offish/tf2-utils/blob/master/LICENSE)
[![Stars](https://img.shields.io/github/stars/offish/tf2-utils.svg)](https://github.com/offish/tf2-utils/stargazers)
[![Issues](https://img.shields.io/github/issues/offish/tf2-utils.svg)](https://github.com/offish/tf2-utils/issues)
[![Size](https://img.shields.io/github/repo-size/offish/tf2-utils.svg)](https://github.com/offish/tf2-utils)
[![Discord](https://img.shields.io/discord/467040686982692865?color=7289da&label=Discord&logo=discord)](https://discord.gg/t8nHSvA)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tools and utilities for TF2 trading. Use 3rd party inventory providers, get SKUs directly from inventories, listen to BackpackTF's websocket and more.

## Donate
- BTC: `bc1qntlxs7v76j0zpgkwm62f6z0spsvyezhcmsp0z2`
- [Steam Trade Offer](https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR)

## Usage

### Inventory fetching
```python
from tf2_utils import Inventory

# using 3rd party provider to avoid being rate-limited
provider = Inventory("steamsupply", "9st947vs0qmgfpeqde1gj92l0oqmhysm")

# using steam as inventory provider
provider = Inventory() # or Inventory("steamcommunity")

# get an inventory
inventory = provider.fetch("76561198253325712")
```

### Gettings SKUs from inventories
**NOTE: NOT ALL SKU ATTRIBUTES ARE ADDED YET**
#### Get SKUs implicitly
```python
from tf2_utils import Inventory, map_inventory

provider = Inventory("steamcommunity")

user_inventory = provider.fetch("76561198253325712")
inventory = map_inventory(user_inventory, add_skus=True)
```

#### Get a particular item's SKU
```python
from tf2_utils import get_sku

inventory = map_inventory(user_inventory)

for item in inventory:
    sku = get_sku(item)
```

### BackpackTF Websocket
#### Handle one listing at a time
```python
from tf2_utils import BackpackTFWebsocket

def my_function(data: dict):
    print("got data!", data)

socket = BackpackTFWebsocket(my_function)

socket.listen()
```

#### Handle list of listings at a time
```python
from tf2_utils import BackpackTFWebsocket

def my_function(data: list[dict]):
    print("got listings")

    for listing in data:
        print("listing", listing)

socket = BackpackTFWebsocket(my_function, solo_entries=False)

socket.listen()
```

## Setup
### Install
```bash
pip install tf2-utils
# or 
python -m pip install tf2-utils
```

### Upgrade
```bash
pip upgrade tf2-utils
# or 
python -m pip upgrade tf2-utils
```

