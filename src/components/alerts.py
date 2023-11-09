# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023

@author: jim
"""

from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


from . import ids


def getAlert(color,message):
    return html.Div(
        [
           
            dbc.Alert(
                message,
                
                is_open=True,
                duration=4000,
                color=color
            ),
        ]
    )


def render(app: Dash) -> html.Div:


    return html.Div(id=ids.ALERT)