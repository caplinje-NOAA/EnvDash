# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023
Transect options card (nested in bath options)
Controls transect plotting and options
@author: jim
"""
# dash imports
from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL

# data science imports
import numpy as np

# project imports
from . import ids, text
from .transectPlot import plotTransects
from ..dataHandling.bathretriever import retrieve, bathdata
from ..dataHandling.geoTools import getBoundingBox
from .custom import inputGroups as ig

#performance related settings
# pulls transects from figure rather than a new ERDDAP request
# IF it is decided this should be false forever, the bath figure input
# should be removed from the plot transect callback
useBathFigureData = True

# inputs store
transInputsStore = dcc.Store(ids.TRANSECT_INPUTS_STORE, storage_type = 'memory',data={})

## build all of the input groups
latInputEnd = ig.inputGroup('End Latitude', 'degrees N', ids.LAT_INPUT_END)
lonInputEnd = ig.inputGroup('End Longitude', 'degrees E', ids.LON_INPUT_END)
singleAzInput = ig.inputGroup('Azimuth', 'degrees rel. N', ids.AZ_INPUT)
radialInput = ig.inputGroup('Radial Step', 'degrees', ids.RADIAL_STEP_INPUT)


# dropdown menu to select transect type
transectOptsDropdown = html.Div(
    [
        dcc.Dropdown([text.transect_single, text.transect_singleAz, text.transect_multiple], text.transect_single, 
                     id=ids.TRANSECT_DROPDOWN,
                     className ="mb-3",
                     clearable = False,
                     searchable = False,
                     ),
       
    ]
)


plotTransectButton = dbc.Button(
     "Plot",
     id=ids.PLOT_TRANSECTS_BUTTON_S,
     className="button",
     color="primary",
     n_clicks=0,
 )


## define the inputs table based on dropdown option
# inputs for single transect options
singleCoordOpts = html.Div(
    [
        dbc.Row(   [ 
                        dbc.Col(latInputEnd),
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
                        dbc.Col(singleAzInput)                   
                ]
            ),

        plotTransectButton
    ]
) 

# inputs for single transect with azimuth options
MultiTransectOpts = html.Div(
    [
        dbc.Row(   [ 
                        dbc.Col(radialInput)                  
                ]
            ),

        plotTransectButton
    ]
) 

# dictionary to define transect options card content
transect_inputs_dict = {text.transect_single: singleCoordOpts,text.transect_singleAz: singleCoordOpts_az, text.transect_multiple:MultiTransectOpts}

# build initial card
transectCard = dbc.Card(
    [       html.H6('Transect type:',className="card-title"),
            transectOptsDropdown,
            html.Div(children=[singleCoordOpts],id=ids.TRANS_INPUTS_DIV),
            transInputsStore,
        
          ]
    )


#### Callbacks of above components
# !!coupling warning: modifying input dictionary may break transectPlot module
def buildInputDict(ids:[dict],values:[],key)->dict:
    """builds a dictionary for flexible inputs from pattern matching callbacks.
    ids are a list of dictionary component ids, values are their stored value, and key
    is the key from the id dictionary to be used in the new dictionary as the key for each 
    element"""
    inputs = {}
    for _id,value in zip(ids,values):
        inputs[_id[key]]=value
        
        
    return inputs

def render(app: Dash) -> html.Div:
    ## Plot transect callback
    @app.callback(
        
        Output(ids.TRANS_MAP_LAYER, "children"),
        Output(ids.TRANSECT_CONTENT, "children"),
        Output(ids.TRANSECT_INPUTS_STORE,'data'),
        
        Input(ids.PLOT_TRANSECTS_BUTTON_S, "n_clicks"),
        
        State(ids.TRANSECT_DROPDOWN, "value"),
        State({'type':ids.TRANSECT_INPUT,"parameter":ALL},'value'),
        State({'type':ids.TRANSECT_INPUT,'parameter':ALL},'id'),
        State(ids.LAT_INPUT,'value'),
        State(ids.LON_INPUT,'value'),
        State(ids.BB_KM,'value'),
        State(ids.BATH_SOURCE_DROPDOWN,'value'),
        State(ids.BATH_PLOT, 'figure')
      
        )
    def plot_transects(n,transectType,parameterValues,parameterIDs,lat_pnt,lon_pnt,km,bathsource,bathfig):
        if n:
            print(bathfig['data'][0]['x'])
            # get bath data
            BB = getBoundingBox(lat_pnt, lon_pnt, km)
            print(BB)
 
            if useBathFigureData:
                data = bathdata(lat=np.array(bathfig['data'][0]['y']),
                                lon = np.array(bathfig['data'][0]['x']),
                                topo= np.array(bathfig['data'][0]['z']),
                                error = None)
            else:
                data = retrieve(BB,DataSet=bathsource,downCast=False)
            
            # convert list inputs to dictionary, high coupling warning here
            print('building inputs')
            inputs = buildInputDict(parameterIDs,parameterValues,'parameter')
            inputs['km']=km
            inputs['transectType'] = transectType
            inputs['lat-start'] = BB.cLat
            inputs['lon-start'] = BB.cLon
            print('requesting figures')
            figure,mapLayers = plotTransects(data, transectType, inputs)
        

            return mapLayers, figure, inputs
        return html.Div(),html.Div(),{}
    
    ## simple callback to edit which inputs show up for each dropdown choice
    ## copies starting coordinates so they carry over when new components are created
    @app.callback(
    Output(ids.TRANS_INPUTS_DIV, "children"), 


    [Input(ids.TRANSECT_DROPDOWN, "value"),

     ],
    prevent_initial_call=True
    )
    def update_inputs(ddvalue):
     
        return transect_inputs_dict[ddvalue]
    
    return transectCard

