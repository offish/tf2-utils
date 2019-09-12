from tf2utils.methods import request


class TradeTF:
    schema = 'https://www.trade.tf/api/schema_440.json'
    spreadsheet = 'https://www.trade.tf/api/spreadsheet.json'

    def __init__(self, key: str):
        self.key = key

    def get_schema(self) -> dict:
        params = {'key': self.key}
        return request(self.schema, params)

    def get_spreadsheet(self) -> dict:
        '''Documentation at https://www.trade.tf/user/api/key'''
        params = {'key': self.key}
        return request(self.spreadsheet, params)
