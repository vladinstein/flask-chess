from flask import Flask
from flask import session
from flask_session import Session
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] ='filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
socketio = SocketIO(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt()

from chess import routes