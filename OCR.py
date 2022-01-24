from re import findall
from PIL import Image
import pytesseract
import numpy as np
import cv2
import re

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def do_ocr(img):
    # Pre-processing
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    org_img = img
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Split image into 3 sections for better OCR results (top, left, and right)
    h, w = img.shape
    crop_h = round(0.145 * h)
    crop_w = round(0.65 * w)

    # Top OCR - for level and set
    top = img[:crop_h, round(0.2 * w):round(0.8 * w)]
    top_text = pytesseract.image_to_string(top)
    print(top_text)

    # Right OCR - for rarity of rune
    right = org_img[crop_h:, crop_w:]
    right_text = pytesseract.image_to_string(right)
    rarity = right_text.split("\n")[0]
    # print(right_text)
    print(rarity)

    # Left OCR - for stats
    left = img[crop_h:, :crop_w]
    left_text = pytesseract.image_to_string(left)
    print(left_text)

    text_byline = left_text.split("\n")

    keep = []

    for line in text_byline:
        # End loop if we see bonus set effect text as we have reached the bottom.
        if line.find('Set') > 0:
            break
        # Else keep any lines with a '+'
        elif line.find('+') > 0:
            keep.append(line)

    # print("keep", keep)

    rune_stats = []

    for stat in keep:
        rune_stats.append(re.findall("([A-Z].*)([+][0-9]*.)", stat)[0])

    print(rune_stats)

if __name__ == "__main__":
    filename = "C:/Users/Admin/Desktop/SWOverlay/Cropped/4.png"
    img2 = np.array(Image.open(filename))
    do_ocr(img2)