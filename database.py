from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired
from flask import Flask, redirect, request, render_template, session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nazabive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'penza_street_networks'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    avatar_id = db.Column(db.Integer,
                          db.ForeignKey("resources.id"),
                          nullable=False)
    resource = db.relationship


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Boolean, unique=False, nullable=False)


class Avatars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar_id = db.Column(db.Integer,
                          db.ForeignKey("resources.id"),
                          nullable=False)
    resource = db.relationship("User", backref=db.backref("Avatar", lazy=True))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)


if __name__ == '__main__':
    # первичная инициализация, уже проведена
    # users_initialization()
    db.create_all()
    app.run(port=8080, host="127.0.0.1")
