"""
his module contains functions for finding valid moves in a 2D array of 
gems and making moves by swapping two adjacent gems. 
The main function is findValidMoves, which takes a 2D array of gems and returns a list of 
tuples representing valid moves that can be made by swapping two adjacent 
gems. 

The module also contains a helper function getSeriesLength, which 
takes a 2D array of integers and returns the length of the longest series 
of consecutive integers in either a row or a column. 

The function makeMoveClicks takes two positions and simulates mouse clicks to 
make a move by swapping two adjacent gems.
"""
from itertools import groupby
import pyautogui
import win32api
import win32con


def findValidMoves(foundGemArray, debug=False):
    """
    Given a 2D array of gems, finds all valid moves that can be made by swapping two adjacent gems.
    A move is considered valid if it results 
    in a series of three or more identical gems in a row or column.
    The function returns a list of tuples, 
    where each tuple represents a valid move and contains the following elements:
    - The row index of the gem being moved
    - The column index of the gem being moved
    - The direction of the move ('up', 'down', 'left', or 'right')
    - The length of the series of identical gems that would result from the move
    - The type of gem being moved (e.g. 'red', 'blue', 'green', 'skull', or 'empty')
    If debug is True, the function prints debug information to the console.
    """
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
            if j < 7:
                futureArray = foundGemArray.copy()
                futureArray[i, j+1] = foundGemArray[i, j]
                futureArray[i, j] = foundGemArray[i, j+1]  # swap the two gems
                series_length = getSeriesLength(futureArray)
                if series_length > 0:
                    # pprint.pprint(futureArray)
                    if debug:
                        print(
                            f"moving {i},{j} right results in {series_length} ")
                    moves.append((i, j, 'right', series_length,  thisGem))
            # LEFT
            if j > 0:
                futureArray = foundGemArray.copy()
                futureArray[i, j-1] = foundGemArray[i, j]
                futureArray[i, j] = foundGemArray[i, j-1]
                series_length = getSeriesLength(futureArray)
                if series_length > 0:
                    # pprint.pprint(futureArray)
                    if debug:
                        print(
                            f"moving {i},{j} left results in {series_length} ")
                    moves.append((i, j, 'left', series_length, thisGem))
            # DOWN
            if i < 7:
                futureArray = foundGemArray.copy()
                futureArray[i+1, j] = foundGemArray[i, j]
                futureArray[i, j] = foundGemArray[i+1, j]
                series_length = getSeriesLength(futureArray)
                if series_length > 0:
                    # pprint.pprint(futureArray)
                    if debug:
                        print(
                            f"moving {i},{j} down results in {series_length} ")
                    moves.append((i, j, 'down', series_length, thisGem))

            # UP
            if i > 0:
                futureArray = foundGemArray.copy()
                futureArray[i-1, j] = thisGem
                futureArray[i, j] = foundGemArray[i-1, j]  # swap the two gems
                series_length = getSeriesLength(futureArray)

                if series_length > 0:
                    # pprint.pprint(futureArray)
                    # pprint.pprint(futureArray)
                    # print(f"moving {i},{j} up results in {series_length} ")
                    moves.append((i, j, 'up', series_length, thisGem))

    if len(moves) > 0:
        moves.sort(key=lambda x: (x[3], x[4] == 'skull'), reverse=True)
        print(f"best move is {moves[0]}")
        print()
    return moves


def getSeriesLength(futureArray, debug=False):
    """
    This function takes a 2D array of integers and 
    returns the length of the longest series of consecutive integers
    in either a row or a column. If there are no series of at least length 3, it returns 0.

    Parameters:
    futureArray (list[list[int]]): A 2D array of integers.
    debug (bool, optional): If True, prints debug information. Defaults to False.

    Returns:
    int: The length of the longest series of consecutive integers in either a row or a column.
    """
    rows, cols = len(futureArray), len(futureArray[0])
    series_length = []
    for row in range(rows):
        thisColumn = list(futureArray[row, :])

        res = {}
        for k, g in groupby(thisColumn):
            res[k] = len(list(g))

        thisSeries = (max(res.values()))
        # seriesType = max(res, key=res.get)
        if thisSeries >= 3:
            if debug:
                print(
                    f"found a row series of length {series_length} in row {row}; ")
            # print (futureArray)

        series_length.append(thisSeries)

    for col in range(cols):
        thisColumn = list(futureArray[:, col])
        res = {}
        for k, g in groupby(thisColumn):
            res[k] = len(list(g))

        thisSeries = max(res.values())
        if thisSeries >= 3:
            if debug:
                print(
                    f"found a column series of length  {series_length} in col {col}; ")
            # print (futureArray)

        series_length.append(thisSeries)

    final_series_length = max(series_length)
    if final_series_length >= 3:
        return final_series_length
    return 0


def makeMoveClicks(pos1, pos2):
    """
    Given two positions, clicks on both to swap gems.
    For some reason, the following combination of 
    pyautogui + win32api functions is necessary to click
    """
    pyautogui.click(pos1[0], pos1[1], duration=0.4, button='left')
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0) # pylint: disable=I1101

    pyautogui.doubleClick(pos2[0], pos2[1], duration=0.4, button='left')
    # win32api.SetCursorPos(adjusted_above_location)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0) # pylint: disable=I1101


def performMove(move, locations_in_cells, game_window, debug=False):
    """
    Given a move, performs the move in the game window.
    """
    row, col, direction, _ , _ = move
    offset = 18
    thisLocation = locations_in_cells[row, col]
    adjusted_this_location = (
        thisLocation[0] + game_window.left + offset, thisLocation[1] + game_window.top + offset)

    if direction == 'up':
        upLocation = locations_in_cells[row-1, col]
        target_location = (
            upLocation[0] + game_window.left + offset, upLocation[1] + game_window.top + offset)
    elif direction == 'down':
        downLocation = locations_in_cells[row+1, col]
        target_location = (downLocation[0] + game_window.left +
                           offset, downLocation[1] + game_window.top + offset)
    elif direction == 'left':
        leftLocation = locations_in_cells[row, col-1]
        target_location = (leftLocation[0] + game_window.left +
                           offset, leftLocation[1] + game_window.top + offset)
    elif direction == 'right':
        rightLocation = locations_in_cells[row, col+1]
        target_location = (rightLocation[0] + game_window.left +
                           offset, rightLocation[1] + game_window.top + offset)

    makeMoveClicks(adjusted_this_location, target_location)

    if debug:
        print(f"Moved {thisLocation} to {locals()[direction+'Location']}")
