# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:49:56 2023

@author: jim
"""
import os.path


import numpy as np
from dataclasses import dataclass
import scipy.io
import scipy.ndimage as snd
from pyproj import Geod


geod = Geod(ellps="WGS84")


@dataclass
class bathdata:
    lat:np.ndarray
    lon:np.ndarray
    topo: np.ndarray
    error:str
    

def loadData(path,structname,variable,landMask=10.0):

    
    mat = scipy.io.loadmat(path)
    
    data = mat[structname]
    lat = np.squeeze(data['latitude'][0][0])
    lon = np.squeeze(data['longitude'][0][0])
    topo = data[variable][0][0]
    topo[topo>1]=landMask
    
    
    return bathdata(lat=lat,lon=lon,topo=topo,error=None)

# def retrieveTransect(bathdata,sLat,sLon,eLat,eLon):
    
#     def toPixel(coord_latlon):
#         latPixel = np.argmin(np.abs(coord_latlon[0]-bathdata.lat))
#         lonPixel = np.argmin(np.abs(coord_latlon[1]-bathdata.lon))
#         return [latPixel,lonPixel]
    
#     startCoord = [sLat,sLon]
#     endCoord = [eLat,eLon]
    
#     # convert to pixel coords
#     startPixelCoord = toPixel(startCoord)
#     endPixelCoord = toPixel(startCoord)
    
#     transLenPixels = int(np.hypot(startPixelCoord[0]-endPixelCoord[0],startPixelCoord[1]-endPixelCoord[1]))
    
    
#     # define x dimension as longitude, in pixel coordinates ..... y ... latitude ....
    
#     x = np.linspace(startPixelCoord[1],endPixelCoord[1],num=transLenPixels).astype(int)
#     print(x)
#     y = np.linspace(startPixelCoord[0],endPixelCoord[0],num=transLenPixels).astype(int)
    

#     transect = bathdata.topo[y,x]
#     lat = bathdata.lat[y]
#     lon = bathdata.lon[x]
    
    
#     r = np.zeros_like(transect)
    
#     for i,(lonVal,latVal) in enumerate(zip(lon,lat)):
#         r[i] = geod.line_length([startCoord[1],lonVal],[startCoord[0],latVal])
        
#     return r,transect
    

def retrieve(Latitude:float, Longitude:float, centerOffset_minutes:float=30., DataSet='SRTM')->bathdata:
    ## CRM volume information
    uid = int(np.abs(Latitude*Longitude*centerOffset_minutes*10))
    saveFile = f'{DataSet}{uid}.mat'
    dataPath = 'data/temp/'
    savePath = f'{dataPath}{saveFile}'
    

        
        
    
    if DataSet=='CRM':
      prefix = 'usgsCeCrm'
      vols = [1,2,3,4,5,6,7,8,9,10]
      Nbounds = np.array([48.00,40.00,35.00,36.00,38.00,37.00,44.00,49.00,20.00,24.00])
      Sbounds = np.array([40.00,31.00,24.00,24.00,24.00,32.00,37.00,44.00,16.00,18.00])
      Ebounds = np.array([-64.00,-68.00,-78.00,-87.00,-94.00,-114.00,-117.00,-116.00,-64.00,-152.00])
      Wbounds = np.array([-80.00,-85.00,-87.00,-94.00,-108.00,-126.00,-128.00,-128.00,-68.00,-162.00])
    
      def boundedBy(latitude,longitude):
        boundedIndex = -1
        for i,(N,S,E,W) in enumerate(zip(Nbounds,Sbounds,Ebounds,Wbounds)):
    
          if (latitude<N) and (latitude>S):
    
            if (longitude<E) and (longitude>W):
    
              boundedIndex = i
        return boundedIndex
    
      bounds = boundedBy(Latitude, Longitude)
    
      if bounds==-1:
        error = 'Inputted coordinates are not bounded by any CRM data sets.'
        filename='null'
        return bathdata(lat=None,lon=None,topo=None,error=error)
    
      else:
        filename = f'{prefix}{vols[bounds]:d}.mat'
        structname = f'{prefix}{vols[bounds]:d}'
        variable = 'topo'
        host = 'https://upwell.pfeg.noaa.gov/erddap/griddap/'
        # get bounds of data set
        lonRangeData = [Wbounds[bounds],Ebounds[bounds]]
        latRangeData = [Sbounds[bounds],Nbounds[bounds]]
        # define box offset to grab
        offset = centerOffset_minutes/60.0
        lonRange = [Longitude-offset,Longitude+offset]
        latRange = [Latitude-offset,Latitude+offset]
        # test if range is outside of dataset and set bounds accordingly if so
        if lonRange[0]<lonRangeData[0]:
          lonRange[0] = lonRangeData[0]
        if lonRange[1]>lonRangeData[1]:
          lonRange[1] = lonRangeData[1]
    
        if latRange[0]<latRangeData[0]:
          latRange[0] = latRangeData[0]
        if latRange[1]>latRangeData[1]:
          latRange[1] = latRangeData[1]
    
    
    
    
    if DataSet=='SRTM':
      lonRangeData = [-180,180]
      latRangeData = [-90,90]  
      filename = 'srtm15plus.mat'
      structname = 'srtm15plus'
      variable='z'
      host = 'https://coastwatch.pfeg.noaa.gov/erddap/griddap/'
    
    # define box offset to grab

    offset = centerOffset_minutes/60.0
    lonRange = [Longitude-offset,Longitude+offset]
    latRange = [Latitude-offset,Latitude+offset]
    # test if range is outside of dataset and set bounds accordingly if so
    if lonRange[0]<lonRangeData[0]:
      lonRange[0] = lonRangeData[0]
    if lonRange[1]>lonRangeData[1]:
      lonRange[1] = lonRangeData[1]
    
    if latRange[0]<latRangeData[0]:
      latRange[0] = latRangeData[0]
    if latRange[1]>latRangeData[1]:
      latRange[1] = latRangeData[1]
    
    if os.path.isfile(savePath):
        print(f'Succesfully loaded bathymetry data ({saveFile}) near ({Latitude:.3f},{Longitude:.3f}) from local storage.')
        return loadData(savePath, structname, variable)
    
    import urllib.request
    import urllib.error as urlerror
    
    query = f'?{variable}%5B({latRange[1]}):1:({latRange[0]})%5D%5B({lonRange[0]}):1:({lonRange[1]})%5D'
    fullurl = f'{host}{filename}{query}'
    try:
        req = urllib.request.urlretrieve(fullurl, savePath)
    except urlerror.HTTPError:
        return bathdata(lat=None,lon=None,topo=None,error='ERDDAP Server Temporarily Unavailable.')
    
    data = loadData(savePath, structname, variable)
    
    print(f'Succesfully loaded bathymetry data ({saveFile}) near ({Latitude:.3f},{Longitude:.3f}) from ERDDAP server.')
    return data

def retrieveTransect(bathdata,sLat,sLon,eLat,eLon, method='interpolate'):

    def toPixel(coord_latlon):
        latPixel = np.argmin(np.abs(coord_latlon[0]-bathdata.lat))
        lonPixel = np.argmin(np.abs(coord_latlon[1]-bathdata.lon))
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
        transect = bathdata.topo[y,x]
        lat = bathdata.lat[y]
        lon = bathdata.lon[x]
        
    elif method=='interpolate':
        lon = np.linspace(bathdata.lon[startPixelCoord[1]],bathdata.lon[endPixelCoord[1]],num=transLenPixels)
        lat = np.linspace(bathdata.lat[startPixelCoord[0]],bathdata.lat[endPixelCoord[0]],num=transLenPixels)
        transect = snd.map_coordinates(bathdata.topo,[y,x])
    else:
        print(f'Unable to get transect using method {method}.  Method must be "nearest" or "interpolate"')
        return 
    
    r = np.zeros_like(transect)
    
    for i,(lonVal,latVal) in enumerate(zip(lon,lat)):
        r[i] = geod.line_length([startCoord[1],lonVal],[startCoord[0],latVal])
        
    
    return r, transect


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
    
    
    
    
 
    

    
























