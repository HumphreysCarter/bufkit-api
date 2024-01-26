# BUFKIT Data API
A simple Python interface to ingesting and reading BUFKIT BUFR files.

## Installation

### Installing from Source
Install using the latest source code which can be obtained from the GitHub repository, [HumphreysCarter/bufkit-api](https://github.com/HumphreysCarter/bufkit-api). Stable releases can also be downloaded from the  [releases listing](https://github.com/HumphreysCarter/bufkit-api/releases) in the repo.
```
git clone https://github.com/HumphreysCarter/bufkit-api
cd bufkit-api
python setup.py install
```

## Dependencies

### Required
* Python 3.9 or higher
* metpy

## Usage

### IO

Supported data feeds for ingest are the real-time [Penn State Bufkit Data Distribution](http://www.meteo.psu.edu/bufkit/CONUS_NAM_00.html) page and the [Iowa State Mtarchive](https://mtarchive.geol.iastate.edu)

#### Ingesting Data

Online files are read by calling ingest, and passing the ```station``` and ```model``` arguments.

```
from bufkit import ingest

bufr_file = ingest('KFLG', 'GFS')
```

The optional ```time``` argument can also be passed to ingest a file for a given model run time.
```
from bufkit import ingest
from datetime import datetime

bufr_file = ingest('KFLG', 'HRRR', time=datetime(2021, 9, 10, 18)
```

#### Retrieving Data

Data files can be parsed for surface data and/or the upper-air and sounding data.

##### Surface Data

Calling surface and passing the ingested file data parses the file for surface data.
```
from bufkit import surface
surface_data = surface(bufr_file)
```

The ```surface_data``` variable will then return a Pandas DataFrame object.

```
        STN                TIME    PMSL   PRES   SKTC   STC1  EVAP  P03M  C03M  SWEM  LCLD  MCLD  HCLD  UWND  VWND   T2MS  Q2MS  WXTS  WXTP  WXTZ  WXTR  S03M  TD2M
0    723755 2021-09-10 18:00:00  1017.8  782.6  32.54  294.3   6.4   0.0   0.0   0.0   0.0   5.0   3.0  -0.8   3.0  25.14  6.42   0.0   0.0   0.0   1.0   0.0  3.80
1    723755 2021-09-10 19:00:00  1016.5  782.0  33.74  295.2   7.1   0.0   0.0   0.0   0.0   5.0   5.0  -1.5   3.9  26.34  5.93   0.0   0.0   0.0   0.0   0.0  2.67
2    723755 2021-09-10 20:00:00  1015.9  781.6  33.64  296.0   7.3   0.0   0.0   0.0   0.0   5.0   3.0   0.4   5.0  26.74  5.50   0.0   0.0   0.0   0.0   0.0  1.61
3    723755 2021-09-10 21:00:00  1015.8  781.5  32.24  296.6   6.9   0.0   0.0   0.0   0.0   3.0   2.0   2.3   5.5  26.34  5.62   0.0   0.0   0.0   0.0   0.0  1.91
4    723755 2021-09-10 22:00:00  1015.4  781.0  30.74  297.1   6.2   0.0   0.0   0.0   0.0   3.0   1.0   3.1   5.2  25.94  5.45   0.0   0.0   0.0   0.0   0.0  1.47
..      ...                 ...     ...    ...    ...    ...   ...   ...   ...   ...   ...   ...   ...   ...   ...    ...   ...   ...   ...   ...   ...   ...   ...
136  723755 2021-09-17 18:00:00  1014.0  778.8  28.94  291.8   4.6   0.0   0.0   0.0   0.0  21.0   0.0   1.7   6.6  22.94  6.06   0.0   0.0   0.0   1.0   0.0  2.92
137  723755 2021-09-17 21:00:00  1011.9  777.4  29.54  293.9   4.8   0.0   0.0   0.0   0.0  37.0   0.0   3.5   7.7  23.74  6.04   0.0   0.0   0.0   1.0   0.0  2.84
138  723755 2021-09-18 00:00:00  1011.8  776.7  22.54  294.8   2.6   0.0   0.0   0.0   0.0  32.0   0.0   3.7   6.8  21.04  5.99   0.0   0.0   0.0   0.0   0.0  2.71
139  723755 2021-09-18 03:00:00  1015.3  777.3  12.54  293.7   0.2   0.0   0.0   0.0   0.0   5.0   0.0   2.4   0.6  13.54  6.44   0.0   0.0   0.0   1.0   0.0  3.75
140  723755 2021-09-18 06:00:00  1014.6  777.3  16.24  292.3   0.5   0.0   0.0   0.0   1.0  31.0   0.0   2.0   4.1  15.84  5.69   0.0   0.0   0.0   1.0   0.0  2.01

[141 rows x 23 columns]
```

##### Upper-Air and Sounding Data

Calling sounding and passing the ingested file data parses the file for the dervied sounding data as well as the upper-air profile.

```
from bufkit import sounding
sounding_data = sounding(bufr_file)
```

The ```sounding_data``` variable will then return a Pandas DataFrame object.
```
     STID    STNM                TIME   SLAT    SLON    SELV   STIM  SHOW  LIFT  SWET  KINX    LCLP   PWAT  TOTL   CAPE    LCLT   CINS    EQLV    LFCT   BRCH                                            PROFILE
0    KFLG  723755 2021-09-10 18:00:00  35.13 -111.67  2137.0    0.0   NaN  1.67   NaN   NaN  576.73  13.74   NaN  44.53  271.93  -1.02  294.39  578.85   2.36       PRES   TMPC     TMWC    DWPC     THTE    ...
1    KFLG  723755 2021-09-10 19:00:00  35.13 -111.67  2137.0    1.0   NaN  1.89   NaN   NaN  555.80  13.04   NaN  20.87  270.22  -1.05  298.81  557.94   1.85       PRES   TMPC     TMWC    DWPC     THTE    ...
2    KFLG  723755 2021-09-10 20:00:00  35.13 -111.67  2137.0    2.0   NaN  2.13   NaN   NaN  542.62  11.67   NaN   0.00  268.77   0.00     NaN     NaN   0.00       PRES   TMPC     TMWC    DWPC     THTE    ...
3    KFLG  723755 2021-09-10 21:00:00  35.13 -111.67  2137.0    3.0   NaN  2.20   NaN   NaN  547.64  11.23   NaN   0.00  269.23   0.00     NaN     NaN   0.00       PRES   TMPC     TMWC    DWPC     THTE    ...
4    KFLG  723755 2021-09-10 22:00:00  35.13 -111.67  2137.0    4.0   NaN  2.31   NaN   NaN  546.21  11.00   NaN   0.00  268.89   0.00     NaN     NaN   0.00       PRES   TMPC     TMWC    DWPC     THTE    ...
..    ...     ...                 ...    ...     ...     ...    ...   ...   ...   ...   ...     ...    ...   ...    ...     ...    ...     ...     ...    ...                                                ...
135  KFLG  723755 2021-09-17 15:00:00  35.13 -111.67  2137.0  165.0   NaN  0.75   NaN   NaN  611.32  12.20   NaN   0.13  272.25 -65.72  567.58  577.18   0.01       PRES   TMPC     TMWC    DWPC     THTE    ...
136  KFLG  723755 2021-09-17 18:00:00  35.13 -111.67  2137.0  168.0   NaN  0.57   NaN   NaN  586.94  14.90   NaN  39.78  271.65  -1.07  511.46  591.53  14.74       PRES   TMPC     TMWC    DWPC     THTE    ...
137  KFLG  723755 2021-09-17 21:00:00  35.13 -111.67  2137.0  171.0   NaN  1.08   NaN   NaN  577.07  13.28   NaN  43.74  271.30  -1.11  512.94  581.17  26.45       PRES   TMPC     TMWC    DWPC     THTE    ...
138  KFLG  723755 2021-09-18 00:00:00  35.13 -111.67  2137.0  174.0   NaN  1.33   NaN   NaN  591.39  12.65   NaN   0.00  271.80   0.00     NaN     NaN   0.00       PRES   TMPC     TMWC    DWPC     THTE    ...
139  KFLG  723755 2021-09-18 03:00:00  35.13 -111.67  2137.0  177.0   NaN  3.77   NaN   NaN  659.61  13.11   NaN   0.00  274.43   0.00     NaN     NaN   0.00       PRES   TMPC     TMWC    DWPC     THTE    ...

[140 rows x 21 columns]
```

The upper-air profile is returned from the dataframe under the ```PROFILE``` header, returning a list of each profile in time. A DataFrame for each time step in the file can be viewed by calling ```sounding_data.PROFILE[0]```, and incrementing the index based on the desired time step.
```
     PRES   TMPC     TMWC    DWPC     THTE    DRCT   SKNT  OMEG      HGHT
0   782.5  23.54    11.61    3.03   338.09  165.47   5.42 -0.39   2138.12
1   778.5  22.74    11.21    2.79   337.44  164.74   6.65 -0.50   2182.73
2   774.0  22.14    10.90    2.64   337.22  162.55   7.13 -0.56   2233.07
3   769.0  21.54    10.60    2.50   337.09  162.03   7.56 -0.62   2289.24
4   763.4  20.84    10.26    2.38   336.96  161.11   7.81 -0.67   2352.44
..    ...    ...      ...     ...      ...     ...    ...   ...       ...
57    1.3 -12.26  1551.89 -120.08  1738.42  112.29  38.44  0.00  45923.22
58    0.7 -12.96  1552.21 -122.23  2068.79  102.34  25.47  0.00  50644.43
59    0.4 -24.56  1557.62 -124.12  2318.86  129.26  31.63  0.00  54811.69
60    0.2 -38.26  1564.00 -126.37  2670.36  153.26  28.95 -0.00  59716.65
61    0.1 -61.26  1574.71 -128.54  2935.84   69.89  14.70  0.00  64249.30

[62 rows x 9 columns]
```

### Utilities

#### Unit Retrieval
Units of any variable in the data files can be retrieved from the ```bufkit.util.units``` class. The value returned is a MetPy unit object. Unit key is based on http://www.meteo.psu.edu/bufkit/bufkit_parameters.txt.

```
from bufkit.util import units
units('CAPE')
```
Which will output:
```
joule / kilogram
```
