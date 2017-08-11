from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from oniichan import config
from oniichan import views
app.config.from_object('oniichan.config')
