import json
import numpy as np

def get_series_length(futureArray):
	rows, cols = len(futureArray), len(futureArray[0])
	series_length = 0

	for rowidx , row in enumerate(futureArray):
		for i in range(cols - 2):
			if row[i] == row[i+1] == row[i+2]:
				series_length = 3
				if i + 3 < cols and row[i+3] == row[i]:
					series_length = 4
				if i + 4 < cols and row[i+4] == row[i]:
					series_length = 5
					break
				if series_length >= 3:
					print(f"found a row series of length  {series_length} in row {rowidx}; ")    
	rowSeriesLength = series_length                 

	series_length = 0		
	for col in range(cols):
		for i in range(rows - 2):
			if futureArray[i,col] == futureArray[i+1,col] == futureArray[i+2,col]:
				series_length = 3
				if i + 3 < rows and futureArray[i+3,col] == futureArray[i,col]:
					series_length = 4
				if i + 4 < rows and futureArray[i+4,col] == futureArray[i,col]:
					series_length = 5
					break
				if series_length >= 3:
					print(f"found a horizontal series of length  {series_length} in col {i}")  
	colSeriesLength = series_length

	if rowSeriesLength > colSeriesLength:
		series_length = rowSeriesLength
	else:
		series_length = colSeriesLength
		

	if series_length >=3:
		return series_length    
	return 0



# get future array from json file
def get_future_array():
	with open('futureArray.json') as json_file:
		data = json.load(json_file)
		futureArray = np.array(data)
	return futureArray

# futureArray = get_future_array()
# print(futureArray)
# print(get_series_length(futureArray))




def get_series_length_bad(futureArray):
	rows, cols = len(futureArray), len(futureArray[0])
	series_length = 0

	# Check for horizontal series
	for row in range(rows):
		for col in range(cols - 2):
			if futureArray[row][col] == futureArray[row][col+1] == futureArray[row][col+2]:
				series_length += 1
				for k in range(col+3, cols):
					if futureArray[row][col] == futureArray[row][k]:
						series_length += 1
					else:
						break
				if series_length >= 3:
					return series_length

	# Check for vertical series
	for col in range(cols):
		for row in range(rows - 2):
			if futureArray[row][col] == futureArray[row+1][col] == futureArray[row+2][col]:
				series_length += 1
				for k in range(row+3, rows):
					if futureArray[row][col] == futureArray[k][col]:
						series_length += 1
					else:
						break
				if series_length >= 3:
					return series_length
	if series_length >= 3:
		# print("found a series of length ", series_length)
		return series_length
	return 0

