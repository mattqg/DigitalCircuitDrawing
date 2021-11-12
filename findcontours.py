from os import link
import imutils
import cv2
import numpy as np
from random import random
# import pytesseract


# open image convert to grayscale
image = cv2.imread("test_drawings/training_out.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(gray)

# find contours in the thresholded image
cnts = cv2.findContours(invert.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# array to capture data
lines = []
words = {}
first_counted = False

# x_sens and y_sens change ellipse parameters
x_sens = 6
y_sens = .5


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

            # weighted euclidian distance
            dist = np.sqrt((1/x_sens)*abs(cX-x)**2 + (1/y_sens)*abs(cY-y)**2)

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
# min_dist < 100*sensitivity and
        if min_dist < 50 and first_counted:
            words[selected_key].append(c)
        else:
            words[(cX, cY)] = [c]
            first_counted = True

        # for word in list(words.values()):
        #     color = (random()*255, random()*255, random()*255)
        #     # color = (0, 0, 0)
        #     cv2.drawContours(image, word, -1, color, -1)

        # for key in words.keys():
        #     cv2.circle(image, key, 10, (255, 0, 0))

        # show the image
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)


i = 1
for word in list(words.values()):
    cnts = np.concatenate(word)
    x, y, w, h = cv2.boundingRect(cnts)
    # cv2.rectangle(image, (x, y), (x + w - 1, y + h - 1), (150, 150, 150), 2)
    image = np.array(image)
    roi = image[y:y+h, x:x+w]

    if int(224*(h/w)) <= 224:
        new_height = int(224*(h/w))
        roi_resized = cv2.resize(roi, (224, new_height))
        roi_bordered = cv2.copyMakeBorder(roi_resized, int((224-new_height)/2), int(
            (224-new_height)/2), 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    else:
        new_width = int(224*(w/h))
        roi_resized = cv2.resize(roi, (new_width, 224))
        roi_bordered = cv2.copyMakeBorder(roi_resized, 0, 0, int(
            (224-new_width)/2), int((224-new_width)/2), cv2.BORDER_CONSTANT, value=(255, 255, 255))

    path = "training_data/out/out{}.png".format(i)
    cv2.imwrite(path, roi_bordered)
    i += 1
    cv2.imshow("Image", image)
    cv2.waitKey(0)

