import win32gui
from PIL import ImageGrab

import config

def screenGrab( rect = config.bounds ):
    x, y, width, height = rect
    image = ImageGrab.grab( bbox=[ x, y, x + width, y + height ], all_screens = True )

    return image

def screenshot(window_title=None):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

            im = ImageGrab.grab(bbox = [x, y, x+x1, y+y1], all_screens=True)
            
            return im
        else:
            print('Window not found!')
    else:
        print('No window input to search for.')

