from typing import List
import os
from .errors import InvalidInputError, MissingEnvVarError
from .constants import DateRange, StockInterval


class StockHistoryRequestBuilder:
    """Class to build the request for stock data.

    The class can be used to generate a HTTPS request to retrieve the history of upto 10 stocks from Rapid API's Yahoo
    Finance Low Latency vendor. The details for the request can be accessed from the conf dictionary created within
    the class

    Args:
        tickers (List[str]): String of stock tickers combined with commas. Cannot be more than 10.
        date_range (enum): The extent of the history to load.
        interval (enum): The aggregate value for a specific interval of stock(s).

    Attributes:
        conf (dict): Dictionary that contains the URL, headers and the querystring to generate the request. These
        information can be accessed from the keys url, headers and querystring

    Raises:
        TypeError: Invalid tickers type
        InvalidInputError: The requested number of tickers is not between 1 and 10
        TypeError: Invalid date range type
        TypeError: Invalid interval type
        MissingEnvVarError: If RAPIDAPI_HOST or RAPIDAPI_ENDPOINT are missing
    """
    def __init__(self, tickers: List[str], date_range: DateRange, interval: StockInterval):
        self._validate(tickers, date_range, interval)
        self.conf = self._build_conf(tickers, date_range, interval)

    def _validate(self, tickers, date_range, interval):
        if not isinstance(tickers, list):
            raise TypeError("Invalid tickers type. Please use a list for tickers")
        if len(tickers) > 10 or len(tickers) == 0:
            raise InvalidInputError("The requested number of tickers is not between 1 and 10")
        if not isinstance(date_range, DateRange):
            raise TypeError("Invalid date range type. Please use DateRange class")
        if not isinstance(interval, StockInterval):
            raise TypeError("Invalid interval type. Please use StockInterval class")

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

        querystring = {"symbols": ",".join(tickers),
                       "range": date_range.value,
                       "interval": interval.value
                       }
        conf["querystring"] = querystring

        return conf
