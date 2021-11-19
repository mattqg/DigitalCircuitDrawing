from keras.models import load_model
from image import show_image
import numpy as np
import cv2

def classify_words(image, word_imgs, positions, show=False):
    # Load the model
    model = load_model('model/keras_model.h5', compile=False)

    # Normalize the image
    normalized_image_array = (word_imgs.astype(np.float32) / 127.0) - 1

    # run the inference
    prediction = model.predict(normalized_image_array)

    # label lookup
    lookup = ['In', 'Out', 'And', 'Or', 'Xor', 'Not']

    labels = []

    for i, predict in enumerate(prediction):
        index = np.argmax(predict)
        label = lookup[index]
        pos = positions[i]

        labels.append({'index': index, 'label': label, 'pos': pos})

        if show:
            cv2.putText(image, label + " " + str(round(np.amax(predict),4)), (int(pos[0]), int(pos[1]-15)), cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,0), lineType=cv2.LINE_AA)
            show_image(image)
    
    return labels