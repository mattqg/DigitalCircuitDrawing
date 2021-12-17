import cv2
import json
import anytree
import numpy as np
from image import show_image

class Board:
    def __init__(self):
        self.data = []

    def add_button(self, button):
        self.data.append(button)

    def save(self, output):
        formatted_data = [button.format() for button in self.data]
        with open(f'saves/{output}.board', 'w') as f:
            f.write(json.dumps(formatted_data, separators=(',', ':')))


class Button:
    def __init__(self, type, id, x, y, width, height, inputs=[], outputs=[]):
        self.type = type
        self.id = id
        self.pos = {'x': x, 'y':y}
        self.dim = {'width': width, 'height': height}
        self.inputs = inputs
        self.outputs = outputs

    def add_input(self, input_button):
        self.input.append(input_button.id)

    def add_output(self, output_button):
        self.output.append(output_button.id)

    def format(self):
        # list['button', dict] -> dict pos, width, output, etc
        info_dict = {'type': self.type, 'id': self.id, 'pos': self.pos, 'width': self.width, 'height': self.height, 'inputs': self.inputs, 'outputs': self.outputs}
        return info_dict

def branchify(image, lines, words, show_algorithm = False):
    # lines: array [{'cnt': c, 'left': (x,y), 'right': (x,y)}]
    # words: array [{label: 'Not', 'cnt': c, 'pos': (x,y,w,h)}]
    blank_img = image.copy()

    for line in lines:
        left = line['left']
        right = line['right']

        selected_left = None
        selected_right = None
        lowest_left_dist = np.inf
        lowest_right_dist = np.inf
        shown_lines_left = []
        shown_lines_right = []

        for word in words:
            word_pos = word['pos']
            dist_left = ((word_pos[0]-left[0])**2 + (word_pos[1]-left[1])**2)**0.5
            dist_right = ((word_pos[0]-right[0])**2 + (word_pos[1]-right[1])**2)**0.5
            
            if dist_left < lowest_left_dist:
                selected_left = word
                lowest_left_dist = dist_left

            if dist_right < lowest_right_dist:
                selected_right = word
                lowest_right_dist = dist_right
                show_image(image)

            if show_algorithm:
                cv2.line(image, word_pos[:2], left, (100,100,100), 1, lineType=cv2.LINE_AA)
                show_image(image)

                if selected_left['pos'][:2] == word_pos[:2]:
                    for line in shown_lines_left:
                        cv2.line(image, line[0], line[1], (100,100,100), 1, lineType=cv2.LINE_AA)
                        
                    cv2.line(image, selected_left['pos'][:2], left, (0,200,0), 1, lineType=cv2.LINE_AA)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.rectangle(image, (0,0), (600,50), (255, 255, 255), -1)
                    cv2.putText(image, f'Left Distance:{round(dist_left,2)} px', (20,40), cv2.FONT_HERSHEY_DUPLEX, 1, (100,100,100), lineType=cv2.LINE_AA)
                    shown_lines_left.append([selected_left['pos'][:2], left])
                    
                
                show_image(image)

                cv2.line(image, word_pos[:2], right, (100,100,100), 1, lineType=cv2.LINE_AA)
                show_image(image)

                if selected_right['pos'][:2] == word_pos[:2]:
                    for line in shown_lines_right:
                        cv2.line(image, line[0], line[1], (100,100,100), 1, lineType=cv2.LINE_AA)

                    cv2.line(image, selected_right['pos'][:2], right, (0,200,0), 1, lineType=cv2.LINE_AA)
                    cv2.rectangle(image, (0,50), (600,100), (255, 255, 255), -1)
                    cv2.putText(image, f'Right Distance: {round(dist_right,2)} px', (20,100), cv2.FONT_HERSHEY_DUPLEX, 1, (100,100,100), lineType=cv2.LINE_AA)
                    shown_lines_right.append([selected_right['pos'][:2], right])

                show_image(image)

        image = blank_img.copy()

        print('\n')

def structure():
    pass




    
