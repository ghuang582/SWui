import pytesseract
import numpy as np
import cv2
import re

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def do_ocr(img):
    img = np.array(img)

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

    # Right OCR - for rarity of rune
    right = org_img[crop_h:, crop_w:]
    right_text = pytesseract.image_to_string(right, config = '--psm 11')
    rarity = right_text.split("\n")[0]

    # Left OCR - for stats
    # Take OCR with longer string, assume it has the more correct version
    left = img[crop_h:, :crop_w]
    left_text = pytesseract.image_to_string(left, config = '--psm 11')

    left_2nd = img[crop_h:, :crop_w]
    left_text_2nd = pytesseract.image_to_string(left_2nd) 

    left_3rd = org_img[crop_h:, :crop_w]
    left_text_3rd = pytesseract.image_to_string(left_3rd) 

    options = [left_text, left_text_2nd, left_text_3rd]
    left_text = max(options, key = len)

    # if len(left_text_2nd) > len(left_text):
    #     left_text = left_text_2nd
    # print(left_text_2nd)
    # print(left_text)

    # # If initial pass returns nothing, try again but with original image
    # # Arbitrary conditions, selected from observations of edge cases
    # if len(left_text) < 5 or left_text.find('+') == -1:
    #     print('2nd')
    #     left = org_img[crop_h:, :crop_w]
    #     left_text = pytesseract.image_to_string(left, config = '--psm 11')

    text_byline = left_text.split("\n")

    keep = []

    for line in text_byline:
        # End loop if we see bonus set effect text as we have reached the bottom.
        if line.find('Set') != -1:
            break
        # Else keep any lines with a '+'
        elif line.find('+') > 0:
            keep.append(line)

    rune_stats = []

    for stat in keep:
        rune_stats.append(re.findall("([A-Z].*)([+][0-9]*.)", stat)[0])

    # Keep only numerics in string, and convert to numeric.
    level = top_text.split(" ")[0]
    try:
        level = int(re.sub("[^0-9]", "", level))
    except ValueError:
        level = 0

    rune_info = [level, rarity, 0]

    # Determine if rune has innate stat
    lines_no = len(rune_stats)
    if lines_no > 5:
        rune_info[2] = 1
    elif rarity.find("Hero") != -1 and lines_no > 4:
        rune_info[2] = 1
    elif rarity.find("Rare") != -1 and lines_no > 3:
            rune_info[2] = 1
    
    # Fill rune_stats list to ensure output always has the same length of 5 (6 if rune has an innate stat)
    cap = 5 + rune_info[2]

    while lines_no < cap:
        rune_stats.append(('Slot {n}'.format(n = lines_no - rune_info[2]), ''))
        lines_no = len(rune_stats)


    return [rune_info, rune_stats]

if __name__ == "__main__":
    # filename = "C:/Users/Admin/Desktop/SWOverlay/Cropped/break_case2.png"
    # img2 = np.array(Image.open(filename))
    # print( do_ocr(img2))

    import RecordScreen
    import BoxDetection
    import PIL

    # snapshot = RecordScreen.screenshot('NoxPlayer2')
    snapshot = RecordScreen.screenGrab()

    # snapshot.show()
    cropped = BoxDetection.crop_boxes(snapshot)
    # print(cropped)
    rune = do_ocr(cropped[0])
    print(rune)