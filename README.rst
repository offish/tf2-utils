tf2-utils
=========

.. image:: https://img.shields.io/github/license/offish/tf2-utils.svg
    :target: https://github.com/offish/tf2-utils/blob/master/LICENSE
    :alt: License

.. image:: https://img.shields.io/github/stars/offish/tf2-utils.svg
    :target: https://github.com/offish/tf2-utils/stargazers
    :alt: Stars

.. image:: https://img.shields.io/github/issues/offish/tf2-utils.svg
    :target: https://github.com/offish/tf2-utils/issues
    :alt: Issues

.. image:: https://img.shields.io/github/repo-size/offish/tf2-utils.svg
    :target: https://github.com/offish/tf2-utils
    :alt: Size

.. image:: https://img.shields.io/discord/467040686982692865?color=7289da&label=Discord&logo=discord
    :target: https://discord.gg/t8nHSvA
    :alt: Discord

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style

.. image:: https://img.shields.io/pypi/dm/tf2-utils
    :target: https://pypi.org/project/tf2-utils/
    :alt: Downloads

Tools and utilities for TF2 trading. Use 3rd party inventory providers, get SKUs directly from inventories, listen to BackpackTF's websocket and more.

Donate
------

- BTC: ``bc1qntlxs7v76j0zpgkwm62f6z0spsvyezhcmsp0z2``
- `Steam Trade Offer <https://steamcommunity.com/tradeoffer/new/?partner=293059984&token=0-l_idZR>`_

Features
--------

- Uses `tf2-sku <https://github.com/offish/tf2-sku>`_
- Uses `tf2-data <https://github.com/offish/tf2-data>`_
- Get SKUs directly from inventories/offers
- Convert name to SKU and vice versa
- Fetch inventories using 3rd party providers (avoid being rate-limited)
- Listen for Backpack.TF websocket events
- Listen for Prices.TF websocket events
- Interact with Prices.TF's API
- Get item properties (``is_craft_hat``, ``get_paint``, ``get_effect`` etc.)
- Fetch TF2 Schema data
- Convert SKU/defindex to item image URL
- Calculate scrap and refined prices


Installing
----------

.. code-block:: bash

    pip install tf2-utils
    # or 
    python -m pip install tf2-utils

Updating
~~~~~~~~

.. code-block:: bash

    pip install --upgrade tf2-utils tf2-sku tf2-data
    # or 
    python -m pip install --upgrade tf2-utils tf2-sku tf2-data


Documentation
-------------
Documentation including usage and examples can be found `here <https://offish.github.io/tf2-utils/>`_.

Development
-----------

Testing
~~~~~~~
.. code-block:: bash

    # tf2-utils/
    python -m unittest

Documentation
~~~~~~~~~~~~~
.. code-block:: bash

    # tf2-utils/docs/
    pip install sphinx furo 
    make clean # .\make.bat <command> on windows
    make html
