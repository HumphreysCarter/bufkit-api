"""
BUFKIT BUFR (.buf) File Parser
06/30/2020
--------------------------------------------------------------------------------

Copyright (c) 2020, Carter J. Humphreys (chumphre@oswego.edu)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
import pandas as pd
import numpy as np
from metpy.units import units
from urllib.request import urlopen
from datetime import datetime

# Returns the units for BUFR Parameter 
# Based on http://www.meteo.psu.edu/bufkit/bufkit_parameters.txt
def getParameterUnit(parameter):   
    units_key={'slat':units.degrees, 'slon':units.degrees, 'selv':units.meters, 'stim':units.hours, 'show':units.dimensionless, 'lift':units.dimensionless, 'swet':units.dimensionless, 
           'kinx':units.dimensionless, 'lclp':units.hPa, 'pwat':units.mm, 'totl':units.dimensionless, 'cape':(units.joules / units.kg), 'lclt':units.kelvin, 'cins':(units.joules / units.kg), 
           'eqlv':units.hPa, 'lfct':units.hPa, 'brch':units.dimensionless, 'pres':units.hPa, 'tmpc':units.degC, 'tmwc':units.degC, 'dwpc':units.degC, 'thte':units.kelvin, 'drct':units.degrees, 
           'sknt':units.knots, 'omeg':(units.Pa / units.seconds), 'cfrl':units.percent, 'hght':units.meters, 'pmsl':units.hPa, 'pres':units.hPa, 'sktc':units.degC, 'stc1':units.kelvin, 
           'snfl':(units.mm), 'wtns':units.percent, 'p01m':units.mm, 'c01m':units.mm, 'stc2':units.kelvin, 'lcld':units.percent, 'mcld':units.percent, 'hcld':units.percent, 'snra':units.percent,
           'uwnd':(units.meter / units.seconds), 'vwnd':(units.meter / units.seconds), 'r01m':units.mm, 'bfgr':units.mm, 't2ms':units.degC, 'q2ms':units.dimensionless, 'wxts':units.dimensionless,
           'wxtp':units.dimensionless, 'wxtz':units.dimensionless, 'wxtr':units.dimensionless, 'ustm':(units.meter / units.seconds), 'vstm':(units.meter / units.seconds), 
           'hlcy':((units.meter * units.meter ) / (units.seconds * units.seconds)), 'sllh':units.mm, 'wsym':units.dimensionless, 'cdbp':units.hPa, 'vsbk':units.km, 'td2m':units.degC}
    
    try:
        return units_key[parameter.lower()]
    except:
        return None    

    
# Reterive data URL based on input parameters
def getBUFR_URL(station, model, run=None):
    dataURL=None
    
    # BUFKIT file servers
    psuServer='http://www.meteo.psu.edu'
    isuServer='https://mtarchive.geol.iastate.edu'
    
    # Get file URL based on request type (archived or latest)
    if run==None:
        if model.upper() == "GFS":
             dataURL=f'{psuServer}/bufkit/data/{model.upper()}/{model.lower()}3_{station.lower()}.buf'
        else:
            dataURL=f'{psuServer}/bufkit/data/{model.upper()}/{model.lower()}_{station.lower()}.buf'
    else:
        dataURL=f'{isuServer}/{run.strftime("%Y/%m/%d/bufkit/%H")}/{model.lower()}/{model.lower()}_{station.lower()}.buf'  
        
    print(f'Downlading data from {dataURL}')
    return dataURL

# Parse sounding parameters of BUFR file
def parseSoundingParameters(file_data, sounding_headers, derived_headers):
    station_headers=['STID', 'STNM', 'TIME', 'SLAT', 'SLON', 'SELV', 'STIM']
    tmp_str=''
    recordStationInfo, recordDerivedQty, recordSoundingQty = False, False, False
    station_metadata, derived_data, sounding_data = [], [], []
    
    for line in file_data:
        
        # Check for station infromation
        if recordStationInfo and line=='':
            # Break values up to only be seperated by one whitespace
            station_info=(tmp_str.replace(' = ', ' '))
            
            # Split values into list
            station_info=station_info.split(' ')
            
            # Remove label values
            station_info=[x for x in station_info if x not in station_headers]
            while '' in station_info:
                station_info.remove('')
            
            # Add to main list
            station_metadata.append(station_info)
            
            # Reset temp vars
            tmp_str=''
            recordStationInfo=False
    
        if any(var in line for var in station_headers):
            recordStationInfo=True
            tmp_str+=(' ' + line)
        
        # Check for derived sounding quantities
        if recordDerivedQty==True and line=='':
            # Break values up to only be seperated by one whitespace
            derived_qty=(tmp_str.replace(' = ', ' '))
            
            # Split values into list
            derived_qty=derived_qty.split(' ')
            
            # Remove non-numeric values
            derived_qty=[x for x in derived_qty if x not in derived_headers]
            while '' in derived_qty:
                derived_qty.remove('')

            # Add to main list
            derived_data.append(derived_qty)
            
            # Reset temp vars
            tmp_str=''
            recordDerivedQty=False
                   
        if any(var in line for var in derived_headers):
            recordDerivedQty=True
            tmp_str+=(' ' + line)
            
        # Check for sounding quantities
        if any(var in line for var in sounding_headers):
            recordSoundingQty=True
            
        if recordSoundingQty and line=='':
            level_list=[]
            
            # Split data string into values
            data_list=tmp_str.split(' ')
            
            # Remove empty indices
            while '' in data_list:
                data_list.remove('')
            
            # Break data up into pressure levels
            for i in range(0, len(data_list), len(sounding_headers)):
                 level_list.append(data_list[i:len(sounding_headers)+i])
            
            # Create Pandas DataFrame
            profile=pd.DataFrame(level_list, columns=sounding_headers, dtype='float64')
            sounding_data.append(profile)
            
            # Reset temp vars
            tmp_str=''
            recordSoundingQty=False
            
        elif recordSoundingQty:
            if any(var in line for var in sounding_headers)==False:
                tmp_str+=(' ' + line)
               
    # Combine lists into one
    dataArray=[]
    for i, j, k in zip(station_metadata, derived_data, sounding_data):
        dataArray.append(i+j+[k])
                
    # Create Pandas Dataframe
    df=pd.DataFrame(dataArray, columns=(station_headers+derived_headers+['PROFILE']), dtype='float64')
    
    # Change time to datatime object
    df['TIME']=pd.to_datetime(df['TIME'], format='%y%m%d/%H%M') 
    
    # Change station ID to int
    df=df.astype({'STNM': 'int64'})
    
    # Set null values
    df=df.replace(-9999.00, np.NaN)
        
    return df

# Parse surface parameters of BUFR file
def parseSurfaceParameters(surface_data):
    dataArray, tmp_str = [], ''
    
    for line in surface_data:
        # Break for new section
        if '/' in line:
            dataArray.append(tmp_str.split(' '))
            tmp_str=line
        # Append current section
        else:
            tmp_str+=(' ' + line)
    
    # Capture last section
    dataArray.append(tmp_str.split(' '))
    
    # Get headers from dataarray
    headers=dataArray.pop(1)
    
    # Change YYMMDD/HHMM header to TIME
    i=headers.index('YYMMDD/HHMM')
    headers[i]='TIME'
    
    # Remove empty row
    dataArray.remove([''])
    
    # Create Pandas Dataframe
    df=pd.DataFrame(dataArray, columns=headers, dtype='float64')
    
    # Change time to datatime object
    df['TIME']=pd.to_datetime(df['TIME'], format='%y%m%d/%H%M') 
    
    # Change station ID to int
    df=df.astype({'STN': 'int64'})
    
    # Set null values
    df=df.replace(-9999.00, np.NaN)
   
    return df
        
# Read BUFR file
def parseBUFR_file(dataURL, getSoundingParameters=True, getSurfaceParameters=True):
    
    # BUFR data var
    BUFR_Data={}
    
    # Close parser if both parameters set to false
    if parseSoundingParameters==False and parseSurfaceParameters==False:
        return None
    
    # Open BUFR file
    fileData = urlopen(dataURL)
    
    tmp_data, SNPARM, STNPRM = [], '', ''
    recordSounding, recordSurface = False, False
    
    # Read each line from BUFR file
    for line in fileData:
        
        # Remove HTML data
        line = str(line).replace("b'", "").replace("\\r\\n'", "")
        
        # Capture sounding parameters
        if getSoundingParameters:
            # Capture sounding parameters headers
            if 'SNPARM' in line:
                SNPARM=line[line.index('=')+2:].replace(' ', '').split(';')
            if 'STNPRM' in line:
                STNPRM=line[line.index('=')+2:].replace(' ', '').split(';')
                
            if 'STID' in line:
                recordSounding=True
            
            if 'STN YYMMDD/HHMM' in line:
                BUFR_Data['sounding']=parseSoundingParameters(tmp_data, SNPARM, STNPRM)
                recordSounding=False
                tmp_data=[]
                
            if recordSounding:
                tmp_data.append(line)             
            
        # Capture surface data
        if getSurfaceParameters:
            
            if 'STN YYMMDD/HHMM' in line:
                recordSurface=True

            # Write surface data to temporary data string
            if recordSurface and line!='':
                tmp_data.append(line)

            # Send data string to parser when end key reached
            elif recordSurface and line=='':
                BUFR_Data['surface']=parseSurfaceParameters(tmp_data)
                tmp_data=[]

                # End of file, break out of loop
                break
                
    return BUFR_Data

# Main Method
def getBUFR_data(site, model, time=None, sounding=True, surface=True):
    url=getBUFR_URL(site, model, time)
    data=parseBUFR_file(url, sounding, surface)
    return data