from iexfinance.stocks import get_historical_data
import os


class StockData:
    def __init__(self, start, end, stock, **kwargs):
        self.start = start
        self.end = end
        self.stock = stock
        self.kwargs = kwargs

    def retrieveData(self):
        data = get_historical_data(self.stock, start=self.start,
                                   end=self.end, **self.kwargs)
        return data
