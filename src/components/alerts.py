# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 14:38:11 2023
Model for alert components
@author: jim
"""

# dash imports

from dash import Dash, html
import dash_bootstrap_components as dbc



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