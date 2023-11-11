# -*- coding: utf-8 -*-
"""A collection of tools wrapping pyproj"""

# data science imports
from dataclasses import dataclass
from pyproj import Geod



geod = Geod(ellps="WGS84")


# !! coupling warning, many modules depend on content of bounding box
@dataclass
class boundingBox:
    north:float
    south:float
    east:float
    west:float
    
    cLat:float
    cLon:float
    halfwidth_km:float
    
def getBoundingBox(cLat:float,cLon:float,halfwidth_km:float)->boundingBox:
    """Calculate bounding coordinates based on center latitude and longitude and a half-box-width distance in km"""
    
    dist = halfwidth_km*1000.0
    _, north, _ = geod.fwd(cLon,cLat,0.,dist)
    east, _, _ = geod.fwd(cLon,cLat,90.,dist)
    _, south, _ = geod.fwd(cLon,cLat,180.,dist)
    west, _, _ = geod.fwd(cLon,cLat,270.,dist)
    
    return boundingBox(north, south, east, west, cLat, cLon, halfwidth_km)


def getEndCoord(sLat,sLon,az,km):
    
    dist = km*1000.0
    
    eLon, eLat, back = geod.fwd(sLon,sLat,az,dist)
    
    return eLat,eLon
    
    
def lineLength(startLat,startLon,endLat,endLon):
    return geod.line_length([startLon,endLon],[startLat,endLat])