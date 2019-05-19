from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from src.common.database import Database

app = Flask(__name__)
CORS(app)
app.secret_key = "Jimmy"
socketio = SocketIO(app)

@app.before_first_request
def init():
    Database.go()
