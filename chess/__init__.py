from flask import Flask
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from chess.config import Config


app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt()

from chess import routes