# -*- coding: utf-8 -*-
"""
Created on Sun May  7 08:39:35 2023
The general options (top-left card) components and primary callback of the app
@author: jim
"""

# dash imports
from dash import Dash, html,State, dcc, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# plotting imports
import dash_leaflet as dl

# project imports
from . import ids,bathplot, ssplot, text
from ..dataHandling.geoTools import boundingBox, getBoundingBox


metadataStore = dcc.Store(id=ids.META_DATA_STORE, storage_type='session')

latInput = dbc.InputGroup(
            [
                dbc.InputGroupText('Center Latitude',className='input-group-label'),
                dbc.Input(type="number",id=ids.LAT_INPUT,value=41.045),
                dbc.InputGroupText('degrees N'),
            ],
            className="mb-3",
        )

lonInput = dbc.InputGroup(
            [
                dbc.InputGroupText('Center Longitude',className='input-group-label'),
                dbc.Input(type="number",id=ids.LON_INPUT,value=-70.439),
                dbc.InputGroupText('degrees E'),
            ],
            className="mb-3",
        )

boxSizeInput = dbc.InputGroup(
            [
                dbc.InputGroupText('Bounding Box Size',className='input-group-label'),
                dbc.Input(type="number",id=ids.BB_KM,value=60.,max=120.,min=10.),
                dbc.InputGroupText('Radial Kilometers'),
            ],
            className="mb-3",
        )

buttonRow = html.Div(
    [   dbc.Row(
        [     
            dbc.Col(dbc.Button("Retrieve Data", id=ids.GET_DATA_BUTTON, className="button", n_clicks=0)),
            dbc.Col(dbc.Button("Download Data", id=ids.DOWNLOAD_CANVAS_BUTTON, className="button", n_clicks=0)),
            
        ]
      )
    ]
        
)

# coniguration card to open canvas and display current configuration
card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("General Options", className="card-title"),
                latInput,
                lonInput,
                boxSizeInput,
                buttonRow
                
                ,
        
            ]
        ),
    ],
    style={"width": "100%"},
)


def buildMapLayers(BB:boundingBox):
    """Builds rectangle showing bounding box and center marker"""
    
    rectangle = dl.Rectangle(bounds=[[BB.north, BB.west], [BB.south, BB.east]],
                             fill=False,
                             id=ids.unique())
    
    marker =  dl.Marker(position=[BB.cLat,BB.cLon],                         
                        children=dl.Tooltip(f"Center, {text.coordToStr(BB.cLat,BB.cLon)}",id=ids.unique())
                        ,id=ids.unique())
    
    return [rectangle, marker]

def render(app: Dash) -> html.Div:
 
    @app.callback(
    # outputs are the two object/figure containers, any map layers, and the alert div    
    Output(ids.BATH_INPUTS_STORE,'data'),
    Output(ids.SSP_INPUTS_STORE, 'data'),
    Output(ids.SEABED_INPUTS_STORE,'data'),
    Output(ids.LAT_INPUT_START, 'value',allow_duplicate=True),
    Output(ids.LON_INPUT_START, 'value',allow_duplicate=True),
    Output(ids.BB_MAP_LAYER, "children"),

    
    [Input(ids.GET_DATA_BUTTON, "n_clicks"),
     State(ids.TABS, 'value'),
     State(ids.LAT_INPUT,'value'),
     State(ids.LON_INPUT,'value'),
     State(ids.BB_KM,'value'),
     State(ids.SSP_MONTH_DROPDOWN,'value'),
     State(ids.BATH_SOURCE_DROPDOWN,'value'),
     State(ids.STRIDE_SLIDER,'value'),
     State(ids.SEABED_SLIDER,'value'),
     State(ids.BATH_INPUTS_STORE,'data'),
     State(ids.SSP_INPUTS_STORE, 'data'),
     State(ids.SEABED_INPUTS_STORE,'data'),
     
     ],
     prevent_initial_call=True
     
    )
    def primary_app_callback(n,tab_value,lat,lon,km,month,bathsource,stride,n_seabed,bathInputs,sspInputs,seabedInputs):
        """This is the main callback of the app, being the duplicate output of all callbacks that trigger
        a data update.  Gathers all data and updates most content, also manages the BB map layers"""
        
        if n is None:
            return None
        else:
            

            # set new inputs
      
            newBathInputs = {'center':[lat,lon],'km':km,'source':bathsource,'stride':stride}
            newsspInputs = {'center':[lat,lon],'km':km,'month':month}
            newSeabedInputs = {'center':[lat,lon],'km':km,'n':n_seabed}
            
            # default all data stores to no_update
            bathOut = no_update
            sspOut = no_update
            seabedOut = no_update

            # check each tab to see if data should be updated            
            if (tab_value=='bath-tab') and (newBathInputs !=bathInputs):
                bathOut = newBathInputs
                
            if (tab_value=='ssp-tab') and (newsspInputs !=sspInputs):
                sspOut = newsspInputs
                
            if (tab_value=='seabed-tab') and (newSeabedInputs !=seabedInputs):
                seabedOut = newSeabedInputs
                
            BB = getBoundingBox(lat, lon, km)
            BBmapLayer = buildMapLayers(BB)

    
            return bathOut,sspOut,seabedOut, lat, lon, BBmapLayer
   


    return html.Div(
        [
            card,
            metadataStore
        ]
    )


## dictionary version of callback signature
# output = dict(
#             fig = Output(ids.TAB_SPINNER, 'children'),
#             outSecondaryChild = Output(ids.TAB_SPINNER_SECONDARY, "children",allow_duplicate=True),
#             mapLayer = Output(ids.MAP_LAYER, "children"),
#             alert = Output(ids.ALERT, "children")
#     )

# inputs = dict(n = Input(ids.GET_DATA_BUTTON, "n_clicks"))

# state = dict(
#         tab_value = State(ids.TABS, 'value'),
#         lat = State(ids.LAT_INPUT,'value'),
#         lon = State(ids.LON_INPUT,'value'),
#         minutes = State(ids.BB_MIN,'value'),
#         month = State(ids.SSP_MONTH_DROPDOWN,'value'),
#         bathsource = State(ids.BATH_SOURCE_DROPDOWN,'value'),
#         secondaryChild = State(ids.TAB_SPINNER_SECONDARY, "children")
#     )


## Old callback from tabs (used to be the fundamental callback)
    # @callback(
    # Output(ids.TAB_SPINNER, 'children'),
    # Output(ids.TAB_SPINNER_SECONDARY, "children",allow_duplicate=True),
    # Output(ids.MAP_LAYER, "children"),
    # Output(ids.ALERT, "children"),
    # [Input(ids.TABS, 'value'),
    # State(ids.MAP_FIG, "clickData"),
    # State(ids.BB_MIN,'value'),
    # State(ids.SSP_MONTH_DROPDOWN,'value'),
    # State(ids.BATH_SOURCE_DROPDOWN,'value'),
    # State(ids.TAB_SPINNER_SECONDARY, "children")],
    # prevent_initial_call=True
    # )
    # def update_tabs(value,clickData,minutes,month,bathsource,secondaryChild):
    #     """This is the primary callback.  When tab value is triggered, gather all inputs, retrieve appropriate data, 
    #     and update figures"""
    #     lat = clickData['latlng']['lat']
    #     lng = clickData['latlng']['lng']
    #     click_lat_lng = [lat,lng]
        
    #     # secondary child div contains transects for the bath tab
    #     # passing the child through this callback allows it to remain
    #     # 
    #     if value == 'bath-tab':
    #         outSecondaryChild = secondaryChild
    #     else:
    #         outSecondaryChild = []
            
    #     fig, mapLayer, alert = renderer[value].render(click_lat_lng,minutes,month,bathsource)


    #     return fig, outSecondaryChild, mapLayer, alert