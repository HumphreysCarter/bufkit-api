from urllib.request import urlopen


def build_url(station, model, time=None):
    """
    Creates a data URL for the bufkit files based on station, model and time.
    """
    # Ingest servers
    psu_server = 'http://www.meteo.psu.edu'
    isu_server = 'https://mtarchive.geol.iastate.edu'

    # Get real-time request from PSU server when no date is passed
    if time is None:
        if model.upper() == 'GFS':
            url = f'{psu_server}/bufkit/data/{model.upper()}/{model.lower()}3_{station.lower()}.buf'
        else:
            url = f'{psu_server}/bufkit/data/{model.upper()}/{model.lower()}_{station.lower()}.buf'

    # Get archive request from Iowa State server
    else:
        if model.upper() == 'GFS':
            url = f'{isu_server}/{time.strftime("%Y/%m/%d/bufkit/%H")}/{model.lower()}/{model.lower()}3_{station.lower()}.buf'
        else:
            url = f'{isu_server}/{time.strftime("%Y/%m/%d/bufkit/%H")}/{model.lower()}/{model.lower()}_{station.lower()}.buf'

    return url


def get_file(url):
    """
    Opens URL and reads in each line from the file into a list
    """
    # Get file data list
    file_data = urlopen(url)

    # Remove HTML characters from each line
    file_data = [str(line).replace("b'", "").replace("\\r\\n'", "") for line in file_data]

    return file_data


class ingest:

    def __new__(cls, station, model, time=None):
        # Create a new instance of the class
        instance = super(ingest, cls)

        # Get the data URL
        data_url = build_url(station, model, time)

        # Get file data
        print(f'Downloading data from {data_url}')
        file_data = get_file(data_url)

        # Return the file data
        return file_data