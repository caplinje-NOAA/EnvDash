# Underwater Acoustic Environment Explorer

## Abstract

This app collects, displays, and handles downloads of environmental data relevant to underwater propagation modeling, and is intended to be a flexible front end to any propagation modeling framework.  Data includes bathymetry, sound speed profiles, and seabed composition. Data calls are supported by the NOAA ERDDAP servers and the USGS usSEABED database. 

### Data Citations

Tozer, B. , D. T. Sandwell, W. H. F. Smith, C. Olson, J. R. Beale, and P. Wessel, Global bathymetry and topography at 15 arc seconds: SRTM15+, Accepted Earth and Space Science, August 3, 2019.

NOAA National Centers for Environmental Information. (2023). Coastal Relief Models (CRMs) Vol. 1-5,9,10. NOAA National Centers for Environmental Information. doi: 10.25921/5ZN5-KN44

Boyer, Tim P.; Garcia, Hernan E.; Locarnini, Ricardo A.; Zweng, Melissa M.; Mishonov, Alexey V.; Reagan, James R.; Weathers, Katharine A.; Baranova, Olga K.; Seidov, Dan; Smolyar, Igor V. (2018). World Ocean Atlas 2018. Temperature and Salinity. NOAA National Centers for Environmental Information. Dataset. https://www.ncei.noaa.gov/archive/accession/NCEI-WOA18. 

Buczkowski, B.J., Reid, J.A., Schweitzer, P.N., Cross, V.A., and Jenkins, C.J., 2020, usSEABED—Offshore surficial-sediment database for samples collected within the United States Exclusive Economic Zone: U.S. Geological Survey data release, https://doi.org/10.5066/P9H3LGWM.

For more information on NOAA ERDDAP:

https://coastwatch.pfeg.noaa.gov/erddap/index.html


## Running the app

Run the following commands and open the local host web address chosen by Dash.

```shell
python ./main.py
```

An example of the expected terminal messages are shown below:

```shell
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```
