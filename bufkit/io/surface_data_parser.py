import numpy as np
import pandas as pd

class surface:

	def __init__(self, fileData):
		"""
		"""
		# Create temp data list and record trigger
		tmp_data, recordSurface = [], False

		# Loop over each line in data file
		for line in fileData:

			# Find start of surface data section
			if 'STN YYMMDD/HHMM' in line:
				recordSurface=True

			# Write surface data to temporary data string
			if recordSurface and line != '':
				tmp_data.append(line)

			# Break out of loop when end key reached
			elif recordSurface and line == '':
				break

		# Call parser for data list
		self.parse(tmp_data)

	def parse(self, surface_data):
		"""
		"""
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

		self.df = df
