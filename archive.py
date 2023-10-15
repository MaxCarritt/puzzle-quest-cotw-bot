def removeOutliers(allLocations):
	# this was moved to detectAndSearch.py and only uses the bottom half of the screen
	# remove any gems that have y coordinates thate is higher than 200
	newLocations = {}
	for gem_type, locs in allLocations.items():
		new_locs = []
		for loc in locs:
			if loc[1] < 600:
				new_locs.append(loc)
		newLocations[gem_type] = new_locs
	return newLocations

	# # Calculate the average distance between all pairs of locations
	# distances = []
	# for loc1 in allLocations.values():
	# 	for loc2 in allLocations.values():
	# 		if loc1 != loc2:
	# 			distance = math.sqrt((loc1[0][0] - loc2[0][0])**2 + (loc1[0][1] - loc2[0][1])**2)
	# 			distances.append(distance)
	# avg_distance = sum(distances) / len(distances)

	# # Remove locations that are far away from the other gems
	# for gem_type, locs in allLocations.items():
	# 	new_locs = []
	# 	for loc in locs:
	# 		distances = [math.sqrt((loc[0] - other_loc[0])**2 + (loc[1] - other_loc[1])**2) for other_loc in locs]
	# 		avg_distance_for_gem = sum(distances) / len(distances)
	# 		if avg_distance_for_gem < avg_distance * 1.5:
	# 			new_locs.append(loc)
	# 	allLocations[gem_type] = new_locs

	# return allLocations


def check_moves(foundGemArray, debug=False):
	moves = []
	rows, cols = len(foundGemArray), len(foundGemArray[0])
	for row in range(rows):
		for col in range(cols):
			thisGem = foundGemArray[row,col]
			#check if moving a gem up will make a match of 3 or more
			upMove = 0
			if check_top_left(row, col, foundGemArray, thisGem):
				upMove += 1
			if check_top_right(row, col, foundGemArray, thisGem):
				upMove += 1
			# if check_top_right_right(row, col, foundGemArray, thisGem):
			# 	upMove += 1
			if upMove == 2:
				moves.append((row,col,'up', thisGem))
	print(moves)
	return  moves