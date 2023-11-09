# -*- coding: utf-8 -*-
"""A collection of tools wrapping pyproj"""

import os.path


import numpy as np
from dataclasses import dataclass
import scipy.io
import scipy.ndimage as snd
from pyproj import Geod
import pickle


geod = Geod(ellps="WGS84")





def getEndCoord(sLat,sLon,az,minutes):
    
    offset = minutes/60.0
    cornerLat = sLat+offset
    cornerLon = sLon+offset
    
    eastDist = geod.line_length([sLon,cornerLon],[sLat,sLat])
    northDist = geod.line_length([sLon,sLon],[sLat,cornerLat])
    
    dist = np.min([eastDist,northDist])
    
    print(f'radial distance = {dist:.1f} m')
    
    eLon, eLat, back = geod.fwd(sLon,sLat,az,dist)
    
    return eLat,eLon

@dataclass
class boundingBox:
    nLat:float
    sLat:float
    eLon:float
    wLon:float
    
def getBoundingBox(cLat:float,cLon:float,radial_distance_km:float)->boundingBox:
    """Calculate bounding coordinates based on center latitude and longitude and a radial distance in km"""
    
    dist = radial_distance_km*1000.0
    _, nLat, _ = geod.fwd(cLon,cLat,0.,dist)
    eLon, _, _ = geod.fwd(cLon,cLat,90.,dist)
    _, sLat, _ = geod.fwd(cLon,cLat,180.,dist)
    wLon, _, _ = geod.fwd(cLon,cLat,270.,dist)
    
    return boundingBox(nLat, sLat, eLon, wLon)
    
    