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
    state = request.args.get('state')
    return render_template('register.html', user_email=user_email, username=username, state=state)


@app.route('/register-image', methods=['POST'])
def register_face():
    user_email = request.args.get('email')
    username = request.args.get('username')
    image = request.files['webcam']
    utils.register_face([image.read()], 'auth0-demo', username)
    return 'OK'


@app.route('/verify')
def verify():
    user_email = request.args.get('email')
    username = request.args.get('username')
    state = request.args.get('state')
    return render_template('verify.html', user_email=user_email, username=username, state=state)


@app.route('/verify-image', methods=['POST'])
def verify_face():
    user_email = request.args.get('email')
    username = request.args.get('username')
    image = request.files['webcam']
    person = utils.find_person(image.read(), 'auth0-demo')
    if person == username:
        return 'OK'
    return 'NOT OK'


@app.route('/send-email')
def send_email():
    user_email = request.args.get('email')
    username = request.args.get('username')
    utils.send_email(user_email, username)
    return 'OK'


@app.route('/thanks')
def registration_done():
    return render_template('thanks.html')


@app.route('/false-verify')
def false_verify():
    return 'Could not match Face identity'

app.run(debug=True)
