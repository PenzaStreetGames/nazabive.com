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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author_relation = db.relationship("User", backref=db.backref("Posts"),
                                      lazy=True)
    content = db.Column(db.String, unique=False, nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Boolean, unique=False, nullable=False)


"""class Avatars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar_id = db.Column(db.Integer,
                          db.ForeignKey("resources.id"),
                          nullable=False)
    resource = db.relationship("User", backref=db.backref("Avatar", lazy=True))"""


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey("user.id"),
                       nullable=False)
    sender_relation = db.relationship("User", backref=db.backref("Sent"),
                                      lazy=True)
    chat = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    chat_relation = db.relationship("Chat", backref=db.backref("Messages"),
                                    lazy=True)
    text = db.Column(db.String(1000), unique=False, nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    post_relation = db.relationship("Post", backref=db.backref("Likes"),
                                    lazy=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_relation = db.relationship("User", backref=db.backref("Users"),
                                    lazy=True)


"""class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    friend = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    target_relation = db.relationship("User", backref=db.backref("Targets"),
                                      lazy=True)
    friend_relation = db.relationship("User", backref=db.backref("Friends"),
                                      lazy=True)"""


class ChatMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_relation = db.relationship("User", backref=db.backref("Chats"),
                                    lazy=True)
    chat = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    chat_relation = db.relationship("Chat", backref=db.backref("Users"),
                                    lazy=True)


def get_all_users():
    return User.query.all()


def add_user(username, password, name, surname):
    new_user = User(username=username, password=password,
                    name=name, surname=surname)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()


def delete_user(user_id):
    try:
        User.query.filter(User.id == user_id).delete()
        db.session.commit()
    except Exception as error:
        print(error)
        db.session.rollback()


if __name__ == '__main__':
    # первичная инициализация, уже проведена
    # users_initialization()
    db.create_all()
    print(get_all_users())
    add_user("User", "123", "Паша", "Соломатин")
    print(get_all_users())
    app.run(port=8080, host="127.0.0.1")
