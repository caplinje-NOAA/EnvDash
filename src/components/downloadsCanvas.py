
from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


from . import ids, text
from ..dataHandling import bathretriever, sspretriever, read_usSeabed
from ..dataHandling.geoTools import BBfromDict


# Download cards for each item in canvas
bathCard = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Raw Bathymetric Data", className="card-title"),
                
                
                html.Div(children=[
                    ], id=ids.BATH_INPUTS_DISPLAY
                ),
                dbc.Button("Download (.mat)", id=ids.DOWNLOAD_BATH_BUTTON,class_name='button',external_link=True),
            ]
        ),
    ],
    style={"width": "100%"},
)

sspCard = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Sound Speed Profile Data", className="card-title"),
                
                
                html.Div(children=[
                    ], id=ids.SSP_INPUTS_DISPLAY
                ),
                html.Div('File type:'),
                dcc.Dropdown(['csv', 'netcdf'], 'netcdf', id=ids.SSP_FILE_TYPE_DROPDOWN, searchable=False,clearable=False),
                dbc.Button("Download", id=ids.SSP_DOWNLOAD_BUTTON,class_name='button',external_link=True),
                dcc.Download(id=ids.SSP_DOWNLOAD)
            ]
        ),
    ],
    style={"width": "100%"},
)

seabedCard = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Seabed Data", className="card-title"),
                
                
                html.Div(children=[
                    ], id=ids.SEABED_INPUTS_DISPLAY
                ),
                html.Div('File type:'),
                dbc.Button("Download (.csv)", id=ids.SEABED_DOWNLOAD_BUTTON,class_name='button',external_link=True),
                dcc.Download(id=ids.SEABED_DOWNLOAD)
            ]
        ),
    ],
    style={"width": "100%"},
)

def bathInputDiv(inputs:dict)->str:
    """creates div summary of current bath inputs"""
    
    if inputs=={}:
        return html.Div('No inputs selected.')
    else:
        return html.Div([
                        html.Hr(),
                        html.H6('Current Inputs:'),
                        html.Div(f'Center Coord. = {text.coordToStr(inputs["center"][0],inputs["center"][1])}'),
                        html.Div(f'Bounding box half-width = {int(inputs["km"])} km'),
                        html.Div(f'Data Source: {inputs["source"]}'),
                        html.Hr(),
            
            ])
    
def sspInputDiv(inputs:dict)->str:
    """creates div summary of current bath inputs"""
    
    if inputs=={}:
        return html.Div('No inputs selected.')
    else:
        return html.Div([
                        html.Hr(),
                        html.H6('Current Inputs:'),
                        html.Div(f'Center Coord. = {text.coordToStr(inputs["center"][0],inputs["center"][1])}'),
                        html.Div(f'Bounding box half-width = {int(inputs["km"])} km'),
                        html.Div(f'Month: {inputs["month"]}'),
                        html.Hr(),
            
            ])
    
def seabedInputDiv(inputs:dict)->str:
    """creates div summary of current bath inputs"""
    
    if inputs=={}:
        return html.Div('No inputs selected.')
    else:
        return html.Div([
                        html.Hr(),
                        html.H6('Current Inputs:'),
                        html.Div(f'Center Coord. = {text.coordToStr(inputs["center"][0],inputs["center"][1])}'),
                        html.Div(f'Bounding box half-width = {int(inputs["km"])} km'),
                        html.Div(f'Max. Observations = {inputs["n"]}'),
                        html.Hr(),
            
            ])
    

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.SSP_DOWNLOAD,'data'),
        Input(ids.SSP_DOWNLOAD_BUTTON,'n_clicks'),
        State(ids.SSP_FILE_TYPE_DROPDOWN,'value'),
        State(ids.SSP_INPUTS_STORE,'data'),
        prevent_initial_call=True
        
        )
    def downloadSSP(n,fileType,inputs):
        BB = BBfromDict(inputs)
        month = inputs['month']
        coordStr = text.coordToStr(inputs["center"][0],inputs["center"][1],fnStyled=True)        
        fn = f'SSP_{month}_near{coordStr}'
        if fileType=='csv':
            # get profiles
            df = sspretriever.retrieveSSprofiles(BB,Month=month,as_DataFrame=True)
            return dcc.send_data_frame(df.to_csv, f'{fn}.csv')
        
        else:
            ds = sspretriever.retrieveSSprofiles(BB,Month=month)
            return dcc.send_bytes(ds.to_netcdf(), f'{fn}.netcdf')
        
    @app.callback(
        Output(ids.SEABED_DOWNLOAD,'data'),
        Input(ids.SEABED_DOWNLOAD_BUTTON,'n_clicks'),
        State(ids.SEABED_INPUTS_STORE,'data'),
        prevent_initial_call=True
        
        )
    def downloadSeabed(n,inputs):
        BB = BBfromDict(inputs)
        n= inputs['n']
        coordStr = text.coordToStr(inputs["center"][0],inputs["center"][1],fnStyled=True)        
        fn = f'usSEABEDsubset_near{coordStr}.csv'

        df,total = read_usSeabed.getBoundedData(BB,n)
        
        if total==0:
            return None
           
        return dcc.send_data_frame(df.to_csv, fn)
        

            
            
            
   
    # main callback which opens the canvas
    @app.callback(
        Output(ids.DOWNLOAD_CANVAS, "is_open"),
        Output(ids.BATH_INPUTS_DISPLAY, "children"),
        Output(ids.SSP_INPUTS_DISPLAY, "children"),
        Output(ids.SEABED_INPUTS_DISPLAY, "children"),
        Output(ids.DOWNLOAD_BATH_BUTTON, "href"),
        Input(ids.DOWNLOAD_CANVAS_BUTTON, "n_clicks"),
        [State(ids.DOWNLOAD_CANVAS, "is_open"),
         State(ids.BATH_INPUTS_STORE, 'data'),
         State(ids.SSP_INPUTS_STORE,'data'),
         State(ids.SEABED_INPUTS_STORE,'data')
    
         
         ],
    )
    def toggle_offcanvas(n1, is_open, bath_inputs,ssp_inputs,seabed_inputs):
        if n1:
        
            # prepare raw bathymetry download
            bathsource = bath_inputs['source']
            BB = BBfromDict(bath_inputs)
            bathlink = bathretriever.retrieve(BB,DataSet=bathsource, returnOnlyRequest=True)
            
            # input displays
            bathInputDisplay = bathInputDiv(bath_inputs)
            sspInputDisplay = sspInputDiv(ssp_inputs)
            seabedInputDisplay = seabedInputDiv(seabed_inputs)
            
            canvasStatus = not is_open
            return canvasStatus, bathInputDisplay,sspInputDisplay,seabedInputDisplay,bathlink
        return is_open

    return html.Div(
        [
            
            
            dbc.Offcanvas(html.Div([
                                    bathCard,
                                    sspCard,
                                    seabedCard
               
                ]),    
                id=ids.DOWNLOAD_CANVAS,
                title="Downloads",
                is_open=False,
            ),
        ]
    )
