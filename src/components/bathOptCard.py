# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023

@author: jim
"""

from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_leaflet as dl
import plotly.express as px

from . import ids
from ..dataHandling.bathretriever import retrieve, retrieveTransect, getEndCoord
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

plotTransectButtonS = dbc.Button(
     "Plot",
     id=ids.PLOT_TRANSECTS_BUTTON_S,
     className="dropdown-button",
     color="primary",
     n_clicks=0,
 )

plotTransectButtonS_AZ = dbc.Button(
     "Plot",
     id=ids.PLOT_TRANSECTS_BUTTON_S_AZ,
     className="dropdown-button",
     color="primary",
     n_clicks=0,
 )

plotTransectButtonM = dbc.Button(
     "Plot",
     id=ids.PLOT_TRANSECTS_BUTTON_M,
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
        plotTransectButtonS
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
        plotTransectButtonS_AZ
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
                        dbc.Col()
                        
                ]
            ),
        plotTransectButtonM
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



def render(app: Dash) -> html.Div:
    
    @app.callback(
        
        Output(ids.TRANS_MAP_LAYER, "children",allow_duplicate=True),
        Output(ids.TAB_SPINNER_SECONDARY, "children",allow_duplicate=True),
        Input(ids.PLOT_TRANSECTS_BUTTON_S, "n_clicks"),
        State(ids.LAT_INPUT_START,'value'),
        State(ids.LON_INPUT_START,'value'),
        State(ids.LAT_INPUT_END,'value'),
        State(ids.LON_INPUT_END,'value'),
        State(ids.MAP_FIG, "click_lat_lng"),
        State(ids.BB_MIN,'value'),
        State(ids.BATH_SOURCE_DROPDOWN,'value'),
       
        prevent_initial_call=True
        )
    def plot_transects1(n,sLat,sLon,eLat,eLon,click_lat_lng,minutes,bathsource):
        if n:
            lat_pnt = click_lat_lng[0]
            lon_pnt = click_lat_lng[1]
            minutes = minutes/2
            bathdata = retrieve(lat_pnt,lon_pnt,centerOffset_minutes=minutes,DataSet=bathsource)
            
            r,transect = retrieveTransect(bathdata, sLat, sLon, eLat, eLon)
            fig = px.line(x=r,y=transect,title=f'Transect from [{sLat:.2f},{sLon:.2f}] to [{eLat:.2f},{eLon:.2f}]')
           
   
            fig.update_layout(xaxis_title="Range (m)", yaxis_title="Depth (m)")
            figure = html.Div(dcc.Graph(figure=fig,style={'width': '100%', 'height': '60vh'}, id=ids.TRANSECT_PLOT))         

            return drawMapLayer([sLat,sLon], [eLat,eLon]),figure
        return [],[]
    
    @app.callback(
        
        Output(ids.TRANS_MAP_LAYER, "children",allow_duplicate=True),
        Output(ids.TAB_SPINNER_SECONDARY, "children",allow_duplicate=True),
        Input(ids.PLOT_TRANSECTS_BUTTON_S_AZ, "n_clicks"),
        State(ids.LAT_INPUT_START,'value'),
        State(ids.LON_INPUT_START,'value'),
        State(ids.AZ_INPUT,'value'),
        State(ids.MAP_FIG, "click_lat_lng"),
        State(ids.BB_MIN,'value'),
        State(ids.BATH_SOURCE_DROPDOWN,'value'),
        
        prevent_initial_call=True
        )
    def plot_transects2(n,sLat,sLon,az,click_lat_lng,minutes,bathsource):
        if n:
            lat_pnt = click_lat_lng[0]
            lon_pnt = click_lat_lng[1]
            minutes = minutes/2
            bathdata = retrieve(lat_pnt,lon_pnt,centerOffset_minutes=minutes,DataSet=bathsource)
   
            
            eLat, eLon = getEndCoord(sLat,sLon,az,minutes)
            r,transect = retrieveTransect(bathdata, sLat, sLon, eLat, eLon)
            fig = px.line(x=r,y=transect,title=f'Transect from [{sLat:.2f},{sLon:.2f}] projected to az={az:.2f} deg. rel N')
            fig.update_layout(xaxis_title="Range (m)", yaxis_title="Depth (m)")
            figure = html.Div(dcc.Graph(figure=fig,style={'width': '100%', 'height': '60vh'}, id=ids.TRANSECT_PLOT))         

            return drawMapLayer([sLat,sLon], [eLat,eLon]),figure
        return [],[]
    
    
    @app.callback(
    Output(ids.TRANS_INPUTS_DIV, "children"), 

    [Input(ids.TRANSECT_DROPDOWN, "value"),
     ],
    prevent_initial_call=True
    )
    def update_inputs(ddvalue):
        print('dropdown callback')

        return transect_inputs_dict[ddvalue]
    
    

    @app.callback(
    Output(ids.TRANSECT_COLLAPSE, "is_open"),
      
    [Input(ids.TRANSECT_COLLAPSE_BUTTON, "n_clicks"),
     State(ids.TRANSECT_COLLAPSE, "is_open")]


    )
    def toggle_collapse(n, is_open):
        print(f'toggle collapse {n}')
 
        if n:
           
                return (not is_open)
         
                
        return is_open
    

    return html.Div(
        [
            card
        ]
    )
