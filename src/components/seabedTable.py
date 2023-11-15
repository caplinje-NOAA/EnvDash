# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 17:22:54 2023

@author: jim
"""

# dash imports
from dash import dcc, Dash, html, Output, Input, dash_table
import dash_bootstrap_components as dbc

# plotting imports
import dash_leaflet as dl

# project imports
from ..dataHandling.read_usSeabed import getBoundedData
from ..dataHandling.geoTools import BBfromDict
from . import ids, alerts, text



# Container for left figure / object
seabedTableDiv  =   dcc.Loading(
                    id=ids.SEABED_TAB_CONTENT,
                    children=[html.Div()],
                    type="circle",
                )





inputsStore = dcc.Store(id=ids.SEABED_INPUTS_STORE, storage_type='session',data={})



def popTable(df)->dbc.Table:
    """ actual bathymetry plot"""
    
    table =  dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    print(df)
    #table = html.Div()
    return table

# dynamic class names based on major constituent for marker colors
classNames = {'M':'marker-cluster-small-mud',
              'S':'marker-cluster-small-sand',
              'G':'marker-cluster-small-gravel',
              'Z':'marker-cluster-small-silt',
              'C':'marker-cluster-small-clay',
              '-':'marker-cluster-small'}

def buildMapLayers(df):
    """Builds Folk Code Based Markers"""
    
    # empty children container
    layerChildren = []
    for index, row in df.iterrows():
        
        markerID = row.to_dict()   
     
        coloredClassName = classNames[row["FolkCde"][-1]]
        print(coloredClassName,row["FolkCde"],row["FolkCde"][-1])
        hovertext = f'{text.folkCodes[row["FolkCde"]]}, Distance = {row["distance (m)"]/1000:.2f} km  '
        
        icon = dict(
            html=f'<div><span> {row["FolkCde"]} </span></div>',
            className=f'marker-cluster {coloredClassName}',
            iconSize=[40, 40]
        )
        # build markers, note that marker ids are dictionaries of each row
        # while tooltip ids are random uids
        marker = dl.DivMarker(position=[row['Latitude'],row['Longitude']],
                              iconOptions=icon,
                              riseOnHover=True,
                              children=[dl.Tooltip(content=hovertext,id=ids.unique())],
                              id = ids.unique()
                              )
        
        layerChildren.append(marker)
        
        
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

        # unpack inputs
        BB = BBfromDict(inputs)
        n = inputs['n']
     
        # get data 
        
        df,total = getBoundedData(BB,n)
        
        if total==0:
            alert = alerts.getAlert(alerts.warning,text.no_seabed_alert)
            return html.Div(), html.Div(), alert
            
        table = popTable(df)
        mapLayers = buildMapLayers(df)
        alert = alerts.getAlert(alerts.success,text.seabed_success)
  
     
   
        return table, mapLayers, alert
        
    return html.Div([seabedTableDiv,inputsStore])