import boto3
import os
import pandas as pd
from caishen_stonks.errors import MissingEnvVarError
import io
import json


class AWSDataCache(object):
    def __init__(self, tickers, bucket_name="caishen-dev-raw"):
        required_env_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
        for var in required_env_vars:
            if var not in os.environ:
                raise MissingEnvVarError(f"{var} enviroment variable is missing")
        self.s3_client = boto3.client("s3")
        self.bucket = bucket_name
        self.data = self.update_cache(tickers)

    def retrieve_data(self, ticker, file_name="data.csv"):
        data_io = io.BytesIO()
        self.s3_client.download_fileobj(self.bucket, f"raw/{ticker}/{file_name}", data_io)
        content = json.loads(data_io.getvalue())
        return content

    def update_cache(self, tickers):
        self.tickers = tickers
        temp = []
        for ticker in tickers:
            temp.append(self.retrieve_data(ticker))

        output = pd.json_normalize(temp)
        return output
