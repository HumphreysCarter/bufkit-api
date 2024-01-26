import numpy as np
import pandas as pd


def parse_file(file_data, sounding_headers, derived_headers):
    """
    """
    # Parse sounding parameters of BUFR file
    station_headers = ['STID', 'STNM', 'TIME', 'SLAT', 'SLON', 'SELV', 'STIM']
    tmp_str = ''
    record_station_info, record_derived_qty, record_sounding_qty = False, False, False
    station_metadata, derived_data, sounding_data = [], [], []

    for line in file_data:
        # Check for station information
        if record_station_info and line == '':
            # Break values up to only be seperated by one whitespace
            station_info = (tmp_str.replace(' = ', ' '))

            # Split values into list
            station_info = station_info.split(' ')

            # Remove label values
            station_info = [x for x in station_info if x not in station_headers]
            while '' in station_info:
                station_info.remove('')

            # Add to main list
            station_metadata.append(station_info)

            # Reset temp vars
            tmp_str = ''
            record_station_info = False

        if any(var in line for var in station_headers):
            record_station_info = True
            tmp_str += (' ' + line)

        # Check for derived sounding quantities
        if record_derived_qty is True and line == '':
            # Break values up to only be seperated by one whitespace
            derived_qty = (tmp_str.replace(' = ', ' '))

            # Split values into list
            derived_qty = derived_qty.split(' ')

            # Remove non-numeric values
            derived_qty = [x for x in derived_qty if x not in derived_headers]
            while '' in derived_qty:
                derived_qty.remove('')

            # Add to main list
            derived_data.append(derived_qty)

            # Reset temp vars
            tmp_str = ''
            record_derived_qty = False

        if any(var in line for var in derived_headers):
            record_derived_qty = True
            tmp_str += (' ' + line)

        # Check for sounding quantities
        if any(var in line for var in sounding_headers):
            record_sounding_qty = True

        if record_sounding_qty and line == '':
            level_list = []

            # Split data string into values
            data_list = tmp_str.split(' ')

            # Remove empty indices
            while '' in data_list:
                data_list.remove('')

            # Break data up into pressure levels
            for i in range(0, len(data_list), len(sounding_headers)):
                level_list.append(data_list[i:len(sounding_headers) + i])

            # Create Pandas DataFrame
            profile = pd.DataFrame(level_list, columns=sounding_headers, dtype='float64')
            sounding_data.append(profile)

            # Reset temp vars
            tmp_str = ''
            record_sounding_qty = False

        elif record_sounding_qty:
            if not any(var in line for var in sounding_headers):
                tmp_str += (' ' + line)

    # Combine lists into one
    data_array = []
    for i, j, k in zip(station_metadata, derived_data, sounding_data):
        data_array.append(i + j + [k])

    # Create Pandas Dataframe
    df = pd.DataFrame(data_array, columns=(station_headers + derived_headers + ['PROFILE']))

    # Change time to datatime object
    df['TIME'] = pd.to_datetime(df['TIME'], format='%y%m%d/%H%M')

    # Change station ID to int
    df = df.astype({'STNM': 'int64'})

    # Change data to be float64
    float_headers = ['SLAT', 'SLON', 'SELV'] + derived_headers
    df[float_headers] = df[float_headers].astype('float64')

    # Set null values
    df[float_headers] = df[float_headers].replace(-9999.00, np.NaN)

    return df


def read_file(file_data):
    """
    """
    # Create temp data list and record trigger
    tmp_data, SNPARM, STNPRM = [], '', ''
    recordSounding = False

    # Loop over each line in data file
    for line in file_data:

        # Capture sounding parameters headers
        if 'SNPARM' in line:
            SNPARM = line[line.index('=') + 2:].replace(' ', '').split(';')
        if 'STNPRM' in line:
            STNPRM = line[line.index('=') + 2:].replace(' ', '').split(';')

        # Find start of sounding data
        if 'STID' in line:
            recordSounding = True

        # Append data line to temp data list
        if recordSounding:
            tmp_data.append(line)

        # Break out of loop when end key reached
        if 'STN YYMMDD/HHMM' in line:
            break

    return tmp_data, SNPARM, STNPRM


class sounding:

    def __new__(cls, file_data):
        # Create a new instance of the class
        instance = super(sounding, cls)

        # Call the parse method to process the data and set df attribute
        tmp_data, SNPARM, STNPRM = read_file(file_data)
        df = parse_file(tmp_data, SNPARM, STNPRM)

        return df

