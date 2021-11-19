from image import inspect_image, parse_contours, parse_words
from model import classify_words

if __name__ == "__main__":
    image, cnts = inspect_image('test4')
    lines, words = parse_contours(image, cnts)
    word_imgs, pos = parse_words(image, words)
    labels = classify_words(image, word_imgs, pos, show=True)    
