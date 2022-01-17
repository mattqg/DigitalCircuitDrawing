from image import inspect_image, parse_contours, parse_words, show_image
from model import classify_words
from logic import structure
from runtime import setup_image


if __name__ == "__main__":
    image, base_image, cnts = inspect_image('test2')
    lines, words = parse_contours(image, cnts)
    word_imgs, positioned_words = parse_words(image, words)
    labeled_words = classify_words(image, word_imgs, positioned_words)
    root_words, graph = structure(base_image, lines, labeled_words)

    while True:
        setup_image(base_image, root_words, graph)
