# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 18:18:29 2023

@author: jim
"""
import os.path
import pickle

import numpy as np
import xarray as xr
import pandas as pd

import urllib.request

from .metaDataHandling import metaDataHandler

dataPath = 'data//temp//'
savePrefix = f'{dataPath}woadata'
saveSuffix ='.netcdf'


## These strings are necessary to request the correct files from the ERDAP server
basetimes = ['1986-01-15T17:26:17.131Z','1986-02-15T03:55:20.963Z','1986-03-17T14:24:24.794Z','1986-04-17T00:53:28.625Z',
             '1986-05-17T11:22:32.456Z','1986-06-16T21:51:36.287Z','1986-07-17T08:20:40.119Z','1986-08-16T18:49:43.950Z',
             '1986-09-16T05:18:47.781Z','1986-10-16T15:47:51.612Z','1986-11-16T02:16:55.444Z','1986-12-16T12:45:59.275Z']

monthDict = {'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}


metaData = {'temperature':metaDataHandler('sspt'),'salinity':metaDataHandler('ssps')}


def ds_to_df(ds:xr.Dataset)->pd.DataFrame:
    df = pd.DataFrame(columns=['depth'],data=np.array(ds.depth))
    for lat in ds.lat:
        for lon in ds.lon:
            cname = f'[{lat:.2f},{lon:.2f}]'
            df[cname] = np.array(ds.sel(lat=lat,lon=lon).C)
            
    return df
    
             
def getWOAdata(variable,statistic,month,lonRange,latRange):
    """download single variable file"""
    # check local storage for requested data
    reqMetaData = {'var':variable,'stat':statistic,'month':month,'lon':lonRange,'lat':latRange}
    exists = metaData[variable].isMatch(reqMetaData)
    
    
    host = f'https://www.ncei.noaa.gov/thredds-ocean/ncss/ncei/woa/{variable}/decav/0.25/'
    filename = f'woa18_decav_{variable[0]}{month}_04.nc'
    var = f'{variable[0]}_{statistic}'
    savePath=f'{savePrefix}_{variable[0]}{saveSuffix}'
 
    
    if exists:
        print('Attempting to use local WOA data.')
        return True
    basetime = basetimes[int(month)-1].replace(':','%3A')
     
    query = f'?var={var}&north={latRange[1]:.3f}&west={lonRange[0]:.3f}&east={lonRange[1]:.3f}&south={latRange[0]:.3f}&disableProjSubset=on&horizStride=1&time_start={basetime}&time_end={basetime}&timeStride=1&vertCoord=&accept=netcdf'
    
    fullurl = f'{host}{filename}{query}'
     
    req = urllib.request.urlretrieve(fullurl, savePath)
    metaData[variable].writeMetaData(reqMetaData)
    
    return req

def getWOAgrid(dataset):

  surfTemp = dataset.sel(depth=0.0)
  tlats = []
  tlons = []

  for tlat in surfTemp.lat:
    for tlon in surfTemp.lon:
      if not np.isnan(surfTemp.sel(lon=tlon,lat=tlat).C):
        tlats.append(tlat)
        tlons.append(tlon)

  return [np.array(tlons),np.array(tlats)]

def toDataFrame(dataset):
    
    df = dataset.to_dataframe()
    
    coord = []
    for lat,lon in zip(df.index.get_level_values('lat'),df.index.get_level_values('lon')):
        coord.append(f'[{lat:.3f},{lon:.3f}]')
        
    newdf = pd.DataFrame()
    newdf['Coordinate'] = coord
    newdf['depth'] = df.index.get_level_values('depth')
    newdf['C']=df['C'].values
    
    return newdf.dropna(axis=0,how='any')
    
# def uniqueCoords(df):
    
#     return 

def SS_Mackenzie(T,S,D):

  return 1448.96+4.591*T-5.304e-2*T**2+2.374e-4*T**3+1.340*(S-35)+1.63e-2*D+1.675e-7*D**2-1.025e-2*T*(S-35)-7.139e-13*T*D**3

def retrieveSSprofiles(lonRange,latRange,Month='January',Statistic='mn',as_DataFrame=False):

  
    
    getWOAdata('temperature',Statistic,monthDict[Month],lonRange,latRange)
    getWOAdata('salinity',Statistic,monthDict[Month],lonRange,latRange)
    
    sPath =f'{savePrefix}_s{saveSuffix}'
    tPath =f'{savePrefix}_t{saveSuffix}'
    
    dataset = xr.open_dataset(tPath,decode_times=False)
    temp = dataset.isel(time=0)
    dataset = xr.open_dataset(sPath,decode_times=False)
    sal = dataset.isel(time=0)
    
    ds = xr.merge([temp,sal])
    ds['C'] = SS_Mackenzie(ds.t_mn,ds.s_mn,ds.depth)
    ds = ds.drop_vars(['t_mn','crs','s_mn'])
    if as_DataFrame:
        return toDataFrame(ds)
    else:
        return ds
    
# lat_pnt =40.867922812601805
# lon_pnt = -64.16015625000001
# minutes = 60

# minutes = minutes/2
# lonRange = [lon_pnt-minutes/60,lon_pnt+minutes/60]
# latRange = [lat_pnt-minutes/60,lat_pnt+minutes/60]
 
# ds = retrieveSSprofiles(lonRange,latRange,Month='January',Statistic='mn')    
# df = toDataFrame(ds)
    

    
   
