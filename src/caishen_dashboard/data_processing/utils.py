from enum import Enum


class DateRange(Enum):
    oneDay = "1d"
    fiveDay = "5d"
    threeMonth = "3mo"
    sixMonth = "3mo"
    oneYear = "1y"
    fiveYear = "5y"
    maximum = "max"


class StockInterval(Enum):
    oneMinute = "1m"
    fiveMinute = "5m"
    fifteenMinute = "15m"
    oneDay = "1d"
    oneWeek = "1wk"
    oneMonth = "1mo"
