# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023
Sound Speed profile options card
@author: jim
"""

# dash imports
from dash import Dash, dcc, html,State, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# project imports
from . import ids




monthDropdown = html.Div(
    [
        dcc.Dropdown(['January','February','March','April','May','June','July','August','September','October','November','December'], 'January', id=ids.SSP_MONTH_DROPDOWN),
       
    ]
)


card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Sound Speed Profile Options", className="card-title"),
                html.H6("Month:", className="card-title"),
                monthDropdown,
                html.H6("Excluded Points:", className="card-title"),
                               
        
            ]
        ),
    ],
    style={"width": "100%"},
)





def render(app: Dash) -> html.Div:
    # callback for changes to the month dropdown
    # changing the month triggers a data update and chains to primary callback in gen opts
    @callback(
        Output(ids.GET_DATA_BUTTON, "n_clicks",allow_duplicate=True), 
        
        [Input(ids.SSP_MONTH_DROPDOWN,'value'),
        State(ids.GET_DATA_BUTTON, "n_clicks")],
        prevent_initial_call=True
        )
    def update_month(value,n):

                
        return n+1

    return html.Div(
        [
            card
        ]
    )
