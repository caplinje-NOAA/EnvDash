# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 08:44:24 2023
Small module for tracking the metadata of local data
@author: jim
"""

import pickle

tempPath = 'data/temp/'

class metaDataHandler:
    
    def __init__(self,name):
        
        self.path = f'{tempPath}{name}_metaData.pkl'
        
    def isMatch(self,reqMetaData:dict)->bool:
        
        #attempt to open existing file
        try:
            with open(self.path,'rb') as f:
                existing = pickle.load(f)
        # if file doesn't exist, there is no match 
        except FileNotFoundError:
            return False
        # test match of existing data    
        if existing==reqMetaData:
            return True
        else:
            return False               
     
    # could use proper error handling, though I don't know what errors to expect
    def writeMetaData(self,reqMetaData:dict)->None:
            with open(self.path,'wb+') as f:
                pickle.dump(reqMetaData, f)
        
        
        