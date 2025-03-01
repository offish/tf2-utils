import time
from typing import Any

import requests

from .exceptions import EmptyResponse, InternalServerError, PricesTFError, RateLimited
from .utils import to_refined


class PricesTF:
    URL = "https://api2.prices.tf"

    def __init__(self) -> None:
        self._access_token = ""
        self._headers = {}

    @staticmethod
    def _format_price(data: dict) -> dict:
        return {
            "buy": {
                "keys": data["buyKeys"],
                "metal": to_refined(data["buyHalfScrap"] / 2),
            },
            "sell": {
                "keys": data["sellKeys"],
                "metal": to_refined(data["sellHalfScrap"] / 2),
            },
        }

    @staticmethod
    def _validate_response(response: dict[str, Any]) -> None:
        if not response:
            raise EmptyResponse("response from server was empty")

        status_code = response.get("statusCode")

        if status_code == 500:
            raise InternalServerError("there was an interal server error")

        if status_code == 429:
            raise RateLimited("currently ratelimited")

    def _set_header(self, header: dict) -> None:
        self._headers = header

    def _get(self, endpoint: str, params: dict = {}) -> dict:
        url = self.URL + endpoint
        response = requests.get(url, headers=self._headers, params=params)
        res = response.json()
        self._validate_response(res)

        return res

    def _post(self, endpoint: str) -> tuple[dict, int]:
        url = self.URL + endpoint
        response = requests.post(url, headers=self._headers)
        res = response.json()
        self._validate_response(res)

        return (res, response.status_code)

    def _get_prices_till_page(
        self, page_limit: int, print_rate_limit: bool = False
    ) -> dict:
        prices = {}
        current_page = 1
        # set higher than current page first time
        max_page = page_limit if page_limit != -1 else 2

        while current_page < max_page:
            try:
                response = self.get_prices(current_page)
            except RateLimited:
                timeout = 60

                if print_rate_limit:
                    print(f"rate limited from prices.tf, waiting {timeout} seconds")

                time.sleep(timeout)
                continue

            if "items" not in response:
                raise PricesTFError("could not find any items in response")

            for item in response["items"]:
                prices[item["sku"]] = self._format_price(item)

            current_page = response["meta"]["currentPage"] + 1
            total_pages = response["meta"]["totalPages"]

            if page_limit == -1:
                max_page = total_pages

        return prices

    def get_history(
        self, sku: str, page: int = 1, limit: int = 100, order: str = "ASC"
    ) -> dict:
        return self._get(
            f"/history/{sku}", {"page": page, "limit": limit, "order": order}
        )

    def get_price(self, sku: str) -> dict:
        return self._get(f"/prices/{sku}")

    def get_prices(self, page: int, limit: int = 100, order: str = "DESC") -> dict:
        return self._get("/prices", {"page": page, "limit": limit, "order": order})

    def get_all_prices(self, print_rate_limit: bool = False) -> dict:
        return self._get_prices_till_page(-1, print_rate_limit)

    def update_price(self, sku: str) -> tuple[dict, int]:
        return self._post(f"/prices/{sku}/refresh")

    def request_access_token(self) -> None:
        res, _ = self._post("/auth/access")

        self._validate_response(res)

        self._access_token = res["accessToken"]

        self._set_header(
            {
                "accept": "application/json",
                "Authorization": f"Bearer {self._access_token}",
            }
        )

    @property
    def access_token(self) -> str:
        if not self._access_token:
            raise PricesTFError("Access token was never set!")

        return self._access_token

    @property
    def headers(self) -> dict:
        return self._headers
