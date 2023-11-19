# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023
Bathymetry options card component, also manages transect plotting
@author: jim
"""
# dash imports
from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# project imports
from . import ids,transectOptCard 


# set to 10 for debugging
strideDefaults = {'CRM':10,'SRTM':10}
#### Build Components of card



# Stride slider
strideSlider =     dcc.Slider(1,10,1,
               value=1,

               id=ids.STRIDE_SLIDER
    )

# 


# Button for toggling transect collapse
collapseButton = dbc.Button(
    "Transects",
    id=ids.TRANSECT_COLLAPSE_BUTTON,
    className="button",
    color="primary",
    n_clicks=0,
)




BathSourceDropdown = html.Div(
    [
        dcc.Dropdown(['CRM', 'SRTM'], 'SRTM', id=ids.BATH_SOURCE_DROPDOWN),
       
    ]
)







def render(app: Dash) -> html.Div:
   
    
    # callback to open the collapse
    @app.callback(
    Output(ids.TRANSECT_COLLAPSE, "is_open"),
      
    Input(ids.TRANSECT_COLLAPSE_BUTTON, "n_clicks"),
    State(ids.TRANSECT_COLLAPSE, "is_open")
    )
    def toggle_collapse(n, is_open):
      
 
        if n:
           
                return (not is_open)
         
                
        return is_open
    
    # Callback which enables default stride values on bath dataset change
    @app.callback(
    Output(ids.STRIDE_SLIDER, "value"),      
    Input(ids.BATH_SOURCE_DROPDOWN, "value"),
    )
    def update_stride(value):

        return strideDefaults[value]
    

    return dbc.Card(
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
                    html.Div(
                        [
                            collapseButton,
                            dbc.Collapse(transectOptCard.render(app), id=ids.TRANSECT_COLLAPSE,is_open=False),
                        ]
                    ),
     

                ]
            ),
        ],
        style={"width": "100%"},
    )
