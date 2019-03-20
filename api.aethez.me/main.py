import requests
import json

r = requests.get('https://api.aethez.me/v1/currencies').JSON()

print(r)
