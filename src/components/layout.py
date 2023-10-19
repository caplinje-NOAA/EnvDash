from dash import Dash, html
import dash_bootstrap_components as dbc
#from . import card_dropdown
from . import map_fig, bathplot, ssplot, genOptCard, bathOptCard,ids,sspOptCard,alerts,tabs

#dropdown1 = card_dropdown.dropDown('1','Card 1')
#dropdown2 = card_dropdown.dropDown('2','Card 2')

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
  
            html.Div([dbc.Row([
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col(html.Div(genOptCard.render(app),className="app-div"))
                                    ]),                                          
                                dbc.Row([                                    
                                    dbc.Col(html.Div(map_fig.render(app),className="app-div"))
                                    ]),
                            
                                
                                ],width=5),

                            dbc.Col(tabs.render(app))
                            ]),
           
                        html.Div(alerts.render(app)),
                        
                        ])
            
            
                           

  

        ],
    )
