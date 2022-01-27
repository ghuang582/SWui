import numpy as np
import cv2

def crop_boxes(img = "C:/Users/Admin/Desktop/SWOverlay/Screenshot_2022-01-18-02-43-35.png"):
    cropped_images = []

    # Load image, grayscale, adaptive threshold
    if type(img) == str:
        image = cv2.imread(img)
    else:
        image = np.array(img)

    result = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)

    # Fill rectangular contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

    # Draw rectangles
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
    
    contours, hiearchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Unpack image dimensions
    i_h, i_w, i_c = image.shape

    idx = 0
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)

        if w > 0.4 * i_w:
            idx += 1
            new_img = result[y:y+h, x:x+w]
            cropped_images.append(new_img)
    
    return cropped_images

# Helper function
def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

# Check list is being created properly
# n = 0
# for img in cropped_images:
#     print(img)
#     cv2.imshow('{n}'.format(n = n), img)
#     n += 1

# cv2.waitKey(0)

# import RecordScreen
# import PIL

# snapshot = RecordScreen.screenGrab()
# # snapshot.show()
# # gray = cv2.cvtColor(snapshot, cv2.COLOR_BGR2GRAY)
# test = crop_boxes(snapshot)
# print(test)