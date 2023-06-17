
import numpy as np
from keras.utils import load_img, img_to_array 
from keras.models import load_model
import urllib
import cv2
model = load_model('model.h5')


def predictPothole(image):
    url = urllib.request.urlopen(image)
    arr = np.asarray(bytearray(url.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    # resize image to 64x64
    img = cv2.resize(img, (64, 64))
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




