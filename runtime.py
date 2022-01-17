import cv2
import builtins
from image import show_image


def run_sim(img, rw, graph, theme='material_dark'):
    show_image(img, wait=1)
    cv2.setMouseCallback('Digital Circuit Sim', find_mouse)
    theme = select_color(theme)

    if not builtins.first_run:
        img[:] = theme['background']

        for word_line in graph:
            if word_line.label == "In":
                cv2.drawContours(img, word_line.cnt, -1,
                                 theme['in_off'], thickness=cv2.FILLED)
            else:
                cv2.drawContours(img, word_line.cnt, -1,
                                 theme['off'], thickness=cv2.FILLED)
        builtins.first_run = True

    builtins.rw = rw
    builtins.graph = graph
    builtins.img = img
    builtins.theme = theme


def find_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        update_image(x, y)


def update_image(x, y):
    rw = builtins.rw
    graph = builtins.graph
    img = builtins.img
    theme = builtins.theme

    for word in rw:
        w_x1 = word.corner_pos[0]
        w_y1 = word.corner_pos[1]
        w_x2 = w_x1 + word.dim[0]
        w_y2 = w_y1 + word.dim[1]

        if w_x1 <= x <= w_x2 and w_y1 <= y <= w_y2:
            word.flip_state()
            print(f'Word Found at ID {word.id}, {word.label}')

    for word in rw:
        propagate_states(word, word.state)
    for word in rw:
        propagate_states(word, word.state)

    img[:] = theme['background']

    for word_line in graph:
        # print(word_line.id, word_line.state)
        if word_line.state:
            cv2.drawContours(img, word_line.cnt, -1, theme['on'],
                             thickness=cv2.FILLED)
        else:
            if word_line.label == "In":
                cv2.drawContours(img, word_line.cnt, -1, theme['in_off'],
                                 thickness=cv2.FILLED)
            else:
                cv2.drawContours(img, word_line.cnt, -1, theme['off'],
                                 thickness=cv2.FILLED)


def propagate_states(word, prev_state):
    for child in word.children:
        child.update_state(prev_state, word.id)
        if child.children:
            propagate_states(child, child.state)


def select_color(theme):
    colors = {'material_dark': {'background': (38, 32, 26),
                                'on': (196, 203, 128),
                                'off': (75, 75, 75),
                                'in_off': (150, 150, 150),
                                }
              }
    return colors[theme]
