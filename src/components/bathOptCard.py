# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023
Bathymetry options card component, also manages transect plotting
@author: jim
"""
# dash imports
from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL

# project imports
from . import ids, text
from .transectPlot import plotTransects
from ..dataHandling.bathretriever import retrieve
from ..dataHandling.geoTools import getBoundingBox
from .custom import inputGroups as ig

# set to 10 for debugging
strideDefaults = {'CRM':10,'SRTM':10}
#### Build Components of card
## Input groups for transects
latInputStart = ig.inputGroup('Start Latitude', 'degrees N', ids.LAT_INPUT_START)
lonInputStart = ig.inputGroup('Start Longitude', 'degrees E', ids.LON_INPUT_START)
latInputEnd = ig.inputGroup('End Latitude', 'degrees N', ids.LAT_INPUT_END)
lonInputEnd = ig.inputGroup('End Longitude', 'degrees E', ids.LON_INPUT_END)
singleAzInput = ig.inputGroup('Azimuth', 'degrees rel. N', ids.AZ_INPUT)
radialInput = ig.inputGroup('Radial Step', 'degrees', ids.RADIAL_STEP_INPUT)


# Stride slider
strideSlider =     dcc.Slider(1,10,1,
               value=1,
               id=ids.STRIDE_SLIDER
    )


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
                        dbc.Col(radialInput)
                    
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

# dictionary to define transect options card content
transect_inputs_dict = {text.transect_single: singleCoordOpts,text.transect_singleAz: singleCoordOpts_az, text.transect_multiple:MultiTransectOpts}

# Button for toggling transect collapse
collapseButton = dbc.Button(
    "Transects",
    id=ids.TRANSECT_COLLAPSE_BUTTON,
    className="button",
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
                dbc.Row([
                    dbc.Col(html.H6("Data Source:", className="card-title")),
                    dbc.Col(html.H6("Stride (Controls resolution, higher stride = lower resolution, but faster plotting):", className="card-title")),
                    ]),
                dbc.Row([
                    dbc.Col(BathSourceDropdown),
                    dbc.Col(strideSlider),
                            ]),
                collapse,
                #dbc.Toast(html.H6(id=ids.BATH_ERROR),header="Data Status:")

            ]
        ),
    ],
    style={"width": "100%"},
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
            print(BB)
 
            print('Getting Bath Data')
            bathdata = retrieve(BB,DataSet=bathsource,downCast=False)
            
            # convert list inputs to dictionary, high coupling warning here
            inputs = buildInputDict(parameterIDs,parameterValues,'parameter')
            inputs['km']=km
            
            figure,mapLayers = plotTransects(bathdata, transectType, inputs)
        

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
      
 
        if n:
           
                return (not is_open), lat, lon
         
                
        return is_open
    
    # Callback which enables default stride values on bath dataset change
    @app.callback(
    Output(ids.STRIDE_SLIDER, "value"),      
    Input(ids.BATH_SOURCE_DROPDOWN, "value"),
    )
    def update_stride(value):

        return strideDefaults[value]
    

    return html.Div(
        [
            card
        ]
    )
