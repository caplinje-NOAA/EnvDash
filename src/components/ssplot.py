# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:53:59 2023

@author: jim
"""

from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State, ALL
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
import xarray as xr
import numpy as np
import dash_leaflet as dl
import pandas as pd

from ..dataHandling.sspretriever import retrieveSSprofiles,getWOAgrid, toDataFrame
from . import ids, alerts


def decodeCoord(coordstr):
    stringArray = coordstr.strip('[').strip(']').split(',')
    lat = float(stringArray[0])
    lon = float(stringArray[1])
    return [lat,lon]

def buildFig(df):
    
    
   
    fig = px.line(df,x='C',y='depth',color='Coordinate')
    print(fig['data'][2]['name'])
    return fig
    
def buildMapMarkers(df):
    markers = []
    locations = df['Coordinate'].unique()
    for loc in locations:
        center = decodeCoord(loc)
        markers.append(
            dl.Circle(center=center,radius=500,children=dl.Tooltip(f'WOA (SSP) data, {loc}'), 
                      id={'type':ids.WOA_DATA_MARKER,'location':loc},color='blue',opacity=1)
                      )
            
    return markers,locations
            
    

def render(click_lat_lng,minutes,month,bathsource):
    

        
        
    lat_pnt = click_lat_lng[0]
    lon_pnt = click_lat_lng[1]
    minutes = minutes/2
    lonRange = [lon_pnt-minutes/60,lon_pnt+minutes/60]
    latRange = [lat_pnt-minutes/60,lat_pnt+minutes/60]
    df = retrieveSSprofiles(lonRange,latRange,Month=month,as_DataFrame=True)
   
    #[gridLon,gridLat] = getWOAgrid(df)
    #nearest = ds.sel(lon=lon_pnt,lat=lat_pnt,method='nearest')
    #C = np.array(nearest.C)
    #depth = np.array(nearest.depth)
    #nonnan = ~np.isnan(C)
    #C = C[nonnan]
    #depth = depth[nonnan]
    fig = buildFig(df)
    fig.update_layout(title=f'{month} SSP near [{click_lat_lng[0]:.3f},{click_lat_lng[1]:.3f}]',
               xaxis_title='Sound Speed (m/s)',
               yaxis_title='Depth (m)')
    fig['layout']['yaxis']['autorange'] = "reversed"
    
    mapLayers = [dl.Marker(position=click_lat_lng, children=dl.Tooltip("(Center, {:.3f}, {:.3f})".format(*click_lat_lng)))]
    markers,locations = buildMapMarkers(df)
    mapLayers=mapLayers+markers
    alert = alerts.getAlert('success','Successfully loaded WOA temperature and sailinity data.')
    figure = html.Div(dcc.Graph(figure=fig,style={'width': '60vh', 'height': '60vh'}, id=ids.SSP_PLOT))
    
    return figure, mapLayers, alert

# def render(app: Dash) -> html.Div:
#     # @app.callback(
#     #     Output(ids.BATH_PLOT, "children"),
#     #     [
#     #         Input(ids.MAP_FIG, "click_lat_lng"),
#     #     ],
#     # )
#     # def wait_for_data(click_lat_lng) -> html.Div:
       

#     #     return html.Div(dbc.Spinner(color="primary"))
    
#     @app.callback(
#         Output(ids.SSP_PLOT, "children"),
#         Output(ids.MAP_LAYER, "children"),
#         Output(ids.LAT_INPUT, "value"),
#         Output(ids.LON_INPUT, "value"),
#         Output(ids.SSP_ALERT_DIV, "children"),
#         Output(ids.SSP_INCLUDE_DROPDOWN,"options"),
#         Output(ids.SSP_INCLUDE_DROPDOWN,"value"),
#         [
#             Input(ids.MAP_FIG, "click_lat_lng"),
#             State(ids.BB_MIN,'value'),
#             State(ids.SSP_MONTH_DROPDOWN,'value')
#         ],
#     )
#     def update_chart(click_lat_lng,minutes,month) -> html.Div:
#         lat_pnt = click_lat_lng[0]
#         lon_pnt = click_lat_lng[1]
#         minutes = minutes/2
#         lonRange = [lon_pnt-minutes/60,lon_pnt+minutes/60]
#         latRange = [lat_pnt-minutes/60,lat_pnt+minutes/60]
#         ds = retrieveSSprofiles(lonRange,latRange,Month=month)
#         df = ds_to_df(ds)
#         [gridLon,gridLat] = getWOAgrid(ds)
#         nearest = ds.sel(lon=lon_pnt,lat=lat_pnt,method='nearest')
#         C = np.array(nearest.C)
#         depth = np.array(nearest.depth)
#         nonnan = ~np.isnan(C)
#         C = C[nonnan]
#         depth = depth[nonnan]
#         fig = buildFig(ds)
#         fig.update_layout(title=f'SSP near {str(click_lat_lng)}',
#                    xaxis_title='Sound Speed (m/s)',
#                    yaxis_title='Depth (m)')
#         fig['layout']['yaxis']['autorange'] = "reversed"
        
#         mapLayers = [dl.Rectangle(bounds=[[latRange[1], lonRange[1]], [latRange[0], lonRange[0]]],children=dl.Tooltip("Bounding box for bathymetry")),
#                      dl.Marker(position=click_lat_lng, children=dl.Tooltip("(Center, {:.3f}, {:.3f})".format(*click_lat_lng)))]
#         markers,locations = buildMapMarkers(ds)
#         mapLayers=mapLayers+markers

#         return [html.Div(dcc.Graph(figure=fig,style={'width': '60vh', 'height': '60vh'}), id=ids.SSP_PLOT), 
#                             mapLayers, 
#                             lat_pnt, 
#                             lon_pnt, 
#                             getAlert('success','Successfully loaded WOA temperature and sailinity data.'),
#                             locations,
#                             locations
                            
#                             ]

#     return spinner


