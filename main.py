from image import inspect_image, parse_contours, parse_words
from model import classify_words
from logic import structure
from runtime import run_sim


if __name__ == "__main__":
    image, base_image, cnts = inspect_image('test4')
    lines, words = parse_contours(image, cnts)
    word_imgs, positioned_words = parse_words(image, words)
    labeled_words = classify_words(image, word_imgs, positioned_words, show=True)
    root_words, graph = structure(base_image, lines, labeled_words, show_branches=True)

    while True:
        run_sim(base_image, root_words, graph)