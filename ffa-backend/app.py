from flask import Flask, render_template, request
from flask_mongoalchemy import MongoAlchemy


app = Flask(__name__)


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/register')
def new_registration():
    register_args = request.args
    print(register_args)