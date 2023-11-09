# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023

@author: jim
"""

from dash import Dash, dcc, html,State, ALL,callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


from . import ids


# latInput = dbc.InputGroup(
#             [
#                 dbc.InputGroupText('Center Latitude',className='input-group-label'),
#                 dbc.Input(type="number",id=ids.LAT_INPUT),
#                 dbc.InputGroupText('degrees N'),
#             ],
#             className="mb-3",
#         )



monthDropdown = html.Div(
    [
        dcc.Dropdown(['January','February','March','April','May','June','July','August','September','October','November','December'], 'January', id=ids.SSP_MONTH_DROPDOWN),
       
    ]
)

# includeDropdown = html.Div(
#     [
#         dcc.Dropdown(['none'], 'none', id=ids.SSP_EXCLUDE_DROPDOWN, multi=True),
       
#     ]
# )
# coniguration card to open canvas and display current configuration
card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Sound Speed Profile Options", className="card-title"),
                html.H6("Month:", className="card-title"),
                monthDropdown,
                html.H6("Excluded Points:", className="card-title"),
                #includeDropdown
                #dbc.Toast(html.H6(id=ids.BATH_ERROR),header="Data Status:")

                
                
        
            ]
        ),
    ],
    style={"width": "100%"},
)





def render(app: Dash) -> html.Div:
    
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
