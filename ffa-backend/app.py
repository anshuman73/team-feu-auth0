from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials


app = Flask(__name__)


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/register')
def new_registration():
    register_args = request.args
    