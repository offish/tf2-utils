import json
from typing import Callable

from websockets.sync.client import ClientConnection, connect

from .prices_tf import PricesTF


class PricesTFWebsocket:
    URL = "wss://ws.prices.tf"

    def __init__(
        self,
        callback: Callable[[dict], None],
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

    def process_message(self, ws: ClientConnection, message: str) -> None:
        data = json.loads(message)

        # our auths are only valid for 10 minutes at a time
        # pricestf requests us to authenticate again
        if data.get("type") == "AUTH_REQUIRED":
            self.prices_tf.request_access_token()
            ws.send(
                json.dumps(
                    {
                        "type": "AUTH",
                        "data": {"accessToken": self.prices_tf.access_token},
                    }
                )
            )
            return

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
                self.process_message(websocket, message)
