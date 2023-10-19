# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 13:08:01 2023

@author: jim
"""

from dash import Dash, dcc, html, Input, Output, callback, State, ALL
import dash_bootstrap_components as dbc


from . import map_fig, bathplot, ssplot, genOptCard, bathOptCard,ids,sspOptCard

spinner  =        dcc.Loading(
                    id=ids.TAB_SPINNER,
                    children=[html.Div()],
                    type="circle",
                )

spinnerSecondary =        dcc.Loading(
                    id=ids.TAB_SPINNER_SECONDARY,
                    children=[html.Div()],
                    type="circle",
                )

tabContent = dbc.Row([dbc.Col(spinner,width=7,id=ids.PRIMARY_FIGURE_COLUMN),
                      dbc.Col(spinnerSecondary)])



# tabs = html.Div([
#     dcc.Tabs(id=ids.TABS, value='bath-tab', children=[
#         dcc.Tab(label='Bathymetry', value='bath-tab',children=[bathOptCard.render(Dash)]),
#         dcc.Tab(label='Sound Speed', value='ssp-tab',children=[sspOptCard.render()]),
#         dcc.Tab(label='Seabed', value='seabed-tab',children=[html.Div()]),
#     ]),
#     spinner
# ])

renderer = {'bath-tab':bathplot,'ssp-tab':ssplot,'seabed-tab':None}



def render(app: Dash) -> html.Div:
    @callback(
        Output({'type':ids.WOA_DATA_MARKER,"location":ALL},'opacity'),
        Output(ids.SSP_PLOT,'figure'),
        Output(ids.SSP_EXCLUDE_DROPDOWN,'options'),
        Output(ids.SSP_EXCLUDE_DROPDOWN,'value'),
        
        [Input(ids.SSP_PLOT,'clickData'),
         State({'type':ids.WOA_DATA_MARKER,"location":ALL},'id'),
         State({'type':ids.WOA_DATA_MARKER,"location":ALL},'opacity'),
         State(ids.SSP_PLOT,'figure'),
         State(ids.SSP_EXCLUDE_DROPDOWN,'options')
         ]
        )
    def ExcludedMarker(clickData,markerIds,markerOp,fig,excludeList):
        if clickData:
            print(clickData)
            curve = clickData['points'][0]['curveNumber']
            name = fig['data'][curve]['name']
            if excludeList==['none']:
                excludelist=[name]
            else:
                excludeList.append(name)
            fig['data'][curve]['visible']=False
        
            for i,markerID in enumerate(markerIds):
           
                if name == markerID['location']:
                    markerOp[i]=.2
        
     
     
        
               
                    
        return markerOp,fig,excludeList,excludeList

            
    
    
    @callback(
        Output({'type':ids.WOA_DATA_MARKER,"location":ALL},'color'),
        
        [Input(ids.SSP_PLOT,'hoverData'),
         State({'type':ids.WOA_DATA_MARKER,"location":ALL},'id'),
         State(ids.SSP_PLOT,'figure')
         ]
        )
    def highlightHoveredMarker(hoverData,markerIds,fig):
        curve = hoverData['points'][0]['curveNumber']
        name = fig['data'][curve]['name']
        colors = []
        for markerID in markerIds:
       
            if name == markerID['location']:
                colors.append('red')
            else:
                colors.append('blue')
                
        return colors
    
    @callback(
    Output(ids.TAB_SPINNER, 'children'),
    Output(ids.TAB_SPINNER_SECONDARY, "children",allow_duplicate=True),
    Output(ids.MAP_LAYER, "children"),
    Output(ids.ALERT, "children"),
    [Input(ids.TABS, 'value'),
    State(ids.MAP_FIG, "clickData"),
    State(ids.BB_MIN,'value'),
    State(ids.SSP_MONTH_DROPDOWN,'value'),
    State(ids.BATH_SOURCE_DROPDOWN,'value'),
    State(ids.TAB_SPINNER_SECONDARY, "children")],
    prevent_initial_call=True
    )
    def update_tabs(value,clickData,minutes,month,bathsource,secondaryChild):
        lat = clickData['latlng']['lat']
        lng = clickData['latlng']['lng']
        click_lat_lng = [lat,lng]
        if value == 'bath-tab':
            outSecondaryChild = secondaryChild
        else:
            outSecondaryChild = []
            
        fig, mapLayer, alert = renderer[value].render(click_lat_lng,minutes,month,bathsource)


        return fig, outSecondaryChild, mapLayer, alert
    
    return html.Div([
        dcc.Tabs(id=ids.TABS, value='bath-tab', children=[
            dcc.Tab(label='Bathymetry', value='bath-tab',children=[bathOptCard.render(app)]),
            dcc.Tab(label='Sound Speed', value='ssp-tab',children=[sspOptCard.render(app)]),
            dcc.Tab(label='Seabed', value='seabed-tab',children=[html.Div()]),
        ]),
        tabContent
    ])
