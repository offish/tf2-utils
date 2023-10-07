from websockets.sync.client import connect
import requests


class PricesTFError(Exception):
    """General error"""


class InternalServerError(PricesTFError):
    """Something went wrong"""


class RateLimited(PricesTFError):
    """Rate limited"""


class EmptyResponse(PricesTFError):
    """Response was empty"""


class PricesTF:
    URL = "https://api2.prices.tf"

    def __init__(self) -> None:
        self.access_token = ""
        self.header = {}

    @staticmethod
    def has_code(response, code: int) -> bool:
        return response.get("statusCode") == code

    @staticmethod
    def validate_response(response) -> None:
        if not response:
            raise EmptyResponse("response from server was empty")

        if PricesTF.has_code(response, 500):
            raise InternalServerError("there was an interal server error")

        if PricesTF.has_code(response, 429):
            raise RateLimited("currently ratelimited")

    def _get(self, endpoint: str, params: dict = {}) -> dict:
        response = requests.get(self.URL + endpoint, headers=self.header, params=params)

        res = response.json()

        self.validate_response(res)
        return res

    def _post(self, endpoint: str) -> tuple[dict, int]:
        response = requests.post(self.URL + endpoint, headers=self.header)

        res = response.json()

        self.validate_response(res)
        return (res, response.status_code)

    def _set_header(self, header: dict) -> None:
        self.header = header

    def update_price(self, sku: str) -> tuple[dict, int]:
        return self._post(f"/prices/{sku}/refresh")

    def get_prices(self, page: int) -> dict:
        return self._get("/prices", {"page": page, "limit": 100, "order": "DESC"})

    def get_headers(self) -> dict:
        return self.header

    def request_access_token(self) -> None:
        res, _ = self._post("/auth/access")

        self.validate_response(res)

        access_token = res["accessToken"]
        self.access_token = access_token

        self._set_header(
            {
                "accept": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            }
        )
