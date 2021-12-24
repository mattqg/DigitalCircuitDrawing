from imutils import grab_contours
import cv2
import numpy as np

def inspect_image(input_name, show_input = False):

    # open image convert to grayscale
    image = cv2.imread("test_drawings/" + input_name + ".png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    base_image = image.copy()
    # find contours in the thresholded image
    cnts = cv2.findContours(invert.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    
    if show_input:
        show_image(image)

    return image, base_image, grab_contours(cnts)

def show_image(img):
    screen_res = 1280, 720
    scale_width = screen_res[0] / img.shape[1]
    scale_height = screen_res[1] / img.shape[0]
    scale = min(scale_width, scale_height)
    #resized window width and height
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    #cv2.WINDOW_NORMAL makes the output window resizealbe
    cv2.namedWindow('Resized Window', cv2.WINDOW_NORMAL)
    #resize the window according to the screen resolution
    cv2.resizeWindow('Resized Window', window_width, window_height)
    cv2.imshow('Resized Window', img)
    cv2.waitKey(0)


def parse_contours(image, cnts, output= 'tests', x_sens = 6, y_sens = 0.5):
     # array to capture data
    lines = []
    words = {}

    first_counted = False

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

        # draw the contour white and center the shape on the image
        if ratio > 5:
            lines.append({"cnt": [c], "left": (
                smallest[0], smallest[1]), "right": (largest[0], largest[1])})

            cv2.drawContours(image, c, -1, (255, 255, 255), -1)

        else:
            min_dist = np.inf
            selected_key = (0, 0)

            for word_key in words:

                x = word_key[0]
                y = word_key[1]

                # weighted euclidian distance
                dist = np.sqrt((1/x_sens)*abs(cX-x)**2 + (1/y_sens)*abs(cY-y)**2)

                if dist < min_dist:
                    selected_key = word_key
                    min_dist = dist

            if min_dist < 50 and first_counted:
                words[selected_key].append(c)
            else:
                words[(cX, cY)] = [c]
                first_counted = True
    
    return lines, words

def parse_words(image, words, export_path = False, rect_output = False, show_outputs = False, starting_num = 1):
    images = []
    positioned_words = []

    for word in list(words.values()):
        cnts = np.concatenate(word)
        x, y, w, h = cv2.boundingRect(cnts)
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

        roi_bordered_resized = cv2.resize(roi_bordered, (224, 224))

        if export_path and isinstance(export_path, str):
            path = "training_data/" + export_path + "/" + export_path + "{}.png".format(starting_num)
            cv2.imwrite(path, roi_bordered_resized)
            starting_num += 1
        elif rect_output:
            cv2.rectangle(image, (x, y), (x + w - 1, y + h - 1), (150, 150, 150), 2)
            show_image(image)
        
        if show_outputs:
            show_image(roi_bordered_resized)

        positioned_words.append({'word': word,'pos':(int(x+w/2),int(y+h/2),x,y,w,h)})        
        images.append(roi_bordered_resized)

    return np.asarray(images), positioned_words