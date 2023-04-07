from flask import Flask, request, render_template, jsonify
import numpy as np
from model import predictPothole
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hi, It\'s me. I\'m the problem it\'s me.'

@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['image'] # get the image
    # save the image to ./uploads
    image.save(os.path.join('./uploads', image.filename))
    # predict the class using path to image
    prediction = predictPothole(os.path.join('./uploads', image.filename))
    return jsonify({'prediction': prediction, })



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))