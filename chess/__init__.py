import os
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] ='filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
socketio = SocketIO(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt()

from chess import routes