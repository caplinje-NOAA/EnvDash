# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023

@author: jim
"""

from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL
import dash_leaflet as dl
import plotly.express as px
import numpy as np

from . import ids
from ..dataHandling.bathretriever import retrieve, retrieveTransect, getEndCoord
from ..dataHandling.geoTools import getBoundingBox
from .custom import inputGroups as ig


## Input groups for transects
latInputStart = ig.inputGroup('Start Latitude', 'degrees N', ids.LAT_INPUT_START)
lonInputStart = ig.inputGroup('Start Longitude', 'degrees E', ids.LON_INPUT_START)
latInputEnd = ig.inputGroup('End Latitude', 'degrees N', ids.LAT_INPUT_END)
lonInputEnd = ig.inputGroup('End Longitude', 'degrees E', ids.LON_INPUT_END)
singleAzInput = ig.inputGroup('Azimuth', 'degrees rel. N', ids.AZ_INPUT)
radialInput = ig.inputGroup('Radial Step', 'degrees', ids.RADIAL_STEP_INPUT)

# Display text for transect type dropdown options
single_txt = 'Single transect with start/end coordinates'
singleAz_txt = 'Single transect with start coord and azimuth'
multiple_txt = 'mutiple radials'


# dropdown menu to select transect type
transectOptsDropdown = html.Div(
    [
        dcc.Dropdown([single_txt, singleAz_txt, multiple_txt], single_txt, 
                     id=ids.TRANSECT_DROPDOWN,
                     className ="mb-3"),
       
    ]
)


plotTransectButton = dbc.Button(
     "Plot",
     id=ids.PLOT_TRANSECTS_BUTTON_S,
     className="dropdown-button",
     color="primary",
     n_clicks=0,
 )


# inputs for single transect options
singleCoordOpts = html.Div(
    [
        dbc.Row(   [ 
                        dbc.Col(latInputStart),
                        dbc.Col(latInputEnd)
                    
                ]
            ),
        dbc.Row(   [ 
                        dbc.Col(lonInputStart),
                        dbc.Col(lonInputEnd)
                    
                ]
            ),
        plotTransectButton
    ]
) 

# inputs for single transect with azimuth options
singleCoordOpts_az = html.Div(
    [
        dbc.Row(   [ 
                        dbc.Col(latInputStart),
                        dbc.Col(singleAzInput)
                    
                ]
            ),
        dbc.Row(   [ 
                        dbc.Col(lonInputStart),
                        dbc.Col()
                        
                ]
            ),
        plotTransectButton
    ]
) 

# inputs for single transect with azimuth options
MultiTransectOpts = html.Div(
    [
        dbc.Row(   [ 
                        dbc.Col(latInputStart),
                        dbc.Col(singleAzInput)
                    
                ]
            ),
        dbc.Row(   [ 
                        dbc.Col(lonInputStart),
                        dbc.Col(radialInput)
                        
                ]
            ),
        plotTransectButton
    ]
) 

# dictionary to define transect options card content
transect_inputs_dict = {single_txt: singleCoordOpts,singleAz_txt: singleCoordOpts_az, multiple_txt:MultiTransectOpts}

# Button for toggling transect collapse
collapseButton = dbc.Button(
    "Transects",
    id=ids.TRANSECT_COLLAPSE_BUTTON,
    className="dropdown-button",
    color="primary",
    n_clicks=0,
)



transectCard = dbc.Card(
    [       html.H6('Transect type:',className="card-title"),
            transectOptsDropdown,
            html.Div(children=[singleCoordOpts],id=ids.TRANS_INPUTS_DIV),
        
          ]
    )

collapse = html.Div(
    [
        collapseButton,
        dbc.Collapse(transectCard, id=ids.TRANSECT_COLLAPSE,is_open=False),
    ]
)

BathSourceDropdown = html.Div(
    [
        dcc.Dropdown(['CRM', 'SRTM'], 'SRTM', id=ids.BATH_SOURCE_DROPDOWN),
       
    ]
)

# Parent Card For Bathymetry options
card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Bathymetry Options", className="card-title"),
                html.H6("Data Source:", className="card-title"),
                BathSourceDropdown,
                collapse,
                #dbc.Toast(html.H6(id=ids.BATH_ERROR),header="Data Status:")

            ]
        ),
    ],
    style={"width": "100%"},
)


def drawMapLayer(startLatLon, endLatLon):
    return dl.Polyline(positions=[startLatLon,endLatLon],color='red')


def buildInputDict(ids:[dict],values:[],key)->dict:
    """builds a dictionary for flexible inputs from pattern matching callbacks.
    ids are a list of dictionary component ids, values are their stored value, and key
    is the key from the id dictionary to be used in the new dictionary as the key for each 
    element"""
    inputs = {}
    for _id,value in zip(ids,values):
        inputs[_id[key]]=value
        
        
    return inputs

def retrieveFigure(bathdata:np.ndarray,transectType:str,inputs:dict)->html.Div:
            if transectType == single_txt:
                print(inputs)
                sLat, sLon = inputs['lat-start'],inputs['lon-start']
                eLat, eLon = inputs['lat-end'], inputs['lon-end']
  
            
                r,transect = retrieveTransect(bathdata, sLat, sLon, eLat, eLon)
                fig = px.line(x=r,y=transect,title=f'Transect from [{sLat:.2f},{sLon:.2f}] to [{eLat:.2f},{eLon:.2f}]')
               
       
                fig.update_layout(xaxis_title="Range (m)", yaxis_title="Depth (m)")
           
                mapLayers = drawMapLayer([sLat,sLon], [eLat,eLon])
                
            if transectType ==singleAz_txt:
                sLat, sLon = inputs['lat-start'],inputs['lon-start']
                eLat, eLon = getEndCoord(sLat,sLon,inputs['single-azimuth'],inputs['km'])
                
                r,transect = retrieveTransect(bathdata, sLat, sLon, eLat, eLon)
                fig = px.line(x=r,y=transect,title=f'Transect from [{sLat:.2f},{sLon:.2f}] to [{eLat:.2f},{eLon:.2f}]')
               
       
                fig.update_layout(xaxis_title="Range (m)", yaxis_title="Depth (m)")
               
                mapLayers = drawMapLayer([sLat,sLon], [eLat,eLon])
                
            if transectType == multiple_txt:
                sLat, sLon = inputs['lat-start'],inputs['lon-start']
                # get end coordinate arrays
                num = int(np.round(360/inputs['radial-step']))
                az = np.linspace(0,360,num=num)
           
                fig = px.line()
                mapLayers = []
                for i,azVal in enumerate(az):
                    eLat,eLon = getEndCoord(sLat,sLon,azVal,inputs['km'])
                    r,transect = retrieveTransect(bathdata, sLat, sLon, eLat, eLon)
                    fig.add_trace(px.line(x=r,y=transect).data[0])
                    mapLayers.append(drawMapLayer([sLat,sLon], [eLat,eLon]))
                    
                fig.update_layout(xaxis_title="Range (m)", yaxis_title="Depth (m)",autosize=True)
                    
                
            figure = html.Div(dcc.Graph(figure=fig,style={'width': '100%', 'height': '60vh'}, id=ids.TRANSECT_PLOT))    
            return figure,mapLayers
        

    

def render(app: Dash) -> html.Div:
    
    @app.callback(
        
        Output(ids.TRANS_MAP_LAYER, "children"),
        Output(ids.TAB_SPINNER_SECONDARY, "children"),
        
        Input(ids.PLOT_TRANSECTS_BUTTON_S, "n_clicks"),
        
        State(ids.TRANSECT_DROPDOWN, "value"),
        State({'type':ids.TRANSECT_INPUT,"parameter":ALL},'value'),
        State({'type':ids.TRANSECT_INPUT,'parameter':ALL},'id'),
        State(ids.LAT_INPUT,'value'),
        State(ids.LON_INPUT,'value'),
        State(ids.BB_KM,'value'),
        State(ids.BATH_SOURCE_DROPDOWN,'value'),
      
        )
    def plot_transects(n,transectType,parameterValues,parameterIDs,lat_pnt,lon_pnt,km,bathsource):
        if n:
            # get bath data
            BB = getBoundingBox(lat_pnt, lon_pnt, km)
            lonRange = [BB.eLon,BB.wLon]
            latRange = [BB.sLat,BB.nLat]
            print('Getting Bath Data')
            bathdata = retrieve(latRange,lonRange,DataSet=bathsource)
            
            # convert list inputs to dictionary
            inputs = buildInputDict(parameterIDs,parameterValues,'parameter')
            inputs['km']=km
            
            figure,mapLayers = retrieveFigure(bathdata, transectType, inputs)
        

            return mapLayers,figure
        return [],[]
    

    
    ## simple callback to edit which inputs show up for each dropdown choice
    ## copies starting coordinates so they carry over when new components are created
    @app.callback(
    Output(ids.TRANS_INPUTS_DIV, "children"), 
    Output(ids.LAT_INPUT_START,"value",allow_duplicate=True),
    Output(ids.LON_INPUT_START,"value",allow_duplicate=True),

    [Input(ids.TRANSECT_DROPDOWN, "value"),
     State(ids.LAT_INPUT_START,"value"),
     State(ids.LON_INPUT_START,"value")
     ],
    prevent_initial_call=True
    )
    def update_inputs(ddvalue,lat,lon):
        print('dropdown callback')

        return transect_inputs_dict[ddvalue],lat,lon
    
    
    # callback to open the collapse
    @app.callback(
    Output(ids.TRANSECT_COLLAPSE, "is_open"),
    Output(ids.LAT_INPUT_START,"value",allow_duplicate=True),
    Output(ids.LON_INPUT_START,"value",allow_duplicate=True),
      
    [Input(ids.TRANSECT_COLLAPSE_BUTTON, "n_clicks"),
     State(ids.TRANSECT_COLLAPSE, "is_open"),
     State(ids.LAT_INPUT,"value"),
     State(ids.LON_INPUT,"value")]


    )
    def toggle_collapse(n, is_open, lat, lon):
        print(f'toggle collapse {n}')
 
        if n:
           
                return (not is_open), lat, lon
         
                
        return is_open
    

    return html.Div(
        [
            card
        ]
    )
