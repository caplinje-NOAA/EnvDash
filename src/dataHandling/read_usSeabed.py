# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# data science imports
import pandas as pd
import numpy as np

# project imports

from .geoTools import lineLength, boundingBox






gridfn = 'seabed_latlon.npy'
datapath = 'data/usSeabed'
files = {'default':'US9_ONE.h5','abbreviated':'US9_ONE_ABRV2.h5','native':'US9_ONE_native.h5'}

# load grid out of functional scope to slightly increase performance with higher memory commit
# grid = np.load(f'{datapath}/{gridfn}',allow_pickle=True)
# gridLat,gridLon = grid[0],grid[1]


# vols = [1,2,3,4,5,6,7,8,9,10,11,12]
# Nbounds = np.array([48.00,40.00,35.00,36.00,38.00,37.00,44.00,49.00,20.00,24.00,66.50,75.00])
# Sbounds = np.array([40.00,31.00,24.00,24.00,24.00,32.00,37.00,44.00,16.00,18.00,48.50,66.50])
# Ebounds = np.array([-64.00,-68.00,-78.00,-87.00,-94.00,-114.00,-117.00,-116.00,-64.00,-152.00,-130.00,-130.00])
# Wbounds = np.array([-80.00,-85.00,-87.00,-94.00,-108.00,-126.00,-128.00,-128.00,-68.00,-162.00,-190.00,-190.00])

# def boundedBy(latitude,longitude):
#   boundedIndex = -1
#   for i,(N,S,E,W) in enumerate(zip(Nbounds,Sbounds,Ebounds,Wbounds)):
  
#     if (latitude<N) and (latitude>S):
  
#       if (longitude<E) and (longitude>W):
  
#         boundedIndex = i
#   return boundedIndex

def getDataIndices(gridLat:np.ndarray,gridLon:np.ndarray,latRange:[float],lonRange:[float],cLat:float,cLon:float,num:int=0)->[np.ndarray,np.ndarray]:
    """Uses USONE grid data (lat/lon) to determine data indicies within a box bounded by latRange and lonRange. Indices can be truncated with num. 
    For num>0, the nearest number (num) of indices to the center coordinate (cLat,cLon) will be returned.  The function returns both the data indices
    and their corresponding distances to the center coordinates in meters, sorted by lowest distance. ->[indices,distances]"""
    
    
    # get indices in bounding box
    Latlocs = np.where(np.logical_and(gridLat>latRange[0], gridLat<latRange[1]))
    Lonlocs = np.where(np.logical_and(gridLon>lonRange[0], gridLon<lonRange[1]))
    locs = np.intersect1d(Latlocs,Lonlocs)
    total = len(locs)

    # get distances to data indices
    distances = np.zeros((len(locs),))
    for il,i in enumerate(locs):
        #distances[il] = getLineLength([cLon,gridLon[i]], [cLat,gridLat[i]])
        distances[il] = lineLength(cLat, cLon, gridLat[i], gridLon[i])
      
    
    # sort
    isort = np.argsort(distances)
    distances = distances[isort]
    indices = locs[isort]
    
    if num>0:
        return indices[0:num],distances[0:num], total
    
    else:
        return indices, distances, total


  


def getSubFrame(indices,distances,useFile='abbreviated',appendDistances=True):
    
    fn = f'{datapath}/{files[useFile]}'
    starti = np.min(indices)
    stopi = np.max(indices)
    df = pd.read_hdf(fn,'table',start = starti,stop=stopi+1)
    #df['distance from center (m)'] = distances
    df = df.loc[indices]
    df['distance (m)'] = distances

    return df

def getBoundedData(BB:boundingBox,num,useFile='abbreviated',appendDistances=True):
    """Gets data bounded by latRange and lonRange from USseabed database.  Data is limited by the input num, doing
    so will output the nearest 'num' datapoints. The default file contains all columns but takes considerably longer to load.
    Use the option 'abbreviated' for fast reading. """
    # uncomment for scoped grid, decreases performance but lowers memory commit
    grid = np.load(f'{datapath}/{gridfn}',allow_pickle=True)
    gridLat,gridLon = grid[0],grid[1]
    latRange = [BB.south,BB.north]
    lonRange = [BB.west,BB.east]
    indices, distances, total = getDataIndices(gridLat,gridLon,latRange,lonRange,BB.cLat,BB.cLon,num = num)
    
    if len(indices)==0:
        return None, 0
 
    return getSubFrame(indices,distances,useFile=useFile,appendDistances=appendDistances), total
    
def getMean(df,col):
    vals = df[col].values
    return np.mean(vals[vals>-1])
    
    
# #testing
# start = timeit.default_timer()


    
# lonRange = [-71,-70.5]
# latRange = [40,41]
# cLat,cLon = [40.7514,-70.6089]
# num=200

# df,total = getBoundedData(latRange,lonRange,cLat,cLon,useFile='abbreviated',num=num)
# print(f'Displaying nearest {num} data points out of {total} available.')
# stop = timeit.default_timer()
# total_time = stop - start

# print(f't= {total_time*1000:.2f} ms')


# sand = getMean(df,'Sand')
# mud = getMean(df,'Mud')
# clay = getMean(df,'Clay')

# print('mean values:')
# print(f'Sand: {sand:.1f},  Mud: {mud:.1f}, Clay: {clay:.1f}')

