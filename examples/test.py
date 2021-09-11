# Ingest data from the server
from bufkit import ingest
file = ingest('KFLG', 'GFS')

# Parse file for surface data
from bufkit import surface
sfc = surface(file.data)
print(sfc.df)

# Parse file for sounding data
from bufkit import sounding
sdg = sounding(file.data)
print(sdg.df)
