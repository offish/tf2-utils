from .prices_tf import PricesTF

import json

from websockets.sync.client import connect


class BackpackTFSocket:
    URL = "wss://ws.backpack.tf/events"

    def __init__(
        self,
        callback,
        solo_entries: bool = True,
        headers: dict = {"batch-test": True},
        max_size: int | None = None,
        settings: dict = {},
    ) -> None:
        """
        Args:
            callback: Function pointer where you want the data to end up
            solo_entries: If data to callback should be solo entries or a batched list
            headers: Additional headers to send to the socket
            settings: Additional websocket settings as a dict to be unpacked
        """
        self.callback = callback
        self.solo_entries = solo_entries
        self.headers = headers
        self.max_size = max_size
        self.settings = settings

    def process_messages(self, data: str) -> None:
        messages = json.loads(data)

        if not self.solo_entries:
            self.callback(messages)
            return

        for message in messages:
            payload = message["payload"]
            self.callback(payload)

    def listen(self) -> None:
        """Listen for messages from BackpackTF"""
        with connect(
            self.URL,
            additional_headers=self.headers,
            max_size=self.max_size,
            **self.settings,
        ) as websocket:
            while True:
                data = websocket.recv()
                self.process_messages(data)


class PricesTFSocket:
    URL = "wss://ws.prices.tf"

    def __init__(
        self,
        callback,
        settings: dict = {},
    ) -> None:
        """
        Args:
            callback: Function pointer where you want the data to end up
            settings: Additional websocket settings as a dict to be unpacked
        """
        self.callback = callback
        self.prices_tf = PricesTF()
        self.settings = settings

    def process_message(self, message: str) -> None:
        data = json.loads(message)
        self.callback(data)

    def listen(self) -> None:
        """Listen for messages from PricesTF."""
        self.prices_tf.request_access_token()
        headers = self.prices_tf.get_headers()

        with connect(
            self.URL,
            additional_headers=headers,
            **self.settings,
        ) as websocket:
            while True:
                message = websocket.recv()
                self.process_message(message)
