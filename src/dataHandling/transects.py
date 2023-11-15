# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:12:00 2023
Method for calculating line transects from topographic data
@author: jim
"""

# data science imports
import numpy as np
import scipy.ndimage as snd

# project imports
from .geoTools import lineLength
from .bathretriever import bathdata


def calculateTransect(data:bathdata,sLat,sLon,eLat,eLon, method='interpolate', truncate=False):

    
    def toPixel(coord_latlon):

        latPixel = np.argmin(np.abs(coord_latlon[0]-data.lat))
        lonPixel = np.argmin(np.abs(coord_latlon[1]-data.lon))
        
        return [latPixel,lonPixel]
    
    startCoord = [sLat,sLon]
    endCoord = [eLat,eLon]

    
    # convert to pixel coords
    startPixelCoord = toPixel(startCoord)
    endPixelCoord = toPixel(endCoord)
    
    transLenPixels = int(np.round(np.hypot(startPixelCoord[0]-endPixelCoord[0],startPixelCoord[1]-endPixelCoord[1])))

    
    # define x dimension as longitude, in pixel coordinates ..... y ... latitude ....
    
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
        
        
    
    return r, transect