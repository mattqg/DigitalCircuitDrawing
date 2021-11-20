from image import inspect_image, parse_contours, parse_words
# from model import classify_words
from parse import Board, Button, stringify

if __name__ == "__main__":
    image, cnts = inspect_image('test')
    lines, words = parse_contours(image, cnts)
    word_imgs, pos = parse_words(image, words)
    # labels = classify_words(image, word_imgs, pos)    
    board = Board('test3')
    button = Button(type = "And", id = 0, name = "AND#0", x = 8, y =-4, width = 10, height = 10, rotation = 0)
    board.add_button(button)
    board.stringify('y')

    # TODO:
    # give id to each line
    # loop through lines, finding the word that is closest to each endpoint, add to dict with word key, line id value in list along w/ coords
    # Classify inputs / outputs by x and y dim for each word
    # Write_input method to write id, position is based on type of block, need template, set values to zero
    # FIGURE OUT WIRES