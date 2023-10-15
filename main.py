from detectAndSearch import * 

import time
import pyautogui
import pydirectinput
import ctypes, sys
import win32api, win32con
import json
from itertools import groupby

def check_top_left(row, col, foundGemArray, thisGem):
	#check top left
	if row > 0 and col > 0:
		if foundGemArray[row-1,col-1] == thisGem:
			return True
	return False

def check_top_right(row, col, foundGemArray, thisGem):
	#check top right
	if row > 0 and col < len(foundGemArray[0])-1:
		if foundGemArray[row-1,col+1] == thisGem:
			return True
	return False

def check_top_right_right(row, col, foundGemArray, thisGem):
	#check top right
	if row > 0 and col < len(foundGemArray[0])-1:
		if foundGemArray[row-1,col+1] == thisGem:
			return True
	return False

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


def find_valid_moves(foundGemArray, debug=False):
	moves = [] 
	# if all the gems are empty in row 1 then return no moves
	emptyCount = 0
	for x in foundGemArray[0]:
		if x == 'empty':
			emptyCount += 1
	if emptyCount == 7:
		print("no moves, first row all empty")
		return moves
	

	
	for i, row in enumerate(foundGemArray):
		for j, thisGem in enumerate(row):
			# RIGHT 
			if j < 7 :
				futureArray = foundGemArray.copy()
				futureArray[i,j+1] = foundGemArray[i,j]
				futureArray[i,j] = foundGemArray[i,j+1] # swap the two gems
				series_length = get_series_length(futureArray)
				if series_length > 0 :
					# pprint.pprint(futureArray)
					if debug:
						print(f"moving {i},{j} right results in {series_length} ")
					moves.append((i,j,'right', series_length,  thisGem))
			# LEFT
			if j > 0 :
				futureArray = foundGemArray.copy()
				futureArray[i,j-1] = foundGemArray[i,j]
				futureArray[i,j] = foundGemArray[i,j-1]
				series_length = get_series_length(futureArray)
				if series_length > 0 :
					# pprint.pprint(futureArray)
					if debug:
						print(f"moving {i},{j} left results in {series_length} ")
					moves.append((i,j,'left', series_length, thisGem))
			# DOWN
			if i < 7 :
				futureArray = foundGemArray.copy()
				futureArray[i+1,j] = foundGemArray[i,j]
				futureArray[i,j] = foundGemArray[i+1,j]
				series_length = get_series_length(futureArray)
				if series_length > 0 :
					# pprint.pprint(futureArray)
					if debug:
						print(f"moving {i},{j} down results in {series_length} ")
					moves.append((i,j,'down', series_length, thisGem))
			
			
			# UP
			if i > 0 :
				futureArray = foundGemArray.copy()
				futureArray[i-1,j] = thisGem
				futureArray[i,j] = foundGemArray[i-1,j] # swap the two gems
				series_length = get_series_length(futureArray)

				# if i == 2 and j == 5:
				# 	print("UP SKULL HERE")
				# 	pprint.pprint(futureArray)
				# 	# write future array to json file 
				# 	with open('futureArray.json', 'w') as outfile:
				# 		json.dump(futureArray.tolist(), outfile)	


				if series_length > 0 :
					# pprint.pprint(futureArray)
					# pprint.pprint(futureArray)
					# print(f"moving {i},{j} up results in {series_length} ")
					moves.append((i,j,'up', series_length, thisGem))

	

	if len(moves) > 0:
		moves.sort(key=lambda x: (x[3], x[4] == 'skull'), reverse=True) 
		print(f"best move is {moves[0]}")
		print()
	return moves 
				

def get_series_length(futureArray, debug=False):
	rows, cols = len(futureArray), len(futureArray[0])
	series_length = []

	# for rowidx , row in enumerate(futureArray):
	# 	for i in range(cols - 2):
	# 		if row[i] == row[i+1] == row[i+2]:
	# 			series_length = 3
	# 			if i + 3 < cols and row[i+3] == row[i]:
	# 				series_length = 4
	# 			if i + 4 < cols and row[i+4] == row[i]:
	# 				series_length = 5
	# 				break
	# 			if series_length >= 3:
	# 				print(f"found a row series of length  {series_length} in row {rowidx}; ")    
	for row in range(rows):
		thisColumn = list(futureArray[row,:])

		res = {}
		for k, g in groupby(thisColumn):
			res[k]=  len(list(g))
		
		thisSeries = (max(res.values()))
		seriesType = max(res, key=res.get)
		if thisSeries >= 3:
			if debug:
				print(f"found a row series of length {series_length} in row {row}; ")  
			# print (futureArray)
        
		series_length.append(thisSeries)
	


	for col in range(cols):
		thisColumn = list(futureArray[:,col])
		res = {}
		for k, g in groupby(thisColumn):
			res[k]=  len(list(g))
		
		thisSeries  = max(res.values())
		if thisSeries >= 3:
			if debug:
				print(f"found a column series of length  {series_length} in col {col}; ")  
			# print (futureArray)

		series_length.append(thisSeries)
		
	final_series_length = max(series_length)	
	if final_series_length >=3:
		return final_series_length    
	return 0


def makeMoveClicks(pos1, pos2):
	# for some reason this combination of pyautogui and win32api works for clicking in desmume
	pyautogui.click(pos1[0], pos1[1], duration=0.4, button='left')
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

	pyautogui.doubleClick(pos2[0], pos2[1], duration=0.4, button='left')
	# win32api.SetCursorPos(adjusted_above_location)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

def performMove(move, locations_in_cells, game_window, debug=False):
	row, col, direction, seriesCount, gem= move
	offset = 18
	thisLocation = locations_in_cells[row, col]
	adjusted_this_location = (thisLocation[0] + game_window.left + offset, thisLocation[1] + game_window.top + offset)
	
	if direction == 'up':
		upLocation = locations_in_cells[row-1, col]
		target_location = (upLocation[0] + game_window.left + offset, upLocation[1] + game_window.top + offset)
	elif direction == 'down':
		downLocation = locations_in_cells[row+1, col]
		target_location = (downLocation[0] + game_window.left + offset, downLocation[1] + game_window.top + offset)
	elif direction == 'left':
		leftLocation = locations_in_cells[row, col-1]
		target_location = (leftLocation[0] + game_window.left + offset, leftLocation[1] + game_window.top + offset)
	elif direction == 'right':
		rightLocation = locations_in_cells[row, col+1]
		target_location = (rightLocation[0] + game_window.left + offset, rightLocation[1] + game_window.top + offset)

	makeMoveClicks(adjusted_this_location, target_location)
	
	if debug:
		print(f"Moved {thisLocation} to {locals()[direction+'Location']}")



 
def main():
	icon_templates = getTemplateImages()
	
	while True:
		screenshot , game_window = getPqWindowScreenShot()  # Capture the screen

		print ("Checking if it's your turn")
		if not detect_turn_indicator(screenshot):
			print("Not your turn")
			time.sleep(0.3)
			continue
			
		print ("It's your turn!")
		time.sleep(0.5) # need to detect some kind of wait to see if the game board  has settled
		
 
		screenshot , game_window = getPqWindowScreenShot()  # Capture the screen
		allLocations = detect_icons(screenshot,icon_templates, debug=False)
		# allLocations = removeOutliers(allLocations)

		topLeft = findTopLeft(allLocations)
		bottomRight = findBottomRight(allLocations)
		if float('inf') in topLeft or float('-inf') in bottomRight:
			print("No gems found")
			time.sleep(1)
			continue

		grid = getGrid(screenshot , topLeft, bottomRight, debug=False)
		foundGemArray , locations_in_cells = searchGrid(grid, allLocations, screenshot, debug=False)

		#moves = check_moves(foundGemArray)
		moves = find_valid_moves(foundGemArray)
		# print(moves)
		if moves:
			print(f"Best move: {moves[0]}")
			performMove(moves[0], locations_in_cells, game_window,  debug=False)
			print("Move performed")
			time.sleep(0.5)
		else:
			print("No moves found")
			time.sleep(1)


def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False


if __name__ == '__main__':
	if True: # is_admin():
		# Code of your program here
		print("now running in admin mode\n press any key to continue")
		main()
		print('fin')
	else:
		# Re-run the program with admin rights
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
