from dash import Dash, html
import dash_bootstrap_components as dbc
#from . import card_dropdown
from . import map_fig, bathplot, ssplot, genOptCard, bathOptCard,ids,sspOptCard,alerts,tabs



def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
  
            html.Div([dbc.Row([
                            # Left hand side
                            dbc.Col([
                                # Options Row
                                dbc.Row([
                                    
                                    dbc.Col(html.Div(genOptCard.render(app),className="app-div"))
                                    ]),  
                                # Map Row                                        
                                dbc.Row([                                    
                                    dbc.Col(html.Div(map_fig.render(app),className="app-div"))
                                    ]),
                            
                                
                                ],width=4),
                            # tab column    
                            dbc.Col(tabs.render(app))
                            ],style={'flex-wrap': 'nowrap'}),  # nowrap prevents overflow caused by large-width figures
           
                        html.Div(alerts.render(app)),
                        
                        ])
            
            
                           

  

        ],
    )
