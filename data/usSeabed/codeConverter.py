# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:14:15 2023

@author: jim
"""

def getField(line):
    loc = line.find(':')+1
    return line[loc:].strip()

with open('folkCodes.txt') as f:
    keys = []
    values = []
    line = f.readline()
    while line:
        if line.find('Enumerated_Domain_Value:')>-1:
            loc = line.find(':')+1
            keys.append(getField(line))
            
        if line.find('Enumerated_Domain_Value_Definition:')>-1:
            loc = line.find(':')+1
            values.append(getField(line))
            
        line = f.readline()
            
        
            
codes = {key:val for key,val in zip(keys,values)}