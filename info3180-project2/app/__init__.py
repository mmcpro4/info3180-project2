from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './app/static/uploads' 
app.config['SECRET_KEY'] = os.urandom(67)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:password@localhost/project2v" 
app.config['LINK']=" "
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views

