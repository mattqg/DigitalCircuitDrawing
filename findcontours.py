import imutils
import cv2
import numpy as np

# open image convert to grayscale
image = cv2.imread("test_drawings/test1.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(gray)

# find contours in the thresholded image
cnts = cv2.findContours(invert.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# array to capture line data
lines = []
words = []

# loop over the contours
for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # returns rotated bounding rectangle
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # cv2.drawContours(image, [box], 0, (0, 0, 255), 2)

    # [[x1,y1], [x2,y2], [x3,y3], [x4, y4]]
    max_length = 0
    min_length = np.inf
    largest = [0, 0]
    smallest = [np.inf, np.inf]

    # loop through sets of points and take distance between them
    for i in range(4):
        length = np.sqrt((box[i][0] - box[i-1][0])**2 +
                         (box[i][1] - box[i-1][1])**2)
        if length <= min_length:
            min_length = length

        if length >= max_length:
            max_length = length

        if box[i][0] < smallest[0]:
            smallest = box[i]

        if box[i][0] > largest[0]:
            largest = box[i]

    ratio = max_length/min_length

    # draw the contour and center of the shape on the image
    if ratio > 5:
        lines.append({"contour": c, "left": (
            smallest[0], smallest[1]), "right": (largest[0], largest[1])})
        # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        # cv2.circle(image, (cX, cY), 15, (0, 255, 255), -1)
        # cv2.circle(image, (largest[0], largest[1]), 15, (255, 0, 255), -1)
        # cv2.circle(image, (smallest[0], smallest[1]), 15, (255, 255, 0), -1)
    else:
        words.append(c)

# for x in lines:
    # cv2.drawContours(image, [x['contour']], -1, (0, 255, 0), 2)

# show the image
cv2.imshow("Image", image)
cv2.waitKey(0)
