from image import inspect_image, parse_contours, parse_words, show_image
from model import classify_words
from logic import branchify, structure

if __name__ == "__main__":
    image, base_image, cnts = inspect_image('test')
    lines, words = parse_contours(image, cnts)
    word_imgs, positioned_words = parse_words(image, words)
    labeled_words = classify_words(image, word_imgs, positioned_words)    
    tree = branchify(base_image, lines, labeled_words)
    # board = structure(image, tree)

    # print(labels)
    # board = Board('')
    # button = Button()
    # board.add_button(button)
    # board.stringify('y')
    # while true:
    #   check mouse pos
    #   see if clicked
    #   use base image
    # 	if event == cv2.EVENT_LBUTTONDOWN:
    #   elif event == cv2.EVENT_LBUTTONUP:
    #   
    # TODO:
    # give id to each line
    # loop through lines, finding the word that is closest to each endpoint, add to dict with word key, line id value in list along w/ coords
    # Classify inputs / outputs by x and y dim for each word
    # Write_input method to write id, position is based on type of block, need template, set values to zero
    # FIGURE OUT WIRES