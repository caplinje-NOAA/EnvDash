# -*- coding: utf-8 -*-
"""
Created on Sun May  7 08:39:35 2023

@author: jim
"""


from dash import Dash, html, callback
from dash.dependencies import Input, Output,State
import dash_leaflet as dl

from . import ids





# render the map
def render(app: Dash) -> html.Div:

    @callback(
    Output(ids.GET_DATA_BUTTON, "n_clicks",allow_duplicate=True),
    Output(ids.LAT_INPUT,'value'),
    Output(ids.LON_INPUT,'value'),
    Output(ids.LAT_INPUT_START, "value"),
    Output(ids.LON_INPUT_START, "value"),

    [Input(ids.MAP_FIG, "clickData"),
    State(ids.GET_DATA_BUTTON, "n_clicks")],
    prevent_initial_call=True
    )
    def click_event_callback(click,n):
        """ On click event, update lat/lon inputs and trigger tab even"""
    
        lat = click['latlng']['lat']
        lng = click['latlng']['lng']

        return n+1,lat,lng,lat,lng
    
    


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