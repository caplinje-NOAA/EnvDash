# -*- coding: utf-8 -*-

# Converts old meta data schema to new list of dictionaries (as found in bathymetry.py adjacent)
CRM_datasets = {'vol1':'noaa_ngdc_5a67_fa8e_35e2',
                'vol10':'noaa_ngdc_c143_8b2d_0582',
                'vol2':'noaa_ngdc_5801_62a2_09a4',
                'vol3':'noaa_ngdc_e25f_55f5_89af',
                'vol4':'noaa_ngdc_56b9_a5a0_4bf0',
                'vol5':'noaa_ngdc_acb1_e79a_30de',
                'vol6':'noaa_ngdc_701c_84cf_3cdf',
                'vol7':'noaa_ngdc_b56c_cc0a_ebe1',
                'vol8':'noaa_ngdc_d632_63b2_0f78',
                'vol9':'noaa_ngdc_1c7c_3132_0eb3',
                'southak':'noaa_ngdc_89d4_f619_3334'
        
                }

vols =    ['vol1','vol2','vol3','vol4', 'vol5', 'vol6', 'vol7', 'vol8','vol9','vol10','southak']
Nbounds = [ 48.00, 40.00, 35.00, 36.00,  38.00,  37.00,  44.00,  49.00, 20.00,  24.00,    66.50]
Sbounds = [ 40.00, 31.00, 24.00, 24.00,  24.00,  32.00,  37.00,  44.00, 16.00,  18.00,    48.50]
Ebounds = [-64.00,-68.00,-78.00,-87.00, -94.00,-114.00,-117.00,-116.00,-64.00,-152.00,  -130.00]
Wbounds = [-80.00,-85.00,-87.00,-94.00,-108.00,-126.00,-128.00,-128.00,-68.00,-162.00,  -190.00]

CRM_host = 'https://upwell.pfeg.noaa.gov/erddap/griddap/'
CRMbathVariable = 'z'

CRM = []

for i,(N,S,E,W) in enumerate(zip(Nbounds,Sbounds,Ebounds,Wbounds)):

    datasetDict = {'dataset_id':CRM_datasets[vols[i]],
                    'server':CRM_host,
                    'bathVar':CRMbathVariable,
                    'resolution':0.008333333333333333,
                    'Nbound':N,
                    'Sbound':S,
                    'Ebound':E,
                    'Wbound':W,
           
                    }
    if vols[i]=='southak':
        datasetDict['lon360']=True
    else:
        datasetDict['lon360']=False

    CRM.append(datasetDict)