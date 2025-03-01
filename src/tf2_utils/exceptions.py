# generic
class TF2UtilsError(Exception):
    pass


class InvalidInventory(TF2UtilsError):
    pass


# pricestf
class PricesTFError(TF2UtilsError):
    pass


class InternalServerError(PricesTFError):
    pass


class RateLimited(PricesTFError):
    pass


class EmptyResponse(PricesTFError):
    pass


# marketplacetf
class MarketplaceTFException(TF2UtilsError):
    pass


class SKUDoesNotMatch(MarketplaceTFException):
    pass


class NoAPIKey(MarketplaceTFException):
    pass
