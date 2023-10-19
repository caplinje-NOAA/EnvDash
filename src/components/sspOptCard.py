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

includeDropdown = html.Div(
    [
        dcc.Dropdown(['none'], 'none', id=ids.SSP_EXCLUDE_DROPDOWN, multi=True),
       
    ]
)
# coniguration card to open canvas and display current configuration
card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Sound Speed Profile Options", className="card-title"),
                html.H6("Month:", className="card-title"),
                monthDropdown,
                html.H6("Excluded Points:", className="card-title"),
                includeDropdown
                #dbc.Toast(html.H6(id=ids.BATH_ERROR),header="Data Status:")

                
                
        
            ]
        ),
    ],
    style={"width": "100%"},
)





def render(app: Dash) -> html.Div:
    
    # @callback(
    #     Output({'type':ids.WOA_DATA_MARKER,"location":ALL},'color'),
        
    #     [Input(ids.SSP_INCLUDE_DROPDOWN,'value'),
    #      State({'type':ids.WOA_DATA_MARKER,"location":ALL},'id')
    #      ]
    #     )
    # def showIncludedMarkerse(included,markerIds):
    #     colors = []
    #     for markerID in markerIds:
    #         if markerID['location'] in included:
    #             colors.append('blue')
    #         else:
    #             colors.append('red')
                
    #     return colors

    return html.Div(
        [
            card
        ]
    )
