# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:53:59 2023
This module handles rendering of bathymetry and related map layers
@author: jim
"""

# dash imports
from dash import dcc, Dash, html, Output, State, Input
import dash_bootstrap_components as dbc
# plotting imports
import plotly.graph_objects as go
import dash_leaflet as dl

# project imports
from ..dataHandling.bathretriever import retrieve
from ..dataHandling.geoTools import boundingBox, BBfromDict
from . import ids, alerts



dataDowncast = {'SRTM':False,'CRM':False}

# Container for left figure / object
bathDiv  =        dcc.Loading(
                    id=ids.BATH_TAB_CONTENT,
                    children=[html.Div(dcc.Graph(figure=go.Figure(),style={'width': '60vh', 'height': '60vh'},id=ids.BATH_PLOT))],
                    type="circle",
                )

# Container for right figure / object (e.g. transects)
transectDiv =        dcc.Loading(
                    id=ids.TRANSECT_CONTENT,
                    children=[html.Div()],
                    type="circle",
                )

# container for all figures (bottom section of tabs, width sets ratio (out of 12))
bathContent = dbc.Row([dbc.Col(bathDiv,width='auto'),
                      dbc.Col(transectDiv)],style={'flex-wrap': 'nowrap'}) # no wrap fixed the overflow issues with wide transect figures

inputsStore = dcc.Store(id=ids.BATH_INPUTS_STORE, storage_type='memory',data={})

def buildFigure(bathdata,BB:boundingBox,source:str)->dcc.Graph:
    """ actual bathymetry plot"""
    fig = go.Figure(data =
        go.Contour(
            z=bathdata.topo,
            x=bathdata.lon, # horizontal axis
            y=bathdata.lat,# vertical axis
            colorbar=dict(
        title='Depth (m)', # title here
              #        titleside='right'
            ),
            
        ))
    fig.update_layout(title=f'{source} bathymetry Contour near [{BB.cLat:.3f},{BB.cLon:.3f}]',
               xaxis_title='Longitude (degrees E)',
               yaxis_title='Latitude (degrees N)',
               autosize=True,
               margin=dict(b=200, t=50, l=50, r=50),
             
               #width = 500,
               #height = 500)
               )
    
    #figure = dcc.Graph(figure=fig,style={'width': '60vh', 'height': '60vh'},id=ids.BATH_PLOT)
    return fig


    
def render(app: Dash) -> html.Div:
    @app.callback(
    # outputs only the bath figure and alert  
    Output(ids.BATH_PLOT, 'figure'),
    Output(ids.ALERT, "children", allow_duplicate=True), 
    
    [Input(ids.BATH_INPUTS_STORE, "data"),   
     ],
     prevent_initial_call=True
     
    )
    def updatePlot(inputs):
        # unpack inputs
        bathsource = inputs['source']
        BB = BBfromDict(inputs)

        
        # get data 
        bathdata = retrieve(BB,DataSet=bathsource, stride = inputs['stride'], downCast=dataDowncast[bathsource])
        print(bathdata.error)
        
      
        # handle request errors
        if bathdata.error:
            figure = go.Figure()
            alert = alerts.getAlert('danger',bathdata.error)
            return figure, alert
    
        else:
            
            # return rendered objects
            alert = alerts.getAlert('success',f'Successfully loaded bathymetry data from {bathsource}.')
       
            figure = buildFigure(bathdata,BB,bathsource)
        
            return figure, alert
        
    return html.Div([bathContent,inputsStore])
    

