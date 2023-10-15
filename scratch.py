import pygetwindow as gw

# Get a list of all open windows
window_list = gw.getAllWindows()

# Print information about each window
for window in window_list:
    if 'puzzle quest' in window.title.lower():
        print(dir(window))
        print("Title:", window.title)
        # print("Class:", window.className)
        print("Geometry:", window.left, window.top, window.width, window.height)
        print("----------")

#['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_getWindowRect', '_hWnd', '_rect', '_setupRectProperties', 'activate', 'area', 'bottom', 'bottomleft', 'bottomright', 'box', 'center', 'centerx', 'centery', 'close', 'height', 'hide', 'isActive', 'isMaximized', 'isMinimized', 'left', 'maximize', 'midbottom', 'midleft', 'midright', 'midtop', 'minimize', 'move', 'moveRel', 'moveTo', 'resize', 'resizeRel', 'resizeTo', 'restore', 'right', 'show', 'size', 'title', 'top', 'topleft', 'topright', 'visible', 'width']