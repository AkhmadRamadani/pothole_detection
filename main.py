from flask import Flask, request, render_template, jsonify
import numpy as np
from model import predictPothole
import os
import cv2
from multiprocessing import Value

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
counter = Value('i', 0)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hi, It\'s me. I\'m the problem it\'s me.'

@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['image'] # get the image
    # save the image to ./uploads
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    # predict the class using path to image
    prediction = predictPothole(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    return jsonify({'prediction': prediction, })


@app.route('/upload', methods=['POST','GET'])
def upload():
	received = request
	img = None
	if received.files:
		print(received.files['imageFile'])
		# convert string of image data to uint8
		file  = received.files['imageFile']
		nparr = np.fromstring(file.read(), np.uint8)
		# decode image
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		save_img(img)
		
		return "[SUCCESS] Image Received", 201
	else:
		return "[FAILED] Image Not Received", 204

def save_img(img):
	with counter.get_lock():
		counter.value += 1
		count = counter.value
	img_dir = "esp32_imgs"
	if not os.path.isdir(img_dir):
		os.mkdir(img_dir)
	cv2.imwrite(os.path.join(img_dir,"img_"+str(count)+".jpg"), img)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=8000), host='0.0.0.0')