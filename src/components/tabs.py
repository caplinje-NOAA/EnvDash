# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 13:08:01 2023

@author: jim

Tab layout and callback for primary content
"""

from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc


from . import bathOptCard,ids,sspOptCard

# Container for left figure / object
spinner  =        dcc.Loading(
                    id=ids.TAB_SPINNER,
                    children=[html.Div()],
                    type="circle",
                )

# Container for right figure / object (e.g. transects)
spinnerSecondary =        dcc.Loading(
                    id=ids.TAB_SPINNER_SECONDARY,
                    children=[html.Div()],
                    type="circle",
                )

# container for all figures (bottom section of tabs, width sets ratio (out of 12))
tabContent = dbc.Row([dbc.Col(spinner,width=7,id=ids.PRIMARY_FIGURE_COLUMN),
                      dbc.Col(spinnerSecondary)])


def render(app: Dash) -> html.Div:
    
    @callback(
    Output(ids.GET_DATA_BUTTON, "n_clicks",allow_duplicate=True),    
    [Input(ids.TABS, 'value'),
    State(ids.GET_DATA_BUTTON, "n_clicks")],
    prevent_initial_call=True
    )
    def update_tabs(value,n):
        """Update data if tab changes"""

        return n+1
    
    return html.Div([
        # children are the upper portion of the tab (i.e. the options, etc)
        dcc.Tabs(id=ids.TABS, value='bath-tab', children=[
            dcc.Tab(label='Bathymetry', value='bath-tab',children=[bathOptCard.render(app)]),
            dcc.Tab(label='Sound Speed', value='ssp-tab',children=[sspOptCard.render(app)]),
            dcc.Tab(label='Seabed', value='seabed-tab',children=[html.Div()]),
        ]),
        # actual figures / tables go in tab content
        tabContent
    ])

#### OLD CALLBACKS FOR ADJUSTING MAP LAYER, REMOVING/HIGHLIGHTING SSP POINTS

    # @callback(
    #     Output({'type':ids.WOA_DATA_MARKER,"location":ALL},'opacity'),
    #     Output(ids.SSP_PLOT,'figure'),
    #     Output(ids.SSP_EXCLUDE_DROPDOWN,'options'),
    #     Output(ids.SSP_EXCLUDE_DROPDOWN,'value'),
        
    #     [Input(ids.SSP_PLOT,'clickData'),
    #      State({'type':ids.WOA_DATA_MARKER,"location":ALL},'id'),
    #      State({'type':ids.WOA_DATA_MARKER,"location":ALL},'opacity'),
    #      State(ids.SSP_PLOT,'figure'),
    #      State(ids.SSP_EXCLUDE_DROPDOWN,'options')
    #      ]
    #     )
    # def ExcludedMarker(clickData,markerIds,markerOp,fig,excludeList):
    #     if clickData:
    #         print(clickData)
    #         curve = clickData['points'][0]['curveNumber']
    #         name = fig['data'][curve]['name']
    #         if excludeList==['none']:
    #             excludelist=[name]
    #         else:
    #             excludeList.append(name)
    #         fig['data'][curve]['visible']=False
        
    #         for i,markerID in enumerate(markerIds):
           
    #             if name == markerID['location']:
    #                 markerOp[i]=.2
        
     
     
        
               
                    
    #     return markerOp,fig,excludeList,excludeList

            
    
    
    # @callback(
    #     Output({'type':ids.WOA_DATA_MARKER,"location":ALL},'color'),
        
    #     [Input(ids.SSP_PLOT,'hoverData'),
    #      State({'type':ids.WOA_DATA_MARKER,"location":ALL},'id'),
    #      State(ids.SSP_PLOT,'figure')
    #      ]
    #     )
    # def highlightHoveredMarker(hoverData,markerIds,fig):
    #     curve = hoverData['points'][0]['curveNumber']
    #     name = fig['data'][curve]['name']
    #     colors = []
    #     for markerID in markerIds:
       
    #         if name == markerID['location']:
    #             colors.append('red')
    #         else:
    #             colors.append('blue')
                
    #     return colors