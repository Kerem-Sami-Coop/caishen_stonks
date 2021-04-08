from caishen_dashboard.utils.stock import StockData
import requests
import requests_mock
import io
import os


def test_request():
    details = StockData(symbols="AAPL", date_range="1y", interval="1mo")
    conf = details.conf

    with requests_mock.Mocker() as mock:
        host = os.environ["RAPIDAPI_HOST"]
        endpoint = os.environ["RAPIDAPI_ENDPOINT"]
        mock.register_uri("GET",
                          f"https://{host}/{endpoint}?symbols=AAPL&range=1y&interval=1mo",
                          status_code="200",
                          body=io.BytesIO(
                              b'{"AAPL":{"symbol":"AAPL","end":null,"start":null,"timestamp":[1588305600,1590984000,1593576000,1596254400,1598932800,1601524800,1604203200,1606798800,1609477200,1612155600,1614574800,1617249600,1617912003],"close":[79.485,91.2,106.26,129.04,115.81,108.86,119.05,132.69,131.96,121.26,122.15,127.9,130.36],"previousClose":null,"chartPreviousClose":66.518,"dataGranularity":300}}'  # noqa: E501
                                          )
                          )
        response = requests.request("GET", conf["url"], headers=conf["headers"],
                                    params=conf["querystring"])

    assert response.status_code == "200"
