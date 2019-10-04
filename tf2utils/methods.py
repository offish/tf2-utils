import requests
import json


def request(url: str, params: dict = {}, headers: dict = {}, allow400: bool = False):
    r = requests.get(url, params=params, headers=headers)

    if r.ok:
        return r.json()
    elif r.status_code in range(400, 499) and allow400:
        return r.json()
    return f'{r.status_code}: {r.reason}'


def post(url: str, headers: dict, data: dict = {}, allow400: bool = False):
    p = requests.post(url, headers=headers, data=data)

    if p.ok:
        return p.json()
    elif p.status_code in range(400, 499) and allow400:
        return p.json()
    return f'{p.status_code}: {p.reason}'
