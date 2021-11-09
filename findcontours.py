from os import link
import imutils
import cv2
import numpy as np
from random import random
# import pytesseract


# open image convert to grayscale
image = cv2.imread("test_drawings/test3.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(gray)

# find contours in the thresholded image
cnts = cv2.findContours(invert.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# array to capture line data
lines = []
words = {}
weighted_averages = {}
first_counted = False
# x_sensitivity = 1
# y_sensitivity = 1.9
sensitivity = 1
# x_weight = 0.4
# loop over the contours
for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    if M["m00"] == 0:
        continue
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
    i = 0
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

        cv2.drawContours(image, [c], -1, (255, 255, 255), -1)

    else:
        min_dist = np.inf
        selected_key = (0, 0)

        for word_key in words:

            # if word_key in list(weighted_averages.keys()):
            #     x = weighted_averages[word_key][0]
            #     y = weighted_averages[word_key][1]
            # else:
            x = word_key[0]
            y = word_key[1]

            dist = np.sqrt((cX-x)**2 + abs(cY-y)**2)

            if dist < min_dist:
                selected_key = word_key
                min_dist = dist

        # print(selected_key)
        # if selected_key in list(weighted_averages.keys()):
        #     wa_x = weighted_averages[selected_key][0]
        #     wa_y = weighted_averages[selected_key][1]
        #     wa_n = weighted_averages[selected_key][2]
        #     cv2.circle(image, (int(wa_x), int(wa_y)), 10, (255, 0, 0))
        #     weighted_averages[selected_key] = ((((wa_n-1)/wa_n)*wa_x+(1/wa_n)*cX), ((wa_n-1)/wa_n)*wa_y+(1/wa_n)*cY, wa_n+1)

        # else:
        #     weighted_averages[selected_key] = (cX, cY, 1)
        #     cv2.circle(image, (cX, cY), 10, (0, 0, 255))

        # if (cX > x-t and cX < x+t) and (cY > y-t and cY < y+t):
        #     print('within thresh x:'+str(cX)+' y:'+ str(cY))
        #     cv2.drawContours(image, [c], -1, (0, 255, 255), -1)

        if min_dist < 100*sensitivity and first_counted:
            words[selected_key].append(c)
        else:
            words[(cX, cY)] = [c]
            first_counted = True

        for word in list(words.values()):
            # color = (random()*255, random()*255, random()*255)
            color = (0, 0, 255)
            cv2.drawContours(image, word, -1, color, -1)

        # for key in words.keys():
        #     cv2.circle(image, key, 10, (255, 0, 0))

        # show the image
        cv2.imshow("Image", image)
        cv2.waitKey(0)


i = 1
for word in list(words.values()):
    cnts = np.concatenate(word)
    x, y, w, h = cv2.boundingRect(cnts)
    cv2.rectangle(image, (x, y), (x + w - 1, y + h - 1), (150, 150, 150), 2)
    image = np.array(image)
    roi = image[y:y+h, x:x+w]
    # path = "training_data/output/output{}.png".format(i)
    # cv2.imwrite(path, roi)
    i += 1
    cv2.imshow("Image", image)
    cv2.waitKey(0)

# h, w, c = image.shape
# boxes = pytesseract.image_to_boxes(image)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     image = cv2.rectangle(
#         image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# cv2.imshow('image', image)
# cv2.waitKey(0)

# results = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
# print(results)
# custom_oem_psm_config = r'--oem 3 --psm 12'
# data = pytesseract.image_to_string(image)
# print(data)
# results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

# show the output image
# cv2.imshow("Image", image)
# cv2.waitKey(0)
