from caishen_dashboard.utils.stock import StockData


def test_stock_retrieval():
    init = StockData(symbols="AAPL", date_range="1y", interval="1mo")
    data = init.retrieveData()
    print(data)
    assert False
    # assert shape[0] > 0
