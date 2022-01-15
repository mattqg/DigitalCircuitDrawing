import cv2
from image import show_image
import builtins

def setup_image(img):
    show_image(img, wait=1)
    cv2.setMouseCallback("Digital Circuit Sim", find_mouse)

def find_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        builtins.x1 = x
        builtins.y1 = y

def get_click(): 
    try:
        click_x = builtins.x1
        click_y = builtins.y1
    except AttributeError:
        click_x = 0
        click_y = 0

    return (click_x, click_y)


def propagate_logic(pos, root_words, graph):
    pass


def update_image(base_image, prop_contours):
    pass
    # cv2.line(prev_image, (0,20), (100, 900), (0,200,0), 1, lineType=cv2.LINE_AA)
    # ui = cv2.imread("test_drawings/" + "test2" + ".png")
    # show_image(ui, 1)

# def depthFirst(graph, currentVertex, visited):
#     visited.append(currentVertex)
#     for vertex in graph[currentVertex]:
#         if vertex not in visited:
#             depthFirst(graph, vertex, visited.copy())
#     visitedList.append(visited)

# depthFirst(graph, 0, [])

# print(visitedList)
