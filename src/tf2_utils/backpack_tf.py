import json

from websockets.sync.client import connect


class BackpackTFWebsocket:
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
        :param callback: Function pointer where you want the data to end up

        :param solo_entries: If data to callback should be solo entries or a batched list
        :type solo_entries: bool
        :param headers: Additional headers to send to the socket
        :type headers: dict
        :param settings: Additional websocket settings as a dict to be unpacked
        :type settings: dict
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
