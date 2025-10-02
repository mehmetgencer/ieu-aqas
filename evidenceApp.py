#!/usr/bin/python3
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_ag_grid as dag
import plotly.express as px
import json, pprint
import pandas as pd
from pathlib import Path
from settings import localsettings, checkpasswd
import evidencelib

storage=localsettings["storage"]
courses=json.load(open(Path(localsettings["storage"])/"courselist.json","r"))
departments=list(courses.keys())
program_outcomes=json.load(open(Path(localsettings["storage"])/"pos.json","r"))

app = Dash(server=False,routes_pathname_prefix="/program_level/")
app.layout = html.Div([
    html.H1(children='IEU İşletme AQAS 2', style={'textAlign':'center'}),
])