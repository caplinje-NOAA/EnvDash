# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:53:59 2023

@author: jim
"""

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from ..dataHandling.bathretriever import retrieve
from . import ids, alerts
import time




def render(click_lat_lng,minutes,month,bathsource):

    lat_pnt = click_lat_lng[0]
    lon_pnt = click_lat_lng[1]
    minutes = minutes/2
    lonRange = [lon_pnt-minutes/60,lon_pnt+minutes/60]
    latRange = [lat_pnt-minutes/60,lat_pnt+minutes/60]
    bathdata = retrieve(lat_pnt,lon_pnt,centerOffset_minutes=minutes,DataSet=bathsource)
    mapLayers = [dl.Rectangle(bounds=[[latRange[1], lonRange[1]], [latRange[0], lonRange[0]]],children=dl.Tooltip("Bounding box for bathymetry")),
                 dl.Marker(position=click_lat_lng, children=dl.Tooltip("(Center, {:.3f}, {:.3f})".format(*click_lat_lng)))]
    
    if bathdata.error:
        figure = None
        alert = alerts.getAlert('danger',bathdata.error)
        return figure, mapLayers, alert

    else:
        alert = alerts.getAlert('success',f'Successfully loaded bathymetry data from {bathsource}.')
        fig = go.Figure(data =
            go.Contour(
                z=bathdata.topo,
                x=bathdata.lon, # horizontal axis
                y=bathdata.lat,# vertical axis
                colorbar=dict(
            title='Depth (m)', # title here
            titleside='right')
            ))
        fig.update_layout(title=f'{bathsource} bathymetry Contour near [{click_lat_lng[0]:.3f},{click_lat_lng[1]:.3f}]',
                   xaxis_title='Longitude (degrees E)',
                   yaxis_title='Latitude (degrees N)',yaxis = dict(scaleanchor = 'x'),xaxis = dict(scaleanchor = 'y'))
        
        figure = dcc.Graph(figure=fig,style={'width': '60vh', 'height': '60vh'},id=ids.BATH_PLOT)
        
        return figure, mapLayers, alert
    


# def render(app: Dash) -> html.Div:

#     @app.callback(
#         Output(ids.BATH_SPINNER, "children"),
#         Output(ids.BATH_ALERT_DIV,"children"),
#         [
#             Input(ids.MAP_FIG, "click_lat_lng"),
#             State(ids.BB_MIN,'value'),
#             State(ids.BATH_SOURCE_DROPDOWN,'value'),
#         ],
#     )
#     def update_chart(click_lat_lng,minutes,bathsource) -> html.Div:
#         time.sleep(0.001)
#         lat_pnt = click_lat_lng[0]
#         lon_pnt = click_lat_lng[1]
#         bathdata = retrieve(lat_pnt,lon_pnt,centerOffset_mintues=minutes/2,DataSet=bathsource)
#         if bathdata.error:
#             return None, getAlert('danger',bathdata.error)

#         else:
#             fig = go.Figure(data =
#                 go.Contour(
#                     z=bathdata.topo,
#                     x=bathdata.lon, # horizontal axis
#                     y=bathdata.lat# vertical axis
#                 ))
#             fig.update_layout(title=f'Bathymetry Contour near {str(click_lat_lng)}',
#                        xaxis_title='Longitude',
#                        yaxis_title='Latitude',yaxis = dict(scaleanchor = 'x'),xaxis = dict(scaleanchor = 'y'))
    
#             return dcc.Graph(figure=fig,style={'width': '60vh', 'height': '60vh'},id=ids.BATH_PLOT),getAlert('success',f'Successfully loaded bathymetry data from {bathsource}.')

#     return spinner