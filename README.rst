tf2-utils
=========
|license| |stars| |issues| |repo_size| |discord| |code_style| |downloads|

``tf2-utils`` is a collection of tools and utilities for TF2 trading. 
Use 3rd party inventory providers, SKUs formatting, interact with various APIs, websockets and more.
``tf2-utils`` is built on top of `tf2-sku <https://github.com/offish/tf2-sku>`_, `tf2-data <https://github.com/offish/tf2-data>`_ 
and `backpack-tf <https://github.com/offish/backpack-tf>`_.
``tf2-utils`` is a key dependency of `tf2-express <https://github.com/offish/tf2-express>`_.

Donate
------

- BTC: ``bc1q9gmh5x2g9s0pw3282a5ypr6ms8qvuxh3fd7afh``
- `Steam Trade Offer <https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR>`_

You can reach me at `Steam <https://steamcommunity.com/id/confern>`_, 
my `Discord server <https://discord.gg/t8nHSvA>`_ 
or `Discord profile <https://discord.com/users/252183247843229696>`_.

Features
--------

- Built-in currency picking (metal + keys) for sending offers 
- Interact with BackpackTF's API
- Interact with PricesTF's API
- Get MarketplaceTF item prices and stocks
- Get SKUs directly from inventories/offers
- Convert names to SKUs and vice versa
- Fetch inventories using 3rd party providers or your own (avoid being rate-limited)
- Listen for Backpack.TF websocket events
- Listen for Prices.TF websocket events
- Get item properties (``is_craft_hat``, ``get_paint``, ``get_effect`` and more)
- Fetch TF2 Schema data
- Convert SKU/defindex to item image URL
- Calculate scrap and refined prices
- Convert SteamIDs
- and more...

Documentation
-------------
Documentation including usage and examples can be found `here <https://offish.github.io/tf2-utils/>`_.

Installing
----------

.. code-block:: bash

    pip install tf2-utils
    # or 
    python -m pip install tf2-utils

Updating
~~~~~~~~

.. code-block:: bash

    pip install --upgrade tf2-utils tf2-sku tf2-data bptf
    # or 
    python -m pip install --upgrade tf2-utils tf2-sku tf2-data bptf


Development
-----------

Testing
~~~~~~~
.. code-block:: bash

    # tf2-utils/
    pytest

Documentation
~~~~~~~~~~~~~
.. code-block:: bash

    # tf2-utils/docs/
    pip install sphinx furo 
    make clean # .\make.bat <command> on windows
    make html

When submitting a pull request, please make sure to run the tests (+ make new ones if applicable) 
and update the documentation. Run the code through ``black`` and ``flake8`` before submitting.

License
-------
MIT License

Copyright (c) 2019-2025 offish (`confern <https://steamcommunity.com/id/confern>`_)

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

.. |license| image:: https://img.shields.io/github/license/offish/tf2-utils.svg
    :target: https://github.com/offish/tf2-utils/blob/master/LICENSE
    :alt: License

.. |stars| image:: https://img.shields.io/github/stars/offish/tf2-utils.svg
    :target: https://github.com/offish/tf2-utils/stargazers
    :alt: Stars

.. |issues| image:: https://img.shields.io/github/issues/offish/tf2-utils.svg
    :target: https://github.com/offish/tf2-utils/issues
    :alt: Issues

.. |repo_size| image:: https://img.shields.io/github/repo-size/offish/tf2-utils.svg
    :target: https://github.com/offish/tf2-utils
    :alt: Size

.. |discord| image:: https://img.shields.io/discord/467040686982692865?color=7289da&label=Discord&logo=discord
    :target: https://discord.gg/t8nHSvA
    :alt: Discord

.. |code_style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style

.. |downloads| image:: https://img.shields.io/pypi/dm/tf2-utils
    :target: https://pypi.org/project/tf2-utils/
    :alt: Downloads