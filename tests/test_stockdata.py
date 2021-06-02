from caishen_stonks.stock import StockHistoryRequestBuilder
from caishen_stonks.constants import DateRange, StockInterval
import requests
import requests_mock
import io
import os
import pytest


def test_correct_request_single():
    details = StockHistoryRequestBuilder(tickers=["AAPL"],
                                         date_range=DateRange.oneYear,
                                         interval=StockInterval.oneMonth)
    conf = details.conf

    with requests_mock.Mocker() as mock:
        host = os.environ["RAPIDAPI_HOST"]
        endpoint = os.environ["RAPIDAPI_ENDPOINT"]
        mock.register_uri("GET",
                          f"https://{host}/{endpoint}?symbols=AAPL&range=1y&interval=1mo",
                          status_code="200",
                          body=io.BytesIO(
                              b'{"AAPL":{"symbol":"AAPL","end":null,"start":null,"timestamp":[1588305600,1590984000,1593576000,1596254400,1598932800,1601524800,1604203200,1606798800,1609477200,1612155600,1614574800,1617249600,1617912003],"close":[79.485,91.2,106.26,129.04,115.81,108.86,119.05,132.69,131.96,121.26,122.15,127.9,130.36],"previousClose":null,"chartPreviousClose":66.518,"dataGranularity":300}}'  # noqa: E501
                                          ))  # noqa: E126
        response = requests.request("GET", conf["url"], headers=conf["headers"],
                                    params=conf["querystring"])

    assert response.status_code == "200"


def test_correct_request_multiple():
    details = StockHistoryRequestBuilder(tickers=["AAPL", "MSFT"],
                                         date_range=DateRange.oneYear,
                                         interval=StockInterval.oneMonth)
    conf = details.conf

    with requests_mock.Mocker() as mock:
        host = os.environ["RAPIDAPI_HOST"]
        endpoint = os.environ["RAPIDAPI_ENDPOINT"]
        mock.register_uri("GET",
                          f"https://{host}/{endpoint}?symbols=AAPL,MSFT&range=1y&interval=1mo",
                          status_code="200",
                          )
        response = requests.request("GET", conf["url"], headers=conf["headers"],
                                    params=conf["querystring"])

    assert response.status_code == "200"


def test_false_ticker_request_1a():
    with pytest.raises(Exception) as ex:
        StockHistoryRequestBuilder(tickers=["AAPL"] * 11, date_range=DateRange.oneYear, interval=StockInterval.oneMonth)
    assert "The requested number of tickers is not between 1 and 10" in str(ex.value)


def test_false_ticker_request_1b():
    with pytest.raises(Exception) as ex:
        StockHistoryRequestBuilder(tickers=[], date_range=DateRange.oneYear, interval=StockInterval.oneMonth)
    assert "The requested number of tickers is not between 1 and 10" in str(ex.value)


def test_false_ticker_request_2():
    with pytest.raises(Exception) as ex:
        StockHistoryRequestBuilder(tickers="AAPL", date_range=DateRange.oneYear, interval=StockInterval.oneMonth)
    assert "Invalid tickers type" in str(ex.value)


def test_false_daterange_request():
    with pytest.raises(Exception) as ex:
        StockHistoryRequestBuilder(tickers=["AAPL"], date_range="10y", interval="1mo")
    assert "Invalid date range type" in str(ex.value)


def test_false_interval_request():
    with pytest.raises(Exception) as ex:
        StockHistoryRequestBuilder(tickers=["AAPL"], date_range=DateRange.oneYear, interval="5mo")
    assert "Invalid interval type" in str(ex.value)


def test_missing_env_var():
    temp = os.environ["RAPID_API_TOKEN"]
    del os.environ["RAPID_API_TOKEN"]
    with pytest.raises(Exception) as ex:
        StockHistoryRequestBuilder(tickers=["AAPL"], date_range=DateRange.oneYear, interval=StockInterval.oneMonth)
    os.environ["RAPID_API_TOKEN"] = temp
    assert "Missing RAPID_API_TOKEN" in str(ex.value)
