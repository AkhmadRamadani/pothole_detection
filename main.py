from flask import Flask, request, render_template, jsonify
import numpy as np
from model import predictPothole, base64predict
import os
import cv2
from multiprocessing import Value
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from firebase_admin import db as firebase_db

import datetime
import pytz
import base64


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
counter = Value('i', 0)
timezone = pytz.timezone("Asia/Jakarta")
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)

firebase_admin.initialize_app(cred, {
    'storageBucket': 'pothole-detection-c439a.appspot.com'
}, name='storage')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pothole-detection-c439a-default-rtdb.asia-southeast1.firebasedatabase.app/'
}, name='realtimeDB')


db = firestore.client()
firebase_db_ref = firebase_db.reference(app=firebase_admin.get_app(name='realtimeDB'))
bucket = storage.bucket(app=firebase_admin.get_app(name='storage'))


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hi, It\'s me. I\'m the problem it\'s me.'

@app.route('/predict', methods=['POST'])
def predict():
    # get data from raw
	data = request.get_json(force=True)
	# get image url
	imageUrl = data['imageUrl']
	prediction = predictPothole(imageUrl)
	return jsonify({'prediction': prediction, })
    # predict the class using url to image
    # predict the class using path to image
    # prediction = predictPothole(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    # return jsonify({'prediction': prediction, })

@app.route('/predict64', methods=['POST'])
def predict64():
		# get data from raw
	data = request.get_json(force=True)
	# get image url
	image = data['image']
	# get latitude from real time database
	latitude = firebase_db_ref.child('latitude').get()
	# get longitude from real time database
	longitude = firebase_db_ref.child('longitude').get()

	# read image from base64
	base64Image = image
	base64Image = base64Image.split(',')[1]
	base64Image = base64Image.encode()
	base64Image = base64.b64decode(base64Image)

	# predict the class using url to image
	prediction = base64predict(image)

	# save image to firebase storage
	clock_time = datetime.datetime.now(timezone)
	clock_time = clock_time.strftime("%Y-%m-%d %H:%M:%S")
	blob = bucket.blob('pictures/'+clock_time+".jpg")
	blob.upload_from_string(base64Image, content_type='image/jpg')
	blob.make_public()

	# save image to firebase firestore
	doc_ref = db.collection(u'images').document()
	doc_ref.set({
		# image url should be downloadable from firebase storage
		u'imageUrl': blob.public_url,
		u'timestamp': firestore.SERVER_TIMESTAMP,
		u'latitude': latitude,
		u'longitude': longitude,
		u'prediction': prediction,
		u'isFixed': False
	})

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