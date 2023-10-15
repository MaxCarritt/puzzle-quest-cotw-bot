"""
This module contains functions for 
detecting and searching for icons in the Puzzle Quest game window.

Functions:
- getTemplateImages(): Loads template images from a folder and returns them as a dictionary.
- getPqWindowScreenShot(): Takes a screenshot of the Puzzle Quest game window 
    and returns it along with the window object.
- detect_icons(screen, icon_templates, debug=False): Detects icons 
    in the given screen using the provided icon templates and 
    returns their locations as a dictionary.
- findGrid(debug=False): Finds the grid in the Puzzle Quest game window and returns its location.
"""

import pprint
import os
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui


# Load template images from a folder
def getTemplateImages():
    """
    Loads template images from a folder and returns them as a dictionary.
    """
    template_folder = 'template_images/'
    file_list = os.listdir(template_folder)
    icon_templates = {}
    for image in file_list:  # Replace with your icon names
        template_path = os.path.join(template_folder, image)
        template_image = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        icon_templates[image] = template_image
        # cv2.imshow("Template Image", template_image)
        # cv2.waitKey(0)  # Wait indefinitely for a key event
    return icon_templates


def getPqWindowScreenShot():
    """
    Takes a screenshot of the Puzzle Quest game window and returns it along with the window object.
    """
    game_window = gw.getWindowsWithTitle(
        "Puzzle Quest - Challenge of the Warlords")
    game_window = game_window[0]
    if game_window is not None:
        screenShot = pyautogui.screenshot(region=(
            game_window.left, game_window.top, game_window.width, game_window.height))
        return screenShot, game_window


