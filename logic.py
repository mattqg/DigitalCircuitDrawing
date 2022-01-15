import cv2
import numpy as np
from image import show_image

class Logic():
    def __init__(self, id, label, cnt, pos):
        self.id = id
        self.label = label
        self.cnt = cnt
        self.pos = pos[:2]
        self.dim = pos[4:]
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class Line():
    def __init__(self, id, cnt, left, right):
        self.id = id
        self.cnt = cnt
        self.left = left
        self.right = right
        self.children = []

    def add_child(self, child):
        self.children.append(child)
    
def structure(image, lines, words, show_algorithm = False, show_branches = False):
    # lines: array [{'cnt': c, 'left': (x,y), 'right': (x,y)}]
    # words: array [{label: 'Not', 'cnt': c, 'pos': (x,y,w,h)}]
    blank_img = image.copy()

    id = 0
    line_list = []
    word_list = []
    for line in lines:
        line_list.append(Line(id, line['cnt'], line['left'], line['right']))
        id += 1
    for word in words:
        word_list.append(Logic(id, word['label'], word['cnt'], word['pos']))
        id += 1
    
    for line in line_list:
        left = line.left
        right = line.right

        selected_left = None
        selected_right = None
        lowest_left_dist = np.inf
        lowest_right_dist = np.inf
        shown_lines_left = []
        shown_lines_right = []

        for word in word_list:
            word_pos = word.pos
            dist_left = ((word_pos[0]-left[0])**2 + (word_pos[1]-left[1])**2)**0.5
            dist_right = ((word_pos[0]-right[0])**2 + (word_pos[1]-right[1])**2)**0.5
            
            if dist_left < lowest_left_dist:
                selected_left = word
                lowest_left_dist = dist_left

            if dist_right < lowest_right_dist:
                selected_right = word
                lowest_right_dist = dist_right

            if show_algorithm:
                cv2.line(image, word_pos, left, (100,100,100), 1, lineType=cv2.LINE_AA)
                show_image(image)

                if selected_left.pos == word_pos:
                    for show_line in shown_lines_left:
                        cv2.line(image, show_line[0], show_line[1], (100,100,100), 1, lineType=cv2.LINE_AA)
                        
                    cv2.line(image, selected_left.pos, left, (0,200,0), 1, lineType=cv2.LINE_AA)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.rectangle(image, (0,0), (600,50), (255, 255, 255), -1)
                    cv2.putText(image, f'Left Distance:{round(dist_left,2)} px', (20,40), cv2.FONT_HERSHEY_DUPLEX, 1, (100,100,100), lineType=cv2.LINE_AA)
                    shown_lines_left.append([selected_left.pos, left])
                    
                show_image(image)

                cv2.line(image, word_pos[:2], right, (100,100,100), 1, lineType=cv2.LINE_AA)
                show_image(image)

                if selected_right.pos == word_pos:
                    for show_line in shown_lines_right:
                        cv2.line(image, show_line[0], show_line[1], (100,100,100), 1, lineType=cv2.LINE_AA)

                    cv2.line(image, selected_right.pos, right, (0,200,0), 1, lineType=cv2.LINE_AA)
                    cv2.rectangle(image, (0,50), (600,100), (255, 255, 255), -1)
                    cv2.putText(image, f'Right Distance: {round(dist_right,2)} px', (20,100), cv2.FONT_HERSHEY_DUPLEX, 1, (100,100,100), lineType=cv2.LINE_AA)
                    shown_lines_right.append([selected_right.pos, right])

                show_image(image)

        image = blank_img.copy()

        # print(selected_left.id, line.id, selected_right.id)
        selected_left.add_child(line)
        line.add_child(selected_right)
        # print(selected_left.children, line.children, selected_right.children)

    if show_branches:
        for line in line_list:
            cv2.drawContours(image, line.cnt, -1, (0, 0, 255), -1)
            show_image(image)
            for child in line.children:
                cv2.drawContours(image, child.cnt, -1, (0, 255, 0), -1)
                show_image(image)

        for word in word_list:
            cv2.drawContours(image, word.cnt, -1, (255, 0, 0), -1)
            show_image(image)
            for child in word.children:
                cv2.drawContours(image, child.cnt, -1, (0, 255, 0), -1)
                show_image(image)

    children = []
    graph = {}
    for line in line_list:
        graph[line.id] = [x.id for x in line.children]
        for sel_chidren in line.children:
            if sel_chidren not in children:
                children.append(sel_chidren)
    for word in word_list:
        graph[word.id] = [x.id for x in word.children]
        for sel_chidren in word.children:
            if sel_chidren not in children:
                children.append(sel_chidren)
    root_words = []
    for word in word_list:
        if word not in children:
            root_words.append(word)
    # print(graph)
    return root_words, graph