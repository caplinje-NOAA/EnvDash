# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 15:09:06 2023
This module handles http requests and treats downloads as temporary files which are deleted after a generic method reads the data
@author: jim
"""

# python imports
import tempfile
from io import BytesIO

# non-standard
import requests


    
def getData(request:str,readMethod:callable,**kwargs):
    """Retrieves arbitrary data via http request using a temporary file (deleted during calls to this function).
    Returns the data object and the request object from the requests package. HTTP error handling can be delt with
    via the status code of the returned request (i.e. r.status_code) """
    
    # open request
    r = requests.get(request,stream=True)
    
    if r.status_code==requests.codes.ok:
        # if request is okay, open tempory file (to be deleted out of scope)
        with tempfile.TemporaryFile() as f:
            # write data
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)
                
            # read data structure
            f.seek(0)    
            output = readMethod(BytesIO(f.read()),**kwargs)
            
    else:
        output=None
        
    return output, r
    

    
        
    
    
    
    