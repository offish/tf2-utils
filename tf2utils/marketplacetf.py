from tf2utils.methods import request


class Seller:
    dashboard = 'https://marketplace.tf/api/Seller/GetDashboardItems/v2'
    sales = 'https://marketplace.tf/api/Seller/GetSales/v2'

    def __init__(self, key: str):
        self.key = key

    def get_dashboard_items(self):
        '''Fetch all items currently deposited on Marketplace that you can act upon. This does not include items that have sold, 
        are still confirming deposit, or are under review. v2 returns item prices in cents, not dollars.'''

        params = {'key': self.key}
        return request(self.dashboard, params)

    def get_sales(self, num: int, start_before: int):
        '''Fetch the specified number of sales your account has made. v2 now provides prices in cents, not dollars.\n
        `num` - The number of sales to fetch. Defaults to 100. Maximum of 500.\n
        `start_before` - A unix timestamp for pagination. Will return all sales that occurred before this timestamp.'''

        params = {'num': num, 'start_before': start_before, 'key': self.key}
        return request(self.sales, params)


def get_bots():
    '''Fetch a list of all Marketplace.tf bot SteamIDs'''

    bots = 'https://marketplace.tf/api/Bots/GetBots/v1'
    return request(bots)


def get_user_ban(steamid: str):
    '''Fetch any ban associated with the provided SteamID. Bans are only issued in instances of chargeback fraud or alt accounts of chargeback fraudsters.\n
    `steamid` - The user's SteamID64 to fetch ban status for.'''

    bans = 'https://marketplace.tf/api/Bans/GetUserBan/v1'
    params = {'steamid': steamid}
    return request(bans, params)
