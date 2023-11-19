# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:53:59 2023
This module handles the rendering of SSP data
@author: jim
"""

# dash imports
from dash import dcc, Dash, html, Output, Input

# data science imports
import pandas as pd

# plotting imports
import plotly.express as px
import dash_leaflet as dl

# project imports
from ..dataHandling.sspretriever import retrieveSSprofiles
from ..dataHandling.geoTools import boundingBox, BBfromDict
from . import ids, alerts, text


inputsStore = dcc.Store(id=ids.SSP_INPUTS_STORE, storage_type='memory', data={})

print(ids.SSP_PLOT)
figure = html.Div(dcc.Graph(figure=px.line(),style={'width': '60vh', 'height': '60vh'},id=ids.SSP_PLOT))




soundSpeedContent = dcc.Loading(
                    id=ids.SSP_TAB_CONTENT,
                    children=[figure],
                    type="circle",
                ) 


def buildFig(df:pd.DataFrame,BB:boundingBox,month:str)->html.Div:   
    """Builds SSP figure Div"""
    if len(df)==0:
        return None
    fig = px.line(df,x='C',y='depth',color='Coordinate')
    
    fig.update_layout(title=f'{month} SSP near {text.coordToStr(BB.cLat,BB.cLon)}',
               xaxis_title='Sound Speed (m/s)',
               yaxis_title='Depth (m)')
    
    fig['layout']['yaxis']['autorange'] = "reversed"
    

    
    return fig
    
def buildMapMarkers(df:pd.DataFrame,BB:boundingBox):
    """builds an array of dl.Circle items of each SSP point"""
    """text and ids managed by text.py and ids.py"""
    markers = []
    locations = df['Coordinate'].unique()
    for loc in locations:
        center = text.strToCoord(loc)
        print(center)
        markers.append(
            dl.Circle(center=center,radius=500,children=dl.Tooltip(f'WOA (SSP) data, {loc}',id=ids.SSP_MARKER_TOOLTIP(loc)), 
                      id=ids.SSP_MARKER(loc),color='blue',opacity=1)
                      )
            
    return markers

def buildMapLayers(df,BB:boundingBox):
    """combines marker layer with center position marker"""
    mapLayers = [dl.Marker(position=[BB.cLat,BB.cLon], children=dl.Tooltip(f"Center, [{BB.cLat:.3f}, {BB.cLon:.3f}]"))]
    markers = buildMapMarkers(df,BB)
    mapLayers=mapLayers+markers 
    return mapLayers       
    
def render(app:Dash)->html.Div:
    @app.callback(
    # Updates the figure, sets map layers, and posts alert  
    Output(ids.SSP_PLOT, 'figure'),
    Output(ids.SSP_MAP_LAYER, "children"),
    Output(ids.ALERT, "children", allow_duplicate=True), 
    
    [Input(ids.SSP_INPUTS_STORE, "data"),   
     ],
     prevent_initial_call=True
     
    )
    def updatePlot(inputs):
        """ Sound speed renderer function in the same template as the other tab content"""   
    
        # unpack inputs
        BB = BBfromDict(inputs)
        month = inputs['month']
       
        # get profiles
        df = retrieveSSprofiles(BB,Month=month,as_DataFrame=True)
       
        # figure and layers
        fig = buildFig(df,BB,month)    
        mapLayers = buildMapLayers(df,BB)
        
        if not figure:
            alert = alerts.getAlert(alerts.warning,text.no_SSP_alert,duration = 8000)
        else:
            alert = alerts.getAlert(alerts.success,text.SSP_success)
      
        
        return fig, mapLayers, alert
    return html.Div([soundSpeedContent,inputsStore])


## get nearest profile method
#[gridLon,gridLat] = getWOAgrid(df)
#nearest = ds.sel(lon=lon_pnt,lat=lat_pnt,method='nearest')
#C = np.array(nearest.C)
#depth = np.array(nearest.depth)
#nonnan = ~np.isnan(C)
#C = C[nonnan]
#depth = depth[nonnan]
    
    
# legacy callback
# def render(app: Dash) -> html.Div:
#     # @app.callback(
#     #     Output(ids.BATH_PLOT, "children"),
#     #     [
#     #         Input(ids.MAP_FIG, "click_lat_lng"),
#     #     ],
#     # )
#     # def wait_for_data(click_lat_lng) -> html.Div:
       

#     #     return html.Div(dbc.Spinner(color="primary"))
    
#     @app.callback(
#         Output(ids.SSP_PLOT, "children"),
#         Output(ids.MAP_LAYER, "children"),
#         Output(ids.LAT_INPUT, "value"),
#         Output(ids.LON_INPUT, "value"),
#         Output(ids.SSP_ALERT_DIV, "children"),
#         Output(ids.SSP_INCLUDE_DROPDOWN,"options"),
#         Output(ids.SSP_INCLUDE_DROPDOWN,"value"),
#         [
#             Input(ids.MAP_FIG, "click_lat_lng"),
#             State(ids.BB_MIN,'value'),
#             State(ids.SSP_MONTH_DROPDOWN,'value')
#         ],
#     )
#     def update_chart(click_lat_lng,minutes,month) -> html.Div:
#         lat_pnt = click_lat_lng[0]
#         lon_pnt = click_lat_lng[1]
#         minutes = minutes/2
#         lonRange = [lon_pnt-minutes/60,lon_pnt+minutes/60]
#         latRange = [lat_pnt-minutes/60,lat_pnt+minutes/60]
#         ds = retrieveSSprofiles(lonRange,latRange,Month=month)
#         df = ds_to_df(ds)
#         [gridLon,gridLat] = getWOAgrid(ds)
#         nearest = ds.sel(lon=lon_pnt,lat=lat_pnt,method='nearest')
#         C = np.array(nearest.C)
#         depth = np.array(nearest.depth)
#         nonnan = ~np.isnan(C)
#         C = C[nonnan]
#         depth = depth[nonnan]
#         fig = buildFig(ds)
#         fig.update_layout(title=f'SSP near {str(click_lat_lng)}',
#                    xaxis_title='Sound Speed (m/s)',
#                    yaxis_title='Depth (m)')
#         fig['layout']['yaxis']['autorange'] = "reversed"
        
#         mapLayers = [dl.Rectangle(bounds=[[latRange[1], lonRange[1]], [latRange[0], lonRange[0]]],children=dl.Tooltip("Bounding box for bathymetry")),
#                      dl.Marker(position=click_lat_lng, children=dl.Tooltip("(Center, {:.3f}, {:.3f})".format(*click_lat_lng)))]
#         markers,locations = buildMapMarkers(ds)
#         mapLayers=mapLayers+markers

#         return [html.Div(dcc.Graph(figure=fig,style={'width': '60vh', 'height': '60vh'}), id=ids.SSP_PLOT), 
#                             mapLayers, 
#                             lat_pnt, 
#                             lon_pnt, 
#                             getAlert('success','Successfully loaded WOA temperature and sailinity data.'),
#                             locations,
#                             locations
                            
#                             ]

#     return spinner


