# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 08:10:46 2023

@author: jim
"""

import xarray as xr

y = xr.DataArray(

    [[20, 5], [7, 13]],

    dims=("lat", "lon"),

    coords={"lat": [35.0, 42.0], "lon": [100.0, 120.0]},

)

ds = y.to_dataset(name = 'y')