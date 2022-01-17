import cv2
import builtins
from image import show_image


def setup_image(img, rw, graph):
    show_image(img, wait=1)
    cv2.setMouseCallback('Digital Circuit Sim', find_mouse)
    builtins.rw = rw
    builtins.graph = graph
    builtins.img = img


def find_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        update_image(x, y)


def update_image(x, y):
    rw = builtins.rw
    graph = builtins.graph
    img = builtins.img

    for word in rw:
        w_x1 = word.corner_pos[0]
        w_y1 = word.corner_pos[1]
        w_x2 = w_x1 + word.dim[0]
        w_y2 = w_y1 + word.dim[1]

        if w_x1 <= x <= w_x2 and w_y1 <= y <= w_y2:
            word.flip_state()
            print(f'Word Found at ID {word.id}')
            # cv2.drawContours(img, word.cnt, -1, (255, 255, 0), thickness=cv2.FILLED)

    propagate_states()

    for word_line in graph:
        if word_line.state:
            cv2.drawContours(img, word_line.cnt, -1, (255, 255, 0),
                             thickness=cv2.FILLED)
        else:
            cv2.drawContours(img, word_line.cnt, -1, (0, 0, 0),
                             thickness=cv2.FILLED)


def propagate_states():
    pass

# def get_click():
#     try:
#         click_x = builtins.x1
#         click_y = builtins.y1
#     except AttributeError:
#         click_x = None
#         click_y = None

#     return (click_x, click_y)


# def propagate_logic(mouse_pos, root_words, graph):
#     print(mouse_pos)

# visitedList = [[]]

# def depthFirst(graph, currentVertex, visited):
#     visited.append(currentVertex)
#     for vertex in graph[currentVertex]:
#         if vertex not in visited:
#             depthFirst(graph, vertex, visited.copy())
#     visitedList.append(visited)

# depthFirst(graph, 0, [])

# print(visitedList)
