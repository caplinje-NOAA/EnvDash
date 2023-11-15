# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 17:11:07 2023

@author: jim
"""

# dash imports
from dash import Dash, dcc, html,State, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# project imports
from . import ids, text

# number of observations slider
obsSlider =     dcc.Slider(5, 50, 5,
               value=10,
               id=ids.SEABED_SLIDER
    )


card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Seabed Options", className="card-title"),
                html.H6("Maximum number of observations:", className="card-title"),
                obsSlider,
                html.H6(text.folkCodeKey, className="card-title"),
                               
        
            ]
        ),
    ],
    style={"width": "100%"},
)





def render(app: Dash) -> html.Div:
    # callback for changes to number of points on slider
    # triggers a data update and chains to primary callback in gen opts
    @callback(
        Output(ids.GET_DATA_BUTTON, "n_clicks",allow_duplicate=True), 
        
        [Input(ids.SEABED_SLIDER,'value'),
        State(ids.GET_DATA_BUTTON, "n_clicks")],
        prevent_initial_call=True
        )
    def update_number(value,n):

                
        return n+1

    return html.Div(
        [
            card
        ]
    )