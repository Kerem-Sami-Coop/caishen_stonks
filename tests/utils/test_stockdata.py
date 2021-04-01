from caishen_dashboard.utils.stock import StockData


def test_stock_data():
    init = StockData(stock="AAPL", start="20190101", end="20190103", output_format="pandas")
    data = init.retrieveData()
    shape = data.shape

    assert shape[0] > 0
