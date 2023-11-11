# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:57:52 2023
This model handles the plotting of transects and drawing of transect map layers

@author: jim
"""

# dash imports
from dash import dcc, html

# plotting imports
import plotly.express as px
import dash_leaflet as dl

# data science imports
import numpy as np

# project imports
from . import ids, text
from ..dataHandling.transects import calculateTransect
from ..dataHandling.geoTools import getEndCoord
from ..dataHandling.bathretriever import bathdata

def drawTransects(startLatLon, endLatLon):
    return dl.Polyline(positions=[startLatLon,endLatLon],color='red')

def plotTransects(data:bathdata,transectType:str,inputs:dict)->html.Div:
            # high coupling with bathOptCard related to the inputs dict
            if transectType == text.transect_single:
          
                sLat, sLon = inputs['lat-start'],inputs['lon-start']
                eLat, eLon = inputs['lat-end'], inputs['lon-end']
  
            
                r,transect = calculateTransect(data, sLat, sLon, eLat, eLon)
                fig = px.line(x=r,y=transect,title=f'Transect from [{sLat:.2f},{sLon:.2f}] to [{eLat:.2f},{eLon:.2f}]')
               
       
                fig.update_layout(xaxis_title="Range (m)", yaxis_title="Depth (m)")
           
                mapLayers = drawTransects([sLat,sLon], [eLat,eLon])
                
            if transectType ==text.transect_singleAz:
                sLat, sLon = inputs['lat-start'],inputs['lon-start']
                eLat, eLon = getEndCoord(sLat,sLon,inputs['single-azimuth'],inputs['km'])
                
                r,transect = calculateTransect(data, sLat, sLon, eLat, eLon)
              
                fig = px.line(x=r,y=transect,title=f'Transect from [{sLat:.2f},{sLon:.2f}] to [{eLat:.2f},{eLon:.2f}]')
               
       
                fig.update_layout(xaxis_title="Range (m)", yaxis_title="Depth (m)")
               
                mapLayers = drawTransects([sLat,sLon], [eLat,eLon])
                
            if transectType == text.transect_multiple:
                sLat, sLon = inputs['lat-start'],inputs['lon-start']
           
                # get end coordinate arrays
                num = int(np.round(360/inputs['radial-step']))
                az = np.linspace(0,360,num=num)
           
                fig = px.line()
                mapLayers = []
                for i,azVal in enumerate(az):
                    eLat,eLon = getEndCoord(sLat,sLon,azVal,inputs['km'])
            
               
                    r,transect = calculateTransect(data, sLat, sLon, eLat, eLon)
            
                    fig.add_trace(px.line(x=r,y=transect).data[0])
                    mapLayers.append(drawTransects([sLat,sLon], [eLat,eLon]))
                    
                fig.update_layout(xaxis_title="Range (m)", yaxis_title="Depth (m)",autosize=True)
                    
                
            figure = html.Div(dcc.Graph(figure=fig,style={'width': '100%', 'height': '60vh'}, id=ids.TRANSECT_PLOT))    
            return figure,mapLayers