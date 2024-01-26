import numpy as np
import pandas as pd


def parse_file(surface_data):
    """
    """
    data_array, tmp_str = [], ''

    for line in surface_data:
        # Break for new section
        if '/' in line:
            data_array.append(tmp_str.split(' '))
            tmp_str = line
        # Append current section
        else:
            tmp_str += (' ' + line)

    # Capture last section
    data_array.append(tmp_str.split(' '))

    # Get headers from data array
    headers = data_array.pop(1)

    # Change YYMMDD/HHMM header to TIME
    i = headers.index('YYMMDD/HHMM')
    headers[i] = 'TIME'

    # Remove empty row
    data_array.remove([''])

    # Create Pandas Dataframe
    df = pd.DataFrame(data_array, columns=headers)

    # Change time to datatime object
    df['TIME'] = pd.to_datetime(df['TIME'], format='%y%m%d/%H%M')

    # Change station ID to int
    df = df.astype({'STN': 'int64'})

    # Change data to be float64
    float_headers = headers[2:]
    df[float_headers] = df[float_headers].astype('float64')

    # Set null values
    df[float_headers] = df[float_headers].replace(-9999.00, np.NaN)

    return df


def read_file(file_data):
    # Create temp data list and record trigger
    tmp_data, record_surface = [], False

    # Loop over each line in data file
    for line in file_data:

        # Find start of surface data section
        if 'STN YYMMDD/HHMM' in line:
            record_surface = True

        # Write surface data to temporary data string
        if record_surface and line != '':
            tmp_data.append(line)

        # Break out of loop when end key reached
        elif record_surface and line == '':
            break

    return tmp_data


class surface:

    def __new__(cls, file_data):
        # Create a new instance of the class
        instance = super(surface, cls)

        # Read data from file
        tmp_data = read_file(file_data)

        # Call parser for data list
        df = parse_file(tmp_data)

        # Return the DataFrame object
        return df
