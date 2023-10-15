""" Main Program for Puzzle Quest Bot"""

import time
import pprint

from detectAndSearch import detect_icons, findTopLeft, findBottomRight, \
      getGrid, searchGrid, detect_turn_indicator, getPqWindowScreenShot, getTemplateImages

from moves import findValidMoves, performMove

def main():
    """
    Main function for the bot.

    This function runs in an infinite loop,
    checking if it is the player's turn.
    If it is, it takes a screenshot of the game window,
    finds the locations of all gems on the board,
    and determines the best move to make.
    It then performs the move.

    """
    icon_templates = getTemplateImages()

    while True:
        screenshot, game_window = getPqWindowScreenShot()  # Capture the screen

        print("Checking if it's your turn")
        if not detect_turn_indicator(screenshot):
            print("Not your turn")
            time.sleep(0.3)
            continue

        print("It's your turn!")
        # need to detect some kind of wait to see if the game board  has settled
        time.sleep(0.5)

        # Capture the screen again for finding gem locations
        screenshot, game_window = getPqWindowScreenShot()
        # get all locations of gems
        allLocations = detect_icons(screenshot, icon_templates, debug=False)

        # find the top left and bottom right of the grid
        topLeft = findTopLeft(allLocations)
        bottomRight = findBottomRight(allLocations)
        if float('inf') in topLeft or float('-inf') in bottomRight:
            print("No gems found")
            time.sleep(1)
            continue

        # builds a grid of the gems
        grid = getGrid(screenshot, topLeft, bottomRight, debug=False)
        # identifies the most likely gem type in each cell
        foundGemArray, locations_in_cells = searchGrid(
            grid, allLocations, screenshot, debug=False)

        # checks each gem , and determines if moving it will result in a match of 3 or more
        moves = findValidMoves(foundGemArray)
        pprint.pprint(moves)

        if moves:
            # if moving a skull is possible, do that over anything else
            movePerformed = False
            for move in moves:
                if move[4] == 'skull.png':
                    print('Found a skull move')
                    performMove(move, locations_in_cells,
                                game_window, debug=False)
                    print("Move performed")
                    time.sleep(0.5)
                    movePerformed = True
                    break

            if not movePerformed:
                print("No skull moves found")
                print(f"Best move: {moves[0]}")
                performMove(moves[0], locations_in_cells,
                            game_window,  debug=False)
                print("Move performed")
                time.sleep(0.5)
        else:
            print("No moves found")
            time.sleep(1)


if __name__ == '__main__':
    main()
