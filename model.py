
import numpy as np
from keras.utils import load_img, img_to_array 
from keras.models import load_model
import urllib
import cv2
import base64

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




def base64predict(image):
    # read image from base64
    base64Image = image
    base64Image = base64Image.split(',')[1]
    base64Image = base64Image.encode()
    base64Image = base64.b64decode(base64Image)
    # convert string of image data to uint8
    nparr = np.fromstring(base64Image, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
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
