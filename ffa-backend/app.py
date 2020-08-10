from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import utils


app = Flask(__name__, static_folder='assets')


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/register')
def new_registration():
    user_email = request.args.get('email')
    username = request.args.get('username')
    return render_template('register.html', user_email=user_email, username=username)


@app.route('/register-image')
def register_face():
    user_email = request.args.get('email')
    username = request.args.get('username')
    image = request.files['photo']
    utils.register_face([image.read()], 'auth0-demo', user_email)
    return 'OK'


@app.route('/send-email')
def send_email():
    user_email = request.args.get('email')
    username = request.args.get('username')
    utils.send_email(user_email, username)
    return 'OK'


@app.route('/thanks')
def registration_done():
    return render_template('thanks.html')

app.run()