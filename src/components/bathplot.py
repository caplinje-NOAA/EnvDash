# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:53:59 2023
This module handles rendering of bathymetry and related map layers
@author: jim
"""

# dash imports
from dash import dcc

# plotting imports
import plotly.graph_objects as go
import dash_leaflet as dl

# project imports
from ..dataHandling.bathretriever import retrieve
from ..dataHandling.geoTools import getBoundingBox, boundingBox
from . import ids, alerts



def buildFigure(bathdata,BB:boundingBox,source:str)->dcc.Graph:
    """ actual bathymetry plot"""
    fig = go.Figure(data =
        go.Contour(
            z=bathdata.topo,
            x=bathdata.lon, # horizontal axis
            y=bathdata.lat,# vertical axis
            colorbar=dict(
        title='Depth (m)', # title here
        titleside='right')
        ))
    fig.update_layout(title=f'{source} bathymetry Contour near [{BB.cLat:.3f},{BB.cLon:.3f}]',
               xaxis_title='Longitude (degrees E)',
               yaxis_title='Latitude (degrees N)',
               autosize=True,
               margin=dict(b=200, t=50, l=50, r=50),
             
               #width = 500,
               #height = 500)
               )
    
    figure = dcc.Graph(figure=fig,style={'width': '60vh', 'height': '60vh'},id=ids.BATH_PLOT)
    return figure

def buildMapLayers(BB:boundingBox):
    """Builds rectangle showing bounding box and center marker"""
    mapLayers = [dl.Rectangle(bounds=[[BB.north, BB.west], [BB.south, BB.east]],children=dl.Tooltip("Bounding box for bathymetry")),
                 dl.Marker(position=[BB.cLat,BB.cLon], children=dl.Tooltip(f"Center, [{BB.cLat:.3f}, {BB.cLon:.3f}]"))]
    return mapLayers
    

def render(coord_lat_lon,km,month,bathsource):
    """Bath plot renderer"""
    # calculate bounding box
    BB = getBoundingBox(coord_lat_lon[0], coord_lat_lon[1], km)
    
    # get data 
    bathdata = retrieve(BB,DataSet=bathsource)
    print(bathdata.error)
    
    mapLayers = buildMapLayers(BB)
    
    # handle request errors
    if bathdata.error:
        figure = None
        alert = alerts.getAlert('danger',bathdata.error)
        return figure, mapLayers, alert

    else:
        
        # return rendered objects
        alert = alerts.getAlert('success',f'Successfully loaded bathymetry data from {bathsource}.')
        
        figure = buildFigure(bathdata,BB,bathsource)
        
        return figure, mapLayers, alert
    

