import sys
import PIL
from PIL import Image, ImageGrab
import cv2

use_grab = True

def screenGrab( rect =[2560, 25, 885, 540] ):
    """ Given a rectangle, return a PIL Image of that part of the screen.
        Handles a Linux installation with and older Pillow by falling-back
        to using XLib """
    global use_grab
    x, y, width, height = rect

    if ( use_grab ):
        image = PIL.ImageGrab.grab( bbox=[ x, y, x+width, y+height ], all_screens = True )

    return image


