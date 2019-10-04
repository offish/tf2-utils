import enum


class ETradeOfferState(enum.IntEnum):
    Invalid = 1
    Active = 2
    Accepted = 3
    Countered = 4
    Expired = 5
    Canceled = 6
    Declined = 7
    InvalidItems = 8
    NeedsConfirmation = 9
    CanceledBySecondFactor = 10
    Escrow = 11


class EItemQuality(enum.IntEnum):
    Normal = 0
    Genuine = 1
    Vintage = 3
    Unusual = 5
    Unique = 6
    Community = 7
    Valve = 8
    SelfMade = 9
    Strange = 11
    Haunted = 13
    Collectors = 14
    DecoratedWeapon = 15


class ESteamCurrency(enum.IntEnum):
    USD = 1
    GBP = 2
    EUR = 3
    CHF = 4
    RUB = 5
    PLN = 6
    BRL = 7
    JPY = 8
    NOK = 9
    IDR = 10
    MYR = 11
    PHP = 12
    SGD = 13
    THB = 14
    VND = 15
    KRW = 16
    TRY = 17
    UAH = 18
    MXN = 19
    CAD = 20
    AUD = 21
    NZD = 22
    CNY = 23
    INR = 24
    CLP = 25
    PEN = 26
    COP = 27
    ZAR = 28
    HKD = 29
    TWD = 30
    SAR = 31
    AED = 32
