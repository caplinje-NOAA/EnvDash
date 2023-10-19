
from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


from . import ids


latInput = dbc.InputGroup(
            [
                dbc.InputGroupText('Center Latitude',className='input-group-label'),
                dbc.Input(type="number",id=ids.LAT_INPUT),
                dbc.InputGroupText('degrees N'),
            ],
            className="mb-3",
        )

lonInput = dbc.InputGroup(
            [
                dbc.InputGroupText('Center Longitude',className='input-group-label'),
                dbc.Input(type="number",id=ids.LON_INPUT),
                dbc.InputGroupText('degrees E'),
            ],
            className="mb-3",
        )

minInput = dbc.InputGroup(
            [
                dbc.InputGroupText('Bounding Box Size',className='input-group-label'),
                dbc.Input(type="number",id=ids.BB_MIN,value=60.,max=120.,min=10.),
                dbc.InputGroupText('minutes'),
            ],
            className="mb-3",
        )

button = html.Div(
    [
        dbc.Button(
            "Retrieve Data", id=ids.GET_DATA_BUTTON, className="me-2", n_clicks=0
        ),
       
    ]
)

# coniguration card to open canvas and display current configuration
card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("General Options", className="card-title"),
                latInput,
                lonInput,
                minInput,
                button
                
                ,
        
            ]
        ),
    ],
    style={"width": "100%"},
)





def render(app: Dash) -> html.Div:
    @app.callback(
    Output(ids.MAP_FIG, "clickData"), [Input(ids.GET_DATA_BUTTON, "n_clicks"),State(ids.LAT_INPUT,'value'),State(ids.LON_INPUT,'value'),State(ids.MAP_FIG,'clickData')]
    )
    def on_button_click(n,lat,lon,clickData):
        if n is None:
            return None
        else:
            clickData['latlng'] = {'lat':lat,'lng':lon}
            return clickData
   


    return html.Div(
        [
            card
        ]
    )
