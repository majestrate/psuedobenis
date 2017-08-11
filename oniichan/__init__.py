from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from oniichan import config

app = Flask(__name__)
app.config.from_object('oniichan.config')

CORS(app)
db = SQLAlchemy(app)
from oniichan import views
from oniichan import activityhub_views
db.create_all()
