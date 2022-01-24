from PIL import Image
import pytesseract
import numpy as np
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

filename = "C:/Users/Admin/Desktop/SWOverlay/Cropped/2.png"
img1 = np.array(Image.open(filename))

# Pre-processing
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
kernel = np.ones((3, 3), np.uint8)
img1 = cv2.dilate(img1, kernel, iterations=1)
img1 = cv2.erode(img1, kernel, iterations=1)
# cv2.threshold(cv2.bilateralFilter(img1, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# OCR
text = pytesseract.image_to_string(img1, config='--psm 4')

print(text)

rune_list = text.split("\n")

# print(rune_list)

# cv2.imshow('view', img1)
# cv2.waitKey(0)

from pytesseract import Output
# import pytesseract
# import cv2

# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# filename = "C:/Users/Admin/Desktop/SWOverlay/Cropped/1.png"
# image = cv2.imread(filename)
image = img1

results = pytesseract.image_to_data(image, output_type=Output.DICT)

for i in range(0, len(results['text'])):
    x = results['left'][i]
    y = results['top'][i]
    
    w = results['width'][i]
    h = results['height'][i]
    text = results['text'][i]
    conf = int(float(results['conf'][i]))
    if conf > 70:
        text = ''.join([c if ord(c) < 128 else '' for c in text]).strip()
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

cv2.imshow('test', image)
cv2.waitKey(0)
# print(results)