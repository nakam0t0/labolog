from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('room_system.config')

db = SQLAlchemy(app)

import room_system.views
