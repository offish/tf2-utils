import requests
import json

key = 'Mann Co. Supply Crate Key'
file = 'prices.json'

r = requests.get('https://api.tf2automatic.com/v1/currencies').json()

data = {}

if r['success'] == True:
    buy = r['result']['keys']['price']['value']
    data[key] = {
        "buy": buy,
        "sell": buy + 0.11
    }
    print('Successfully added {} to {}! Tries left: {}'.format(key, file, r['rate']['remaining']))
else:
    print('There was an error when trying to access the API. Success: {}'.format(r['success']))

with open(file, 'w') as outfile:
    json.dump(data, outfile, indent=4)
