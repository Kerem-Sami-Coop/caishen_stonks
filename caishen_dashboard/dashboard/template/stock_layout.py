from dash_core_components import Dropdown, Store
import dash_html_components as html


def title_style(title, margin_top="20px", margin_bottom="0"):
    title = html.H2(title,
                    style={"display": "inline",
                           "float": "left",
                           "font-size": "2.65em",
                           "margin-left": "7px",
                           "font-weight": "bolder",
                           "font-family": "Product Sans",
                           "color": "rgba(117, 117, 117, 0.95)",
                           "margin-top": margin_top,
                           "margin-bottom": margin_bottom
                           })
    return title


def graph_layout(df, target_column, dropdown_defaults=["YHOO", "GOOGL"]):
    layout = html.Div([
        Store(id="df-store", data={key: df[key].values.tolist() for key in df.columns}),
        html.Div([
            title_style("Finance Explorer")
        ]),
        Dropdown(id="stock-ticker-input",
                 options=[{"label": s[0], "value": str(s[1])}
                          for s in zip(df[target_column].unique(), df[target_column].unique())],
                 value=dropdown_defaults,
                 multi=True
                 ),
        html.Div(id="graphs"),
    ])

    return layout
