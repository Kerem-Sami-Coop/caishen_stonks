from .errors import InvalidInputError, MissingEnvVarError
import os


class StockHistoryRequestBuilder:
    """Class to build the request for stock data.

    The class can be used to generate a HTTPS request to retrieve the history of upto 10 stocks from Rapid API's Yahoo
    Finance Low Latency vendor. The details for the request can be accessed from the conf dictionary created within
    the class

    Args:
        tickers (str): String of stock tickers combined with commas. Cannot be more than 10.
        date_range (str): The extent of the history to load. Expected values are "1d", "5d", "3mo", "6mo", "1y", "5y",
        "max"
        interval (str): The aggregate value for a specific interval of stock(s). Expected values "1m", "5m", "15m",
        "1d", "1wk", "1mo"

    Attributes:
        conf (dict): Dictionary that contains the URL, headers and the querystring to generate the request. These
        information can be accessed from the keys url, headers and querystring

    Raises:
        InvalidInputError: Requested more than 10 stocks
        InvalidInputError: Invalid date range
        InvalidInputError: Invalid interval
        MissingEnvVarError: If RAPIDAPI_HOST or RAPIDAPI_ENDPOINT are missing

    To use:
        >>> from caishen_dashboard.data_processing.stock import StockHistoryRequestBuilder
        >>> request = StockHistoryRequestBuilder(tickers="AAPL,MSFT", date_range="3mo", interval="1d")
        >>> request.conf.keys()
        dict_keys(['headers', 'url', 'querystring'])

    """
    def __init__(self, tickers: str, date_range: str, interval: str):
        self._validate(tickers, date_range, interval)
        self.conf = self._build_conf(tickers, date_range, interval)

    def _validate(self, tickers, date_range, interval):
        if len(tickers.split(",")) > 10:
            raise InvalidInputError("Requested more than 10 stocks")
        if date_range not in ["1d", "5d", "3mo", "6mo", "1y", "5y", "max"]:
            raise InvalidInputError("Invalid date range")
        if interval not in ["1m", "5m", "15m", "1d", "1wk", "1mo"]:
            raise InvalidInputError("Invalid interval")

    def _build_conf(self, tickers, date_range, interval):
        REQUIRED_VARS = ["RAPIDAPI_HOST", "RAPIDAPI_ENDPOINT"]
        ENV_VARS = os.environ.keys()

        for var in REQUIRED_VARS:
            if var not in ENV_VARS:
                raise MissingEnvVarError(f"Missing {var} from enviroment variables")

        conf = {}
        host = os.environ["RAPIDAPI_HOST"]
        endpoint = os.environ["RAPIDAPI_ENDPOINT"]
        headers = {
            "x-rapidapi-key": os.environ["RAPID_API_TOKEN"],
            "x-rapidapi-host": os.environ["RAPIDAPI_HOST"]
        }
        conf["headers"] = headers

        url = f"https://{host}/{endpoint}"
        conf["url"] = url

        querystring = {"symbols": tickers,
                       "range": date_range,
                       "interval": interval
                       }
        conf["querystring"] = querystring

        return conf
