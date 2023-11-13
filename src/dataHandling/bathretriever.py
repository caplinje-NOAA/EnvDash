# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:49:56 2023
Module for retrieving, loading, and managing bathymetric data from the CRM and SRTM models
@author: jim
"""

# python imports

# data science imports
import numpy as np
from dataclasses import dataclass
import scipy.io

# project imports

from .geoTools import boundingBox
from . import  tempRequests



# !! coupling warning: modifying bathdata class may break many modules
@dataclass
class bathdata:
    lat:np.ndarray
    lon:np.ndarray
    topo: np.ndarray
    error:str
    def summary(self):
        return f'size={np.shape(self.topo)},mean depth = {np.mean(np.mean(self.topo))}'
    

def unpackData(matdata,structname,variable, downSample,landMask=10.0,downCast=False):
    """Load local .mat data structure and return bathdata object"""

    
    #mat = loadmat(path)
    
    data = matdata[structname]
    lat = np.squeeze(data['latitude'][0][0])
    lon = np.squeeze(data['longitude'][0][0])
    topo = data[variable][0][0]

    print(f'data type:{topo.dtype}')
    if downSample:
        print(f'downsampling to {downSample} pixels from {len(lat)} points')
        skip = int(len(lat)/downSample)
        if skip==0:
            skip=1
        print(topo.dtype)
        topo = topo[::skip,::skip]
        lat = lat[::skip]
        lon = lon[::skip]
    if downCast:
        topo = topo.astype(np.float16)
    topo[topo>1]=landMask
    print(f'new data type:{topo.dtype}')
    return bathdata(lat=lat,lon=lon,topo=topo,error=None)
   

def retrieve(BB:boundingBox, DataSet='SRTM',downSample=None, downCast=False)->bathdata:
    """ perform http request and download bath data"""
           
    lonRange = [BB.west,BB.east]
    latRange = [BB.south,BB.north]    
    
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
    
      bounds = boundedBy(BB.cLat, BB.cLon)
    
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
    


    # test if range is outside of dataset and set bounds accordingly if so
    if lonRange[0]<lonRangeData[0]:
      lonRange[0] = lonRangeData[0]
    if lonRange[1]>lonRangeData[1]:
      lonRange[1] = lonRangeData[1]
    
    if latRange[0]<latRangeData[0]:
      latRange[0] = latRangeData[0]
    if latRange[1]>latRangeData[1]:
      latRange[1] = latRangeData[1]
    

    
    query = f'?{variable}%5B({latRange[1]:.4f}):1:({latRange[0]:.4f})%5D%5B({lonRange[0]:.4f}):1:({lonRange[1]:.4f})%5D'
    fullurl = f'{host}{filename}{query}'

  
    matdata,r = tempRequests.getData(fullurl, scipy.io.loadmat)
    
    # request error handling 
    if r.status_code == 404:
        return bathdata(lat=None,lon=None,topo=None,error='ERDDAP Server Temporarily Unavailable.')
    else:
        r.raise_for_status()
 
    data = unpackData(matdata, structname, variable, downSample)

    print(f'Succesfully loaded {DataSet} bathymetry data near ({BB.cLat:.3f},{BB.cLon:.3f}) from ERDDAP server.')
    return data





    
    
    
    
 
    

    
























