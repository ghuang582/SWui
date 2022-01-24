from re import findall
from PIL import Image
import pytesseract
import numpy as np
import cv2
import re

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

filename = "C:/Users/Admin/Desktop/SWOverlay/Cropped/99custom.png"

def do_ocr(img1):

    # img1 = np.array(Image.open(filename))

    # Pre-processing
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((3, 3), np.uint8)
    img1 = cv2.dilate(img1, kernel, iterations=1)
    img1 = cv2.erode(img1, kernel, iterations=1)

    # OCR
    text = pytesseract.image_to_string(img1, config='--psm 4')

    # print(text)

    text_byline = text.split("\n")

    print(text_byline)

    keep = []

    for line in text_byline:
        # End loop if we see bonus set effect text as we have reached the bottom.
        if line.find('Set') > 0:
            break
        # Else keep any lines with a '+'
        elif line.find('+') > 0:
            keep.append(line)

    print("keep", keep)

    rune_stats = []

    for stat in keep:
        rune_stats.append(re.findall("([A-Z].*)([+][0-9]*.)", stat)[0])

    print(rune_stats)