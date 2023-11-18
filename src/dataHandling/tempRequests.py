# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 15:09:06 2023
This module handles http requests and treats downloads as temporary files which are deleted after a generic method reads the data
@author: jim
"""

# python imports
import tempfile
from io import BytesIO
import time

# non-standard
import requests

chunk_size_mb = 1
chunk_size = int(1024*1024*chunk_size_mb)
chunk_size=128
    
def getData(request:str,readMethod:callable,**kwargs):
    """Retrieves arbitrary data via http request using a temporary file (deleted during calls to this function).
    Returns the data object and the request object from the requests package. HTTP error handling can be delt with
    via the status code of the returned request (i.e. r.status_code) """
    
    start = time.time()
    # open request
    try:
        r = requests.get(request,stream=True, timeout=10)
    except requests.exceptions.Timeout:
        print(f'server timeout for request: {request}')
        return None, -1
    
    if r.status_code==requests.codes.ok:
        # if request is okay, open tempory file (to be deleted out of scope)
        with tempfile.TemporaryFile() as f:
            # write data
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                f.flush()
                
            # read data structure
            f.seek(0)    
            with BytesIO(f.read()) as readFile:
                output = readMethod(readFile,**kwargs)
            
    else:
        print(f'REQUESTS STATUS CODE: {r.status_code}:{r.reason}:{r.text}')
        output=None
    elapsed = time.time()-start
    print(f'download time = {elapsed:.2f} seconds')
        
    return output
    

    
        
    
    
    
    