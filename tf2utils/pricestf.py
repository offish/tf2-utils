from tf2utils.methods import request, post

headers = {}


class Prices:

    schema = 'https://api.prices.tf/schema'
    items = 'https://api.prices.tf/items/{}'

    def __init__(self, key):
        self.key = key

        if self.key != None:
            headers['Authorization'] = 'Token ' + self.key

    def get_schema(self) -> dict:
        '''Gets all items recorded'''

        return request(self.schema, {}, headers)

    def get_pricelist(self, src: str, cur: str) -> dict:
        '''Gets all suggested prices\n
        `src` - The source of the prices. bptf, mplc\n
        `cur` - Currency to return the prices in USD, EUR, etc.'''

        url = self.items.format('?')
        params = {'src': src, 'cur': cur.upper()}
        return request(url, params, headers)

    def get_prices(self, sku: str, src: str, cur: str) -> dict:
        '''Gets the suggested price of an item\n
        `sku` - The SKU of the item\n
        `src` - The source of the prices. bptf, mplc\n
        `cur` - Currency to return the prices in USD, EUR, etc.'''

        url = self.items.format(sku) + '?'
        params = {'src': src, 'cur': cur.upper()}
        return request(url, params, headers)

    def get_price_history(self, sku: str, src: str, cur: str) -> dict:
        '''Gets the history of suggested prices\n
        `src` - The source of the prices. bptf, mplc\n
        `cur` - Currency to return the prices in USD, EUR, etc.\n
        `sku` - The SKU of the item'''

        params = {'src': src, 'cur': cur.upper()}
        url = self.items.format(sku) + '/history?'
        return request(url, params, headers)

    
class Snapshots:

    items = 'https://api.prices.tf/items/{}'
    snapshot = 'https://api.prices.tf/snapshots/{}'

    def __init__(self, key):
        self.key = key

        if self.key != None:
            headers['Authorization'] = 'Token ' + self.key

    def request_new_price(self, sku: str) -> dict:
        '''Requests an item to be priced\n
        `sku` - The SKU of the item'''

        url = self.items.format(sku)
        data = {'source': 'bptf'}
        return post(url, headers=headers, data=data)

    def get_snapshot(self, sku: str) -> dict:
        '''Gets most recent snapshot of an item\n
        `sku` - The SKU of the item'''

        url = self.items.format(sku) + '/snapshot'
        return request(url, {}, headers)

    def get_all_snapshot(self, empty: bool, listings: bool, sku: str) -> dict:
        '''Gets all snapshots of an item\n
        `empty` - False\n
        `listings` - True\n
        `sku` - The SKU of the item'''

        url = self.items.format(sku) + '/snapshots?'
        params = {'empty': empty, 'listings': listings}
        return request(url, params, headers)

    def get_single_snapshot(self, listing_id: str) -> dict:
        '''Gets a single snapshot with listings\n
        `listing_id` - Listing id to search for (5c7c222f3857c355db65f4ee)'''

        url = self.snapshot.format(listing_id)
        return request(url, {}, headers)

    def request_new_snapshot(self, sku: str) -> dict:
        '''Requests a new snapshot to be taken of an item\n
        `sku` - The SKU of the item'''

        url = self.items.format(sku) + '/snapshot'
        return post(url, headers=headers)
