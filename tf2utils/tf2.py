from tf2utils.methods import request

params = {}


class Items:

    items = 'http://api.steampowered.com/IEconItems_440/GetPlayerItems/v0001/'
    schema = 'http://api.steampowered.com/IEconItems_440/GetSchema/v0001'
    schema_url = 'http://api.steampowered.com/IEconItems_440/GetSchemaURL/v1'
    store = 'http://api.steampowered.com/IEconItems_440/GetStoreMetaData/v1'

    def __init__(self, key: str):
        if key != None:
            params['key'] = key

    def get_player_items(self, steamid: str):
        params['steamid'] = steamid
        return request(self.items, params)

    def get_schema(self, language: str = 'en'):
        params['language'] = language.lower()
        return request(self.schema, params)

    def get_schema_url(self):
        return request(self.schema_url, params)

    def get_store_meta_data(self, language: str = 'en'):
        params['language'] = language
        return request(self.store, params)
