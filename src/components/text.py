# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:00:36 2023
bulk text should be kept here for easy modifications
avoid putting small snippets here
@author: jim
"""

# Display text for transect type dropdown options
transect_single = 'Single transect with start/end coordinates'
transect_singleAz = 'Single transect with start coord and azimuth'
transect_multiple = 'mutiple radials'

#### ALERT TEXT ####
no_SSP_alert = 'No WOA data for this time/area, either expand the region or select a different month.'
SSP_success = 'Successfully loaded WOA temperature and sailinity data.'
seabed_success = 'Successfully loaded USGS US Seabed data.'
no_seabed_alert = 'No USGS US Seabed data found in bounding box, select region in US waters.'


folkCodeKey = "Folk Code Key: M = Mud, S = Sand, G = Gravel, parenthesis indicate 'slightly contains', (i.e. (m)G is slightly muddy gravel)"
#### REFERENCES ####
folkCodeRef = "Folk, R.L, Andrews, P.B., and Lewis, D.W., 1970, Detrital sedimentary rock classification and nomenclature for use in New Zealand: New Zealand Journal of Geology and Geophysics, vol. 13:4, p. 937-968. "

usSeabed_meta_url = "https://cmgds.marine.usgs.gov/data/whcmsc/data-release/doi-P9H3LGWM/"
usSeabed_info_url = "https://www.usgs.gov/data/usseabed-offshore-surficial-sediment-database-samples-collected-within-united-states-exclusive"
usSeabed_meta_link_desc= "usSeabed meta data and data set sources can be found here"
usSeabed_reference = "Buczkowski, B.J., Reid, J.A., Schweitzer, P.N., Cross, V.A., and Jenkins, C.J., 2020, usSEABED—Offshore surficial-sediment database for samples collected within the United States Exclusive Economic Zone: U.S. Geological Survey data release, https://doi.org/10.5066/P9H3LGWM."

SRTM_reference = "Tozer, B. , D. T. Sandwell, W. H. F. Smith, C. Olson, J. R. Beale, and P. Wessel, Global bathymetry and topography at 15 arc seconds: SRTM15+, Accepted Earth and Space Science, August 3, 2019."
SRTM_info_url = "https://topex.ucsd.edu/WWW_html/srtm15_plus.html"

CRM_info_url = "https://www.ncei.noaa.gov/products/coastal-relief-model"
CRM_reference = ["NOAA National Centers for Environmental Information. (2023). Coastal Relief Models (CRMs) Vol. 1-5,9,10. NOAA National Centers for Environmental Information. doi: 10.25921/5ZN5-KN44",
                 "National Geophysical Data Center, 2003. U.S. Coastal Relief Model - Southern California. National Geophysical Data Center, NOAA. doi:10.7289/V500001J",
                 "National Geophysical Data Center, 2003. U.S. Coastal Relief Model - Central Pacific. National Geophysical Data Center, NOAA. doi:10.7289/V50Z7152",
                 "National Geophysical Data Center, 2003. U.S. Coastal Relief Model - Northwest Pacific. National Geophysical Data Center, NOAA. doi:10.7289/V5H12ZXJ"
                 ]
           

### coordinate string functions
def coordToStr(lat:float,lon:float,fnStyled=False)->str:
    """Function for convering lat/lon coordinates to string"""
    """Tested agianst FCC calculator"""
    
    if lat>0:
        latDir = 'N'
    else:
        latDir = 'S'
    if lon>0:
        lonDir ='E'
    else :
        lonDir ='W'
        
    if fnStyled:
        lat,lon = abs(lat),abs(lon)
        latmin = round((lat-int(lat))*60.0)
        latdeg = int(lat)
        lonmin = round((lon-int(lon))*60.0)
        londeg = int(lon)
        return f'{latdeg:,}d{latmin:,}m{latDir}{londeg:,}d{lonmin:,}m{lonDir}'
    
    else:
        return f'[{abs(lat):.3f} {latDir}, {abs(lon):.3f} {lonDir}]'
        
def strToCoord(coordstr:str)->[float]:
    """convert string coordinate [lat,lon] to [float]"""
    # test for incorrect (fnStyled) coordinate string
    if coordstr.find('d')>-1:
        return None
    else:
        stringArray = coordstr.strip('[').strip(']').split(',')
        lat = float(stringArray[0])
        lon = float(stringArray[1])
        return [lat,lon]
        
        
folkCodes = {'(g)M': 'Slightly gravelly mud',
 '(g)mS': 'Slightly gravelly muddy sand',
 '(g)sM': 'Slightly gravelly sandy mud',
 '(g)S': 'Slightly gravelly sand',
 'G': 'Gravel',
 'gM': 'Gravelly mud',
 '(s)gM': 'Slightly gravelly mud',
 'gmS': 'Gravelly muddy sand',
 'gsM': 'Gravelly sandy mud',
 'gS': 'Gravelly sand',
 'M': 'Mud',
 'mG': 'Muddy gravel',
 'mS': 'Muddy sand',
 'msG': 'Muddy sandy gravel',
 'S': 'Sand',
 'sG': 'Sandy gravel',
 'sM': 'Sandy mud',
 'zS': 'Silty sand',
 'cS': 'Clayey sand',
 'sZ': 'Sandy silt',
 'sC': 'Sandy clay',
 'Z': 'Silt',
 'C': 'Clay',
 'cZ': 'Clayey silt',
 'czS': 'Clayey silty sand',
 'scZ': 'Sandy clayey silt',
 'szC': 'Sandy silty clay',
 'zC': 'Silty clay',
 '-': 'No folk code'}
 
        
