import json
from typing import Callable

from websockets.sync.client import ClientConnection, connect

from .prices_tf import PricesTF


class PricesTFWebsocket:
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
        self._callback = callback
        self._prices_tf = PricesTF()
        self._settings = settings

    def _process_message(self, ws: ClientConnection, message: str) -> None:
        data = json.loads(message)

        if data.get("type") != "AUTH_REQUIRED":
            self._callback(data)
            return

        # our auths are only valid for 10 minutes at a time
        # pricestf requests us to authenticate again
        self._prices_tf.request_access_token()

        payload = {
            "type": "AUTH",
            "data": {"accessToken": self._prices_tf.access_token},
        }

        ws.send(json.dumps(payload))

    def listen(self) -> None:
        """Listen for messages from PricesTF."""
        self._prices_tf.request_access_token()
        headers = self._prices_tf.headers

        with connect(
            "wss://ws.prices.tf",
            additional_headers=headers,
            **self._settings,
        ) as websocket:
            while True:
                message = websocket.recv()
                self._process_message(websocket, message)
