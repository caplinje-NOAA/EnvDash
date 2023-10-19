# -*- coding: utf-8 -*-
"""
Created on Sun May  7 08:39:35 2023

@author: jim
"""

import plotly.express as px
from dash import Dash, dcc, html, callback, ALL, MATCH
from dash.dependencies import Input, Output,State
import dash_leaflet as dl
import pandas as pd
from . import ids, bathplot, ssplot

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

renderer = {'bath-tab':bathplot,'ssp-tab':ssplot,'seabed-tab':None}


def render(app: Dash) -> html.Div:






    @callback(
    Output(ids.TABS,'value'),
    Output(ids.LAT_INPUT,'value'),
    Output(ids.LON_INPUT,'value'),
    Output(ids.LAT_INPUT_START, "value"),
    Output(ids.LON_INPUT_START, "value"),

    [Input(ids.MAP_FIG, "clickData"),
    State(ids.TABS, 'value')],
   
    )
    def update_figure(click,value):
    
        lat = click['latlng']['lat']
        lng = click['latlng']['lng']



        return value,lat,lng,lat,lng
    
    


    return html.Div([
    dl.Map([dl.TileLayer(),
            dl.LayerGroup(id=ids.MAP_LAYER),
            dl.LayerGroup(id=ids.TRANS_MAP_LAYER),
            dl.ScaleControl(position="bottomleft")],
            center=[39,-94],
            zoom=4,
            id=ids.MAP_FIG, 
            style={'width': '100%', 'height': '60vh', 'margin': "auto", "display": "block"}),
])
    # update_map()
    # return html.Div(id=ids.MAP)
    #return update_map()


#https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}