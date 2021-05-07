import dash_html_components as html
from dash_core_components import Graph
from dash.dependencies import Input, Output, State
from caishen_dashboard.dashboard.server import app
from dash.exceptions import PreventUpdate
from caishen_dashboard.data_processing.technical_indicators import bollinger_bands
import colorlover as cl
from itertools import compress

COLORSCALE = cl.scales["9"]["qual"]["Paired"]


@app.callback(
    Output(component_id="graphs", component_property="children"),
    Input(component_id="stock-ticker-input", component_property="value"),
    State(component_id="df-store", component_property="data"))
def update_graph(tickers, data):
    if tickers is None:
        raise PreventUpdate
    graphs = []

    if not tickers:
        graphs.append(html.H3(
            "Select a stock ticker.",
            style={"marginTop": 20, "marginBottom": 20}
        ))
    else:
        for i, ticker in enumerate(tickers):

            mask = [x == ticker for x in data["Stock"]]

            candlestick = {
                "x": list(compress(data["Date"], mask)),
                "open": list(compress(data["Open"], mask)),
                "high": list(compress(data["High"], mask)),
                "low": list(compress(data["Low"], mask)),
                "close": list(compress(data["Close"], mask)),
                "type": "candlestick",
                "name": ticker,
                "legendgroup": ticker,
                "increasing": {"line": {"color": COLORSCALE[0]}},
                "decreasing": {"line": {"color": COLORSCALE[1]}}
            }
            bb_bands = bollinger_bands(data["Close"])
            bollinger_traces = [{
                "x": data["Date"], "y": y,
                "type": "scatter", "mode": "lines",
                "line": {"width": 1, "color": COLORSCALE[(i * 2) % len(COLORSCALE)]},
                "hoverinfo": "none",
                "legendgroup": ticker,
                "showlegend": True if i == 0 else False,
                "name": "{} - bollinger bands".format(ticker)
            } for i, y in enumerate(bb_bands)]
            graphs.append(Graph(
                id=ticker,
                figure={
                    "data": [candlestick] + bollinger_traces,
                    "layout": {
                        "margin": {"b": 0, "r": 10, "l": 60, "t": 0},
                        "legend": {"x": 0}
                    }
                }
            ))

    return graphs
