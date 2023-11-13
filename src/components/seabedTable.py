# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 17:22:54 2023

@author: jim
"""

# dash imports
from dash import dcc, Dash, html, Output, State, Input, dash_table
import dash_bootstrap_components as dbc

# plotting imports
import plotly.graph_objects as go
import dash_leaflet as dl

# project imports
from ..dataHandling.read_usSeabed import getBoundedData
from ..dataHandling.geoTools import getBoundingBox, boundingBox
from . import ids, alerts



# Container for left figure / object
seabedTableDiv  =   dcc.Loading(
                    id=ids.SEABED_TAB_CONTENT,
                    children=[html.Div()],
                    type="circle",
                )





inputsStore = dcc.Store(id=ids.SEABED_INPUTS_STORE, storage_type='session',data={})

def divMarker(lat:float,lon:float,text:str,hovertext):
        icon = dict(
        html=f'<div><span> {text} </span></div>',
        className='marker-cluster marker-cluster-small',
        iconSize=[40, 40]
    )
        marker = dl.DivMarker(position=[lat,lon], iconOptions=icon, riseOnHover=True,children=[dl.Tooltip(content=hovertext)])
        return marker

def popTable(df)->dbc.Table:
    """ actual bathymetry plot"""
    
    table =  dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    print(df)
    #table = html.Div()
    return table

def buildMapLayers(df):
    """Builds Folk Code Based Markers"""
    
    layerChildren = []
    for index, row in df.iterrows():
        gravel,sand,mud,clay = row['Gravel'],row['Sand'],row['Mud'],row['Clay']
        
        title = f'({gravel}% G, {sand}% S, {mud}% M, {clay}% clay), Distance = {row["distance (m)"]/1000:.2f} km  '
        layerChildren.append(divMarker(row['Latitude'],row['Longitude'],row['FolkCde'],title))
    return layerChildren
    
def render(app: Dash) -> html.Div:
    @app.callback(
     # outputs are the two object/figure containers, any map layers, and the alert div    
      Output(ids.SEABED_TAB_CONTENT, 'children'),
      Output(ids.SEABED_MAP_LAYER, "children"),
      Output(ids.ALERT, "children", allow_duplicate=True), 
     
      [Input(ids.SEABED_INPUTS_STORE, "data"),   
       ],
       prevent_initial_call=True
      
      )
    def updateTable(inputs):
        #coord_lat_lon,km,month,bathsource,prevMetaData
        #metaData= {'center':coord_lat_lon,'km':km,'source':bathsource}
        coord_lat_lon = inputs['center']
        km = inputs['km']
        n = inputs['n']
     
        """Bath plot renderer"""
        # calculate bounding box
        BB = getBoundingBox(coord_lat_lon[0], coord_lat_lon[1], km)
       
        # get data 
        
        df,total = getBoundedData(BB,n)
        #print(type(df))
        table = popTable(df)

       
        mapLayers = buildMapLayers(df)
     
       
           
        # return rendered objects
        alert = alerts.getAlert('success',f'Successfully loaded seabed data.')
  
     
   
        return table, mapLayers, alert
        
    return html.Div([seabedTableDiv,inputsStore])