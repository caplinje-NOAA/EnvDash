
from dash import Dash, dcc, html,State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import numpy as np

from . import ids, text
from ..dataHandling import bathretriever, sspretriever, read_usSeabed, transects
from ..dataHandling.geoTools import BBfromDict, getEndCoord


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

# Download cards for each item in canvas
transCard = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Transects", className="card-title"),  
                
                html.Div(children=[
                    ], id=ids.TRANSECT_INPUTS_DISPLAY
                ),
                html.Div('Resolution:'),
                dcc.Dropdown(['Dataset native', 'Current selected (Stride)'], 'Dataset native', id=ids.TRANSECT_RES_DROPDOWN, searchable=False,clearable=False),
                dbc.Button("Download (.netcdf)", id=ids.TRANSECT_DOWNLOAD_BUTTON,class_name='button'),
                dcc.Download(id=ids.TRANSECT_DOWNLOAD),
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
                dbc.Button("Download", id=ids.SSP_DOWNLOAD_BUTTON,class_name='button'),
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
                dbc.Button("Download (.csv)", id=ids.SEABED_DOWNLOAD_BUTTON,class_name='button'),
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
                        html.Div(f'Stride = {inputs["stride"]} steps'),
                        html.Div(f'Data Source: {inputs["source"]}'),
                        html.Hr(),
            
            ])
    
def transInputDiv(inputs:dict)->str:
    """creates div summary of current bath inputs"""
    
    if inputs=={}:
        return html.Div('No inputs selected.')
    else:
        if inputs['transectType']==text.transect_single:
            return html.Div([
                            html.Hr(),
                            html.H6('Current Inputs:'),
                            html.Div(f'Transect type: {inputs["transectType"]}'),
                            html.Div(f'Start Coord. = {text.coordToStr(inputs["lat-start"],inputs["lon-start"])}'),
                            html.Div(f'End Coord. = {text.coordToStr(inputs["lat-end"],inputs["lon-end"])}'),
                            html.Div(f'Bounding box half-width = {int(inputs["km"])} km'),
                            html.Hr(),
                
                ])
            
            
        if inputs['transectType']==text.transect_singleAz:
            return html.Div([
                            html.Hr(),
                            html.H6('Current Inputs:'),
                            html.Div(f'Transect type: {inputs["transectType"]}'),
                            html.Div(f'Start Coord. = {text.coordToStr(inputs["lat-start"],inputs["lon-start"])}'),
                            html.Div(f'Azimuth = {inputs["single-azimuth"]} deg. rel. N'),
                            html.Div(f'Bounding box half-width = {int(inputs["km"])} km'),
                            html.Hr(),
                
                ])
            
        if inputs['transectType']==text.transect_multiple:
            
            return html.Div([
                            html.Hr(),
                            html.H6('Current Inputs:'),
                            html.Div(f'Transect type: {inputs["transectType"]}'),
                            html.Div(f'Start Coord. = {text.coordToStr(inputs["lat-start"],inputs["lon-start"])}'),
                            html.Div(f'Azimuth Step = {inputs["radial-step"]} deg.'),
                            html.Div(f'Bounding box half-width = {int(inputs["km"])} km'),
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
    
    @app.callback(
        Output(ids.TRANSECT_DOWNLOAD,'data'),
        
        Input(ids.TRANSECT_DOWNLOAD_BUTTON,'n_clicks'),
        State(ids.TRANSECT_INPUTS_STORE,'data'),
        State(ids.TRANSECT_RES_DROPDOWN,'value'),
        State(ids.BATH_INPUTS_STORE,'data'),
        State(ids.BATH_PLOT,'figure'),
        prevent_initial_call=True
        
        )
    def downloadTransects(n,inputs,resOption,bathInputs,bathfig):
        
      
        # get bath data
        BB = BBfromDict(bathInputs)
        bathsource=bathInputs['source']
        coordStr = text.coordToStr(inputs['lat-start'],inputs['lon-start'],fnStyled=True)        
        fn = f'trans_{bathsource}_near{coordStr}'
        if resOption=='Dataset native':
            data = bathretriever.retrieve(BB,DataSet=bathsource,downCast=False)
        else:
            data = bathretriever.bathdata(lat=np.array(bathfig['data'][0]['y']),
                            lon = np.array(bathfig['data'][0]['x']),
                            topo= np.array(bathfig['data'][0]['z']),
                            error = None)
        if inputs['transectType']==text.transect_single:
            sLat, sLon = inputs['lat-start'],inputs['lon-start']
            eLat, eLon = inputs['lat-end'], inputs['lon-end']
  
        
            r,transect = transects.calculateTransect(data, sLat, sLon, eLat, eLon)     
            ds = transects.transToDataSet(r, transect)
            return dcc.send_bytes(ds.to_netcdf(), f'{fn}.netcdf')
            
        if inputs['transectType']==text.transect_singleAz:
            sLat, sLon = inputs['lat-start'],inputs['lon-start']
            eLat, eLon = getEndCoord(sLat,sLon,inputs['single-azimuth'],inputs['km'])
            
            r,transect = transects.calculateTransect(data, sLat, sLon, eLat, eLon)
            ds = transects.transToDataSet(r, transect)
            return dcc.send_bytes(ds.to_netcdf(), f'{fn}.netcdf')

            
        if inputs['transectType']==text.transect_multiple:
            sLat, sLon = inputs['lat-start'],inputs['lon-start']
            
            ds = transects.calculateMultipleTransects(data, sLat, sLon, inputs['km'], inputs['radial-step'])

            return dcc.send_bytes(ds.to_netcdf(), f'{fn}.netcdf')
                

        # convert list inputs to dictionary, high coupling warning here

        
        
        # BB = BBfromDict(inputs)
        # month = inputs['month']
        # coordStr = text.coordToStr(inputs["center"][0],inputs["center"][1],fnStyled=True)        
        # fn = f'SSP_{month}_near{coordStr}'
        # if fileType=='csv':
        #     # get profiles
        #     df = sspretriever.retrieveSSprofiles(BB,Month=month,as_DataFrame=True)
        #     return dcc.send_data_frame(df.to_csv, f'{fn}.csv')
        
        # else:
        #     ds = sspretriever.retrieveSSprofiles(BB,Month=month)
        #     return dcc.send_bytes(ds.to_netcdf(), f'{fn}.netcdf')
        return None
        

            
            
            
   
    # main callback which opens the canvas
    @app.callback(
        Output(ids.DOWNLOAD_CANVAS, "is_open"),
        Output(ids.BATH_INPUTS_DISPLAY, "children"),
        Output(ids.SSP_INPUTS_DISPLAY, "children"),
        Output(ids.SEABED_INPUTS_DISPLAY, "children"),
        Output(ids.TRANSECT_INPUTS_DISPLAY,"children"),
        Output(ids.DOWNLOAD_BATH_BUTTON, "href"),
        Input(ids.DOWNLOAD_CANVAS_BUTTON, "n_clicks"),
        [State(ids.DOWNLOAD_CANVAS, "is_open"),
         State(ids.BATH_INPUTS_STORE, 'data'),
         State(ids.SSP_INPUTS_STORE,'data'),
         State(ids.SEABED_INPUTS_STORE,'data'),
         State(ids.TRANSECT_INPUTS_STORE,'data'),
    
         
         ],
    )
    def toggle_offcanvas(n1, is_open, bath_inputs,ssp_inputs,seabed_inputs,transect_inputs):
        if n1:
        
            # prepare raw bathymetry download
            bathsource = bath_inputs['source']
            BB = BBfromDict(bath_inputs)
            bathlink = bathretriever.retrieve(BB,DataSet=bathsource, returnOnlyRequest=True)
            
            # input displays
            bathInputDisplay = bathInputDiv(bath_inputs)
            sspInputDisplay = sspInputDiv(ssp_inputs)
            seabedInputDisplay = seabedInputDiv(seabed_inputs)
            transectInputDisplay = transInputDiv(transect_inputs)
            
            canvasStatus = not is_open
            return canvasStatus, bathInputDisplay,sspInputDisplay,seabedInputDisplay,transectInputDisplay,bathlink
        return is_open

    return html.Div(
        [
            
            
            dbc.Offcanvas(html.Div([
                                    bathCard,
                                    transCard,
                                    sspCard,
                                    seabedCard
               
                ]),    
                id=ids.DOWNLOAD_CANVAS,
                title="Downloads",
                is_open=False,
            ),
        ]
    )
