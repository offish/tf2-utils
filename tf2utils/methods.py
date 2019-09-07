import requests
import json


def request(url: str, params: dict = {}, headers: dict = {}):
    r = requests.get(url, params=params, headers=headers)

    if r.ok or r.status_code in range(400, 499):
        return r.json()
    return f'{r.status_code}: {r.reason}'


def post(url: str, headers: dict, data: dict = {}):
    p = requests.post(url, headers=headers, data=data)

    if p.ok or p.status_code in range(400, 499):
        return p.json()
    return f'{p.status_code}: {p.reason}'
