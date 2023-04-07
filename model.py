
import numpy as np
from keras.utils import load_img, img_to_array 
from keras.models import load_model

model = load_model('model.h5')


def predictPothole(image):
    # load image
    img = load_img(image, target_size=(64, 64))
    # convert image to array
    test_image = img_to_array(img)
    test_image = np.expand_dims(img, axis = 0)
    result = model.predict(test_image)
    prediction = ''
    if result[0][0] == 1:
        prediction = 'pothole'
    else:
        prediction = 'normal'
    return prediction




