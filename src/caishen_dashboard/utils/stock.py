import requests
from .errors import InvalidInputError, MissingEnvVarError
import os


class StockData:
    def __init__(self, symbols, date_range, interval):
        self._validate(date_range, interval)
        self.symbols = symbols
        self.date_range = date_range
        self.interval = interval
        self.conf = self._build_conf()

    def _validate(self, date_range, interval):
        if date_range not in ["1d", "5d", "3mo", "6mo", "1y", "5y", "max"]:
            raise InvalidInputError("Invalid stock date range")
        if interval not in ["1m", "5m", "15m", "1d", "1wk", "1mo"]:
            raise InvalidInputError("Invalid stock interval")

    def _build_conf(self):
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

        querystring = {"symbols": self.symbols,
                       "range": self.date_range,
                       "interval": self.interval
                       }
        conf["querystring"] = querystring

        return conf

    def retrieveData(self):
        response = requests.request("GET", self.conf["url"], headers=self.conf["headers"],
                                    params=self.conf["querystring"])
        data = response.content
        return data
