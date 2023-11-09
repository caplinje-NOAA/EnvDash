
from dash import Dash, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


from . import ids,bathplot, ssplot


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

# dictionary container render methods
renderer = {'bath-tab':bathplot,'ssp-tab':ssplot,'seabed-tab':None}


def render(app: Dash) -> html.Div:
    @app.callback(
    # outputs are the two object/figure containers, any map layers, and the alert div    
    Output(ids.TAB_SPINNER, 'children'),
    Output(ids.TAB_SPINNER_SECONDARY, "children",allow_duplicate=True),
    Output(ids.MAP_LAYER, "children"),
    Output(ids.ALERT, "children"), 
    
    [Input(ids.GET_DATA_BUTTON, "n_clicks"),
     State(ids.TABS, 'value'),
     State(ids.LAT_INPUT,'value'),
     State(ids.LON_INPUT,'value'),
     State(ids.BB_MIN,'value'),
     State(ids.SSP_MONTH_DROPDOWN,'value'),
     State(ids.BATH_SOURCE_DROPDOWN,'value'),
     State(ids.TAB_SPINNER_SECONDARY, "children")],
     prevent_initial_call=True
     
    )
    def primary_app_callback(n,tab_value,lat,lon,minutes,month,bathsource,secondaryChild):
        """This is the main callback, that is duplicate output of all callbacks that trigger
        a data update.  Gathers all data and updates most content"""
        if n is None:
            return None
        else:
            click_lat_lng = [lat,lon]
            
            # secondary child div contains transects for the bath tab
            # passing the child through this callback allows it to remain
            # 
            if tab_value == 'bath-tab':
                outSecondaryChild = secondaryChild
            else:
                outSecondaryChild = []
                
            fig, mapLayer, alert = renderer[tab_value].render(click_lat_lng,minutes,month,bathsource)
    
    
            return fig, outSecondaryChild, mapLayer, alert
   


    return html.Div(
        [
            card
        ]
    )


## dictionary version of callback signature
# output = dict(
#             fig = Output(ids.TAB_SPINNER, 'children'),
#             outSecondaryChild = Output(ids.TAB_SPINNER_SECONDARY, "children",allow_duplicate=True),
#             mapLayer = Output(ids.MAP_LAYER, "children"),
#             alert = Output(ids.ALERT, "children")
#     )

# inputs = dict(n = Input(ids.GET_DATA_BUTTON, "n_clicks"))

# state = dict(
#         tab_value = State(ids.TABS, 'value'),
#         lat = State(ids.LAT_INPUT,'value'),
#         lon = State(ids.LON_INPUT,'value'),
#         minutes = State(ids.BB_MIN,'value'),
#         month = State(ids.SSP_MONTH_DROPDOWN,'value'),
#         bathsource = State(ids.BATH_SOURCE_DROPDOWN,'value'),
#         secondaryChild = State(ids.TAB_SPINNER_SECONDARY, "children")
#     )


## Old callback from tabs (used to be the fundamental callback)
    # @callback(
    # Output(ids.TAB_SPINNER, 'children'),
    # Output(ids.TAB_SPINNER_SECONDARY, "children",allow_duplicate=True),
    # Output(ids.MAP_LAYER, "children"),
    # Output(ids.ALERT, "children"),
    # [Input(ids.TABS, 'value'),
    # State(ids.MAP_FIG, "clickData"),
    # State(ids.BB_MIN,'value'),
    # State(ids.SSP_MONTH_DROPDOWN,'value'),
    # State(ids.BATH_SOURCE_DROPDOWN,'value'),
    # State(ids.TAB_SPINNER_SECONDARY, "children")],
    # prevent_initial_call=True
    # )
    # def update_tabs(value,clickData,minutes,month,bathsource,secondaryChild):
    #     """This is the primary callback.  When tab value is triggered, gather all inputs, retrieve appropriate data, 
    #     and update figures"""
    #     lat = clickData['latlng']['lat']
    #     lng = clickData['latlng']['lng']
    #     click_lat_lng = [lat,lng]
        
    #     # secondary child div contains transects for the bath tab
    #     # passing the child through this callback allows it to remain
    #     # 
    #     if value == 'bath-tab':
    #         outSecondaryChild = secondaryChild
    #     else:
    #         outSecondaryChild = []
            
    #     fig, mapLayer, alert = renderer[value].render(click_lat_lng,minutes,month,bathsource)


    #     return fig, outSecondaryChild, mapLayer, alert