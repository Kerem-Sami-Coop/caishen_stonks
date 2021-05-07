from flask import Flask
from dash import Dash

server = Flask("caishen")
app = Dash(server=server)
