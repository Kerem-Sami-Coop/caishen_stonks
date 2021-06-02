from enum import Enum


class DateRange(Enum):
    oneDay = "1d"
    fiveDay = "5d"
    threeMonth = "3mo"
    sixMonth = "3mo"
    oneYear = "1y"
    fiveYear = "5y"
    # maximum can cause errors so it is removed temporarily
    # see https://www.notion.so/Yahoo-Finance-Low-Latency-Rapid-API-61a3f7aa451d4558bc3d89f38dd39494
    # maximum = "max"


class StockInterval(Enum):
    oneMinute = "1m"
    fiveMinute = "5m"
    fifteenMinute = "15m"
    oneDay = "1d"
    oneWeek = "1wk"
    oneMonth = "1mo"
