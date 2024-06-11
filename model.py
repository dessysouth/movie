from flask_login import UserMixin
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    movie_list = db.relationship('MovieList', backref='user', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    image = db.Column(db.String())
    date = db.Column(db.String(150))
    download_link = db.Column(db.String)
    description = db.Column(db.String)

   
    movie_lists = db.relationship('MovieList', backref='movie', lazy=True)

class MovieList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()
