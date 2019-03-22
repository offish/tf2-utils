import requests
import json

r = requests.get('https://api.aethez.me/tf2/currencies').json()

def get_key_price(r):
    return r['currencies']['key']

def get_time(r):
    return r['time']

if r['success'] == "true": #aethez fix this now
    print(get_key_price(r))
    print(get_time(r))
else:
    print('Wrong response from API. Success: {}'.format(r['success']))