def detect_icons(screen, icon_templates, debug=False):
    """
    Detects the locations of icons in a given screen image using template matching.

    Args:
        screen: A PIL Image object representing the screen image.
        icon_templates: A dictionary of icon names and corresponding template images.
        debug: A boolean indicating whether to display debug information.

    Returns:
        A dictionary of icon names and corresponding lists of locations where they were found.
    """

    screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    hsv_image = cv2.cvtColor(screen_np, cv2.COLOR_BGR2HSV)

    # color_mask = cv2.inRange(screen_np, lower_bound, upper_bound)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

    # Create separate masks for each color component
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Combine the individual masks to create an RGB color mask
    color_mask = cv2.merge((blue_mask, green_mask, red_mask))

    # print("Color Mask:", color_mask.shape, color_mask.dtype)

    color_mask = screen_np

    # cv2.imshow("color_mask", screen_np)
    # cv2.destroyAllWindows()

    allLocations = {}
    # Loop through the template images and perform template matching
    for icon_name, template_image in icon_templates.items():
        # print(icon_name)
        # print("Template:", template_image.shape, template_image.dtype)
        template_image = cv2.cvtColor(template_image, cv2.COLOR_RGBA2RGB)
        # template_image = cv2.cvtColor(template_image, cv2.COLOR_RGB2HSV)
        # template_image  = cv2.inRange(template_image, lower_bound, upper_bound)

        if color_mask.dtype != np.uint8:
            color_mask = color_mask.astype(np.uint8)
        if template_image.dtype != np.uint8:
            template_image = template_image.astype(np.uint8)

        # template_image = cv2.cvtColor(template_image, cv2.COLOR_BGR2RGB)
        # cv2.imshow("Template Image", template_image)
        # cv2.waitKey(0)  # Wait indefinitely for a key event
        # cv2.destroyAllWindows()

        result = cv2.matchTemplate(
            color_mask, template_image, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8  # Adjust as needed

        # Find locations where the match exceeds the threshold
        locations = np.where(result >= threshold)

        # get half of the game height
        topHalf = screen_np.shape[0] / 2
        # Loop through all detected matches
        for loc in zip(*locations[::-1]):
            # Get the position of the detected icon and its dimensions
            top_left = loc
            # h, w = template_image.shape[:2]
            # bottom_right = (top_left[0] + w, top_left[1] + h)

            if top_left[1] < topHalf:
                continue
            # # Draw a rectangle around the detected icon
            # cv2.rectangle(screen_np, top_left, bottom_right, (0, 255, 0), 2)
            # # Print the detected icon's name
            # cv2.putText(screen_np, icon_name, (top_left[0], top_left[1] - 10)\
            #   , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # cv2.imshow("Icon Detection", screen_np)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            if icon_name not in allLocations:
                allLocations[icon_name] = []
            allLocations[icon_name].append(loc)

        # cv2.imshow("Icon Detection", screen_np)
        # cv2.waitKey(0)
    if debug:
        # Display the result image with rectangles around detected icons
        cv2.imshow("Icon Detection", screen_np)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # write allLocations to a file
    with open('allLocations.txt', 'w', encoding="utf-8") as f:
        f.write(pprint.pformat(allLocations))

    return allLocations


def findGrid(debug=False):
    """
    Finds the grid in the screenshot of the game window and highlights it with a red rectangle.

    Args:
        debug (bool, optional): If True, displays the screenshot 
        with the detected grid. Defaults to False.

    Returns:
        None
    """
    gameScreen = getPqWindowScreenShot()
    gameScreen = cv2.cvtColor(np.array(gameScreen), cv2.COLOR_RGB2BGR)
    gameScreen = cv2.cvtColor(gameScreen, cv2.COLOR_BGR2GRAY)

    grid_example = cv2.imread('.\\misc_images\\grid_example.png', cv2.IMREAD_UNCHANGED)
    grid_example = cv2.cvtColor(grid_example, cv2.COLOR_BGR2GRAY)
    grid_example = grid_example.astype(gameScreen.dtype)

    # match grid_example to gameScreen
    result = cv2.matchTemplate(gameScreen, grid_example, cv2.TM_CCOEFF_NORMED)
    threshold = 0.1  # Adjust as needed
    locations = np.where(result >= threshold)

    h, w = grid_example.shape[:2]
    for pt in zip(*locations[::-1]):
        cv2.rectangle(gameScreen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    if debug:
        # Show the screenshot with the detected icons
        cv2.imshow('Detected Icons', gameScreen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def findTopLeft(allLocations):
    """ 
    find the top left of the grid 
    returns -inf if no gems are found
    """
    min_x, min_y = float('inf'), float('inf')

    for loc in allLocations.values():
        for x, y in loc:
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y

    # print(f"Top-left coordinate: ({min_x}, {min_y})")
    # TODO: this should be more dynamic, will break at differnt size  # pylint: disable=fixme
    return (min_x - 20, min_y - 10)


def findBottomRight(allLocations):
    """" 
    find the bottom right of the grid 
    returns -inf if no gems are found
    """
    max_x, max_y = float('-inf'), float('-inf')

    for loc in allLocations.values():
        for x, y in loc:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
    max_x += 40
    max_y += 40
    # print(f"Bottom-right coordinate: ({max_x}, {max_y})")
    # TODO: this should be more dynamic, will break at differnt size # pylint: disable=fixme
    return (max_x + 10, max_y+10)


def getGrid(gameScreen, topLeft, bottomRight, debug=False):
    """
    Divides the given game screen into a grid of 8x8 cells, and returns a list of cell ranges.
    
    Parameters:
    gameScreen (PIL.Image.Image): The game screen to divide into a grid.
    topLeft (tuple): The (x, y) coordinates of the top-left corner of the grid.
    bottomRight (tuple): The (x, y) coordinates of the bottom-right corner of the grid.
    debug (bool, optional): Whether to show debug information. Defaults to False.
    
    Returns:
    list: A list of tuples, where each tuple represents a cell range in the format (x1, y1, x2, y2).
    """

    # calculate the width and height of each grid cell
    cellWidth = (bottomRight[0] - topLeft[0]) // 8
    cellHeight = (bottomRight[1] - topLeft[1]) // 8

    # create a list of grid cell ranges
    cellRanges = []
    for j in range(8):
        for i in range(8):
            x1 = topLeft[0] + i * cellWidth
            y1 = topLeft[1] + j * cellHeight
            x2 = x1 + cellWidth
            y2 = y1 + cellHeight
            cellRanges.append((x1, y1, x2, y2))

    # draw the cell ranges on the game screen
    screen_np = cv2.cvtColor(np.array(gameScreen), cv2.COLOR_RGB2BGR)
    # hsv_image = cv2.cvtColor(screenscreen_np_np, cv2.COLOR_BGR2HSV)
    for cellRange in cellRanges:
        cv2.rectangle(screen_np, (cellRange[0], cellRange[1]),
                      (cellRange[2], cellRange[3]), (0, 255, 0), 2)
        if debug:
            cv2.imshow('Cell Ranges', screen_np)
            cv2.waitKey(1)
            cv2.destroyAllWindows()

    # show the screenshot with the cell ranges
    if debug:
        cv2.imshow('Cell Ranges', screen_np)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return cellRanges


def searchGrid(grid, allLocations, gameScreen, debug=False):
    """
    Searches for gems in a grid of cells on the game screen.

    Args:
        grid (list): A list of tuples representing the cell ranges to search for gems in.
        allLocations (dict): A dictionary containing the locations of all gems on the game screen.
        gameScreen (PIL.Image.Image): A screenshot of the game screen.
        debug (bool, optional): Whether to print debug information 
            and show visualizations. Defaults to False.

    Returns:
        tuple: A tuple containing two numpy arrays. 
            The first array contains the most common gem in each cell of the grid, 
            or 'empty' if the cell is empty. The second array contains the locations 
            of each cell in the grid.
    """

    gems_in_cells = []
    location_in_cells = []
    for cellRange in grid:
        gems_in_cell = []
        gem_locations = [(gem, loc) for gem in allLocations.keys()
                         for loc in allLocations[gem]]
        for gem, loc in gem_locations:
            if loc[0] > cellRange[0] \
                and loc[0] < cellRange[2] \
                and loc[1] > cellRange[1] \
                and loc[1] < cellRange[3]:
                gems_in_cell.append(gem)

        # pick the most common gem in the cell
        if gems_in_cell:
            most_common_gem = max(set(gems_in_cell), key=gems_in_cell.count)
            gems_in_cells.append(most_common_gem)
            location_in_cells.append(cellRange)

            if debug:
                for gem in gems_in_cell:
                    if gem != most_common_gem:
                        print("BAD GEM found here: " + gem)

            # show the cellRange with the most common gem
            screen_np = cv2.cvtColor(np.array(gameScreen), cv2.COLOR_RGB2BGR)
            cv2.rectangle(
                screen_np, (cellRange[0], cellRange[1]), \
                    (cellRange[2], cellRange[3]), (0, 255, 0), 2)

            # put a label of the gam on the rectangle
            # cv2.putText(screen_np, most_common_gem, \
            #   (cellRange[0], cellRange[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # cv2.imshow('Cell Ranges', screen_np)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        else:
            gems_in_cells.append('empty')
            location_in_cells.append(cellRange)

    # row = []
    # for i in range(8):
    # 	row = gems_in_cells[i*8:i*8+8]
    # 	print(row)

    # make a 8x8 array
    foundGems = np.array(gems_in_cells).reshape(8, 8)
    foundGems = foundGems[max(0, -len(foundGems)):,
                          max(0, -len(foundGems[0])):]

    print("searchGrid complete, new gem locations found")

    if debug:
        for row in foundGems:
            print(row)
        print()

    # turn 64 cell locations into 8x8 array
    locations_in_cells = np.array(location_in_cells).reshape(8, 8, 4) # pylint: disable=E1121

    return foundGems, locations_in_cells


def detect_turn_indicator(screenshot):
    """
    Detects a turn indicator icon in a given screenshot using template matching.
    The function takes a screenshot as input and returns a boolean value indicating
    whether the turn indicator icon was found in the screenshot or not.

    Parameters:
    screenshot (PIL.Image): A screenshot image in RGB format.

    Returns:
    bool: True if the turn indicator icon was found in the screenshot, False otherwise.
    """

    screen_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    hsv_image = cv2.cvtColor(screen_np, cv2.COLOR_BGR2HSV)

    # color_mask = cv2.inRange(screen_np, lower_bound, upper_bound)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])

    # Create separate masks for each color component
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Combine the individual masks to create an RGB color mask
    color_mask = cv2.merge((blue_mask, green_mask, red_mask))

    color_mask = screen_np

    if color_mask.dtype != np.uint8:
        color_mask = color_mask.astype(np.uint8)

    template_image = cv2.imread(
        './misc_images/turn_indicator.png', cv2.IMREAD_UNCHANGED)
    template_image = cv2.cvtColor(template_image, cv2.COLOR_RGBA2RGB)

    if template_image.dtype != np.uint8:
        template_image = template_image.astype(np.uint8)

    # cv2.imshow("Screenshot with template", template_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows

    # if screenshot_gray.dtype != np.uint8:
    # 	screenshot_gray = screenshot_gray.astype(np.uint8)
    # if template.dtype != np.uint8:
    # 	template = template.astype(np.uint8)

    # Define the range of angles to rotate the template image
    angles = np.arange(-5, 5, 1)

    found = False
    # Loop over the angles and rotate the template image
    for angle in angles:
        rotated_template = cv2.rotate(template_image, cv2.ROTATE_90_CLOCKWISE)
        rotated_template = cv2.rotate(
            rotated_template, cv2.ROTATE_90_CLOCKWISE)
        rotated_template = cv2.rotate(
            rotated_template, cv2.ROTATE_90_CLOCKWISE)
        rotated_template = cv2.rotate(rotated_template, angle)

        # Perform template matching
        result = cv2.matchTemplate(
            color_mask, template_image, cv2.TM_CCOEFF_NORMED)

        # Check if the template was found
        threshold = 0.3
        locations = np.where(result >= threshold)

        # Loop through all detected matches
        for loc in zip(*locations[::-1]):
            # only show locations in top left quadrant
            if loc[0] < color_mask.shape[1] / 2 and loc[1] < color_mask.shape[0] / 2:
                # Get the position of the detected icon and its dimensions
                top_left = loc
                h, w = template_image.shape[:2]
                bottom_right = (top_left[0] + w, top_left[1] + h)

                # Draw a rectangle around the detected icon
                cv2.rectangle(screen_np, top_left,
                              bottom_right, (0, 255, 0), 2)
                # Print the detected icon's name
                cv2.putText(screen_np, 'found', (
                    top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                found = True
    # cv2.imshow("Icon Detection", screen_np)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return found
