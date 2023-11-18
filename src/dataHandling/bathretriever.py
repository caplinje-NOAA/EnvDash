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

from .geoTools import boundingBox, toLon360
from . import  tempRequests
from .metaData import bathymetry as bmd



# !! coupling warning: modifying bathdata class may break many modules
@dataclass
class bathdata:
    lat:np.ndarray
    lon:np.ndarray
    topo: np.ndarray
    error:str
    def summary(self):
        return f'size={np.shape(self.topo)},mean depth = {np.mean(np.mean(self.topo))}'
    
def generateRequest(BB:boundingBox, datasetKey='SRTM',stride:int=1,useAltServer:bool=False,ext:str='.mat'):
    
    if type(stride)!=int:
        raise TypeError('bathretriver.generateRequest: stride must be int not {type(stride)}.')
        
    allDatasets = bmd.datasets[datasetKey]
    
    # get bounded dataset
    dataset = None
    for ds in allDatasets:
           if (BB.cLat<ds[bmd.Nbound]) and (BB.cLat>ds[bmd.Sbound]):
               if (BB.cLon<ds[bmd.Ebound]) and (BB.cLon>ds[bmd.Wbound]):
                   dataset = ds
    
    if not dataset:
        print(f'Unable to find dataset which bounds [{BB.cLat:.3f},{BB.cLon:.3f}] for bathymetry source {datasetKey}')
        return None
    
   
    
    # test if range is outside of dataset and set bounds accordingly if so
    if BB.west < dataset[bmd.Wbound]:
      BB.west = dataset[bmd.Wbound]
    if BB.east > dataset[bmd.Ebound]:
      BB.east = dataset[bmd.Ebound]

    if BB.south < dataset[bmd.Sbound]:
      BB.south = dataset[bmd.Sbound]
    if BB.north > dataset[bmd.Nbound]:
      BB.north = dataset[bmd.Nbound]
      
    # convert to lon360 if necessary 
    if dataset[bmd.lon360]:
        BB.east,BB.west = toLon360(BB.east),toLon360(BB.west)
    
    # build query
    query = f'?{dataset[bmd.bathVar]}%5B({BB.south:.4f}):{stride}:({BB.north:.4f})%5D%5B({BB.west:.4f}):{stride}:({BB.east:.4f})%5D'
    
    # if requested, use alt server if available
    if useAltServer:
        if dataset[bmd.altServer]:
            host = dataset[bmd.altServer]
        else:
            raise ValueError('No alt. server given for {dataset[bmd.dataset_id]}')           
    else:
        host = dataset[bmd.server]
        
    request = f'{host}{dataset[bmd.dataset_id]}{ext}{query}'
    
    return request, dataset
        

def unpackData(matdata,structname,variable, landMask=10.0,downCast=False):
    """Load local .mat data structure and return bathdata object"""
    data = matdata[structname]
    lat = np.squeeze(data['latitude'][0][0])
    lon = np.squeeze(data['longitude'][0][0])
    topo = data[variable][0][0]

    if downCast:
        topo = topo.astype(np.float16)
    topo[topo>1]=landMask
    print(f'new data type:{topo.dtype}')
    return bathdata(lat=lat,lon=lon,topo=topo,error=None)
   


def retrieve(BB:boundingBox, DataSet='SRTM',stride=1,downCast=False,returnOnlyRequest=False)->bathdata:
    """ perform http request, read data into bathdata class"""
    
    request, ds = generateRequest(BB,DataSet,stride)
    
    if not request:
        return bathdata(lat=None,lon=None,topo=None,error=f'Unable to find dataset which bounds [{BB.cLat:.3f},{BB.cLon:.3f}] for bathymetry source {DataSet}.')
    if returnOnlyRequest:
        return request
  
    matdata = tempRequests.getData(request, scipy.io.loadmat)
    if not matdata:
        if ds[bmd.altServer]:
            request, ds = generateRequest(BB,DataSet,stride,useAltServer=True)
            matdata = tempRequests.getData(request, scipy.io.loadmat)
            if not matdata:
                return bathdata(lat=None,lon=None,topo=None,error='Communication error with ERDDAP Server, see logs for details.')
            
            
        return bathdata(lat=None,lon=None,topo=None,error='Communication error with ERDDAP Server, see logs for details.')
        
 
    data = unpackData(matdata, ds[bmd.dataset_id], ds[bmd.bathVar])

    print(f'Succesfully loaded {DataSet} bathymetry data near ({BB.cLat:.3f},{BB.cLon:.3f}) from ERDDAP server.')
    return data





    
    
    
    
 
    

    
























