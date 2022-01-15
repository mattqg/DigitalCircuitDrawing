from image import inspect_image, parse_contours, parse_words
from model import classify_words
from logic import structure
from runtime import setup_image, get_click, propagate_logic

if __name__ == "__main__":
    image, base_image, cnts = inspect_image('test1')
    lines, words = parse_contours(image, cnts)
    word_imgs, positioned_words = parse_words(image, words)
    labeled_words = classify_words(image, word_imgs, positioned_words)
    root_words, graph = structure(base_image, lines, labeled_words)

    setup_image(base_image)
    running = True
    while running:
        pos = get_click()
        break
        # rw_state, prop_contours = propagate_logic(pos, root_words, graph)
        # update_image(base_image, prop_contours)
