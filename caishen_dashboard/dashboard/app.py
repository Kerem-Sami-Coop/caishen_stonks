from .server import app, server # noqa:F401,E261
from .template.stock_layout import graph_layout
import pandas as pd

data_source = "https://raw.githubusercontent.com/plotly/datasets/master/dash-stock-ticker-demo.csv"
df = pd.read_csv(data_source, index_col=False)
df.drop(df.columns[0], inplace=True, axis=1)
app.layout = graph_layout(df, "Stock")

from .callbacks import update_stock # noqa:F401,E261
# Sources: https://github.com/plotly/dash-stock-tickers-demo-app/blob/master/app.py
# https://community.plotly.com/t/splitting-callback-definitions-in-multiple-files/10583
