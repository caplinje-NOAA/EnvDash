# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:12:00 2023
Method for calculating line transects from topographic data
@author: jim
"""

# data science imports
import numpy as np
import scipy.ndimage as snd
import xarray as xr

# project imports
from .geoTools import lineLength, getEndCoord
from .bathretriever import bathdata


def calculateTransect(data:bathdata,sLat,sLon,eLat,eLon, method='interpolate',maxPixelPoint =False, truncate=False, range_km=None):

    
    def toPixel(coord_latlon):

        latPixel = np.argmin(np.abs(coord_latlon[0]-data.lat))
        lonPixel = np.argmin(np.abs(coord_latlon[1]-data.lon))
        
        return [latPixel,lonPixel]
    
    startCoord = [sLat,sLon]
    endCoord = [eLat,eLon]

    
    # convert to pixel coords
    startPixelCoord = toPixel(startCoord)
    endPixelCoord = toPixel(endCoord)

    
    # define x dimension as longitude, in pixel coordinates ..... y ... latitude ....
    if maxPixelPoint:
        if range_km:
            endCoord45d = getEndCoord(sLat,sLon,45,range_km)
            endPixelCoord45 = toPixel(endCoord45d)
            transLenPixels = int(np.round(np.hypot(startPixelCoord[0]-endPixelCoord45[0],startPixelCoord[1]-endPixelCoord45[1])))
        else:
            print('if using maxPixelPoint, range_km must be specified')
            return None, None
        
    else:
        transLenPixels = int(np.round(np.hypot(startPixelCoord[0]-endPixelCoord[0],startPixelCoord[1]-endPixelCoord[1])))
        
        
    x = np.round(np.linspace(startPixelCoord[1],endPixelCoord[1],num=transLenPixels)).astype(int)
    y = np.round(np.linspace(startPixelCoord[0],endPixelCoord[0],num=transLenPixels)).astype(int)
    
    if method=='nearest':
        transect = data.topo[y,x]
        lat = data.lat[y]
        lon = data.lon[x]
        
    elif method=='interpolate':
        lon = np.linspace(data.lon[startPixelCoord[1]],data.lon[endPixelCoord[1]],num=transLenPixels)
        lat = np.linspace(data.lat[startPixelCoord[0]],data.lat[endPixelCoord[0]],num=transLenPixels)
        transect = snd.map_coordinates(data.topo,[y,x])
    else:
        print(f'Unable to get transect using method {method}.  Method must be "nearest" or "interpolate"')
        return 
    
    r = np.zeros_like(transect)
 
    if truncate:
        for i,(lonVal,latVal,trans) in enumerate(zip(lon,lat,transect)):
            r[i] = lineLength(sLat, sLon, latVal, lonVal)
            if trans>0:
                r= r[:i]
                transect=transect[:i]
                break
                
        
            # if using pyproj import here
            #r[i] = geod.line_length([startCoord[1],lonVal],[startCoord[0],latVal])
    else:
        for i,(lonVal,latVal) in enumerate(zip(lon,lat)):
            r[i] = lineLength(sLat, sLon, latVal, lonVal)
        
        
    print(f'Transect points = {len(r)}')
    return r, transect

#def calculateMultipleTransects(data:bathdata,sLat:float,sLon:float,range_km:float,azStep:float, output='ds'):
    

    # # get end coordinate arrays
    # num = int(np.round(360/azStep))
    # az = np.linspace(0,360,num=num)

    # ds = xr.Dataset(
    #     data_vars=dict(
    #         range_m=(["x", "y", "azimuth"], temperature),
    #         depth_m=(["x", "y", "azimuth"], precipitation),

    #     ),

    #     coords=dict(
    #         lon=(["x", "y"], lon),
    #         lat=(["x", "y"], lat),
       
    #     ),

    #     attrs=dict(description="Bathymetric Transects."),

    # )
    # for i,azVal in enumerate(az):
    #     eLat,eLon = getEndCoord(sLat,sLon,azVal,range_km)
    
       
    #     r,transect = calculateTransect(data, sLat, sLon, eLat, eLon,truncate=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        