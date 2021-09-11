from urllib.request import urlopen

class ingest:

	def __init__(self, station, model, time=None):
		"""
		"""
		# Set instance variables
		self.station = station
		self.model   = model
		self.time    = time

		# Get the data URL
		self.buildURL()

		# Get file data
		print(f'Downlading data from {self.url}')
		self.getFileData()

	def buildURL(self):
		"""
		Creates a data URL for the bufkit files based on station, model and time.
		"""
		dataURL = None

		# Ingest servers
		psuServer = 'http://www.meteo.psu.edu'
		isuServer = 'https://mtarchive.geol.iastate.edu'

		# Get archive request from Iowa State server
		if self.time == None:
			if self.model.upper() == 'GFS':
				url = f'{psuServer}/bufkit/data/{self.model.upper()}/{self.model.lower()}3_{self.station.lower()}.buf'
			else:
				url = f'{psuServer}/bufkit/data/{self.model.upper()}/{self.model.lower()}_{self.station.lower()}.buf'

		# Get real-time request from PSU server when no date is passed
		else:
			url = f'{isuServer}/{self.time.strftime("%Y/%m/%d/bufkit/%H")}/{self.model.lower()}/{self.model.lower()}_{self.station.lower()}.buf'

		self.url = url

	def getFileData(self):
		"""
		Opens URL and reads in each line from the file into a list
		"""
		# Get file data list
		fileData = urlopen(self.url)

		# Remove HTML characters from each line
		fileData = [str(line).replace("b'", "").replace("\\r\\n'", "") for line in fileData]

		self.data = fileData
