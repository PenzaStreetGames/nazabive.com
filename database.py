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
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    private = db.Column(db.Boolean, nullable=False)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.Integer, nullable=False)


"""class Avatars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar_id = db.Column(db.Integer,
                          db.ForeignKey("resources.id"),
                          nullable=False)
    resource = db.relationship("User", backref=db.backref("Avatar", lazy=True))"""


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    chat = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(1000), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, nullable=False)
    author = db.Column(db.Integer, nullable=False)


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
    user = db.Column(db.Integer, nullable=False)
    chat = db.Column(db.Integer, nullable=False)


class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.Integer, nullable=False)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_user = db.Column(db.Integer, nullable=False)
    friend = db.Column(db.Integer, nullable=False)


class UserModel:
    """обработка пользователей"""

    def add(self, username, password, name, surname):
        """добавление/регистрация пользователя"""
        new_user = User(username=username, password=password,
                        name=name, surname=surname)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()

    def get_all(self):
        """список пользователей"""
        return User.query.all()

    def delete(self, user_id):
        """удаление пользователя"""
        try:
            User.query.filter(User.id == user_id).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()

    def exists(self, username, password):
        user = User.query.filter(User.username == username).first()
        if not user:
            return "Not found"
        if user.password != password:
            return "Wrong password"
        return user


class FriendRequestModel:
    """обработка заявок в друзья"""

    def send(self, sender, receiver):
        """создать заявку в друзья"""
        new_request = FriendRequest(sender=sender, receiver=receiver)
        try:
            db.session.add(new_request)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()

    def rollback(self, id):
        """вернуть заявку"""
        try:
            FriendRequest.query.filter(FriendRequest.id == id).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()

    def get(self, sender, receiver):
        """найти заявку по отправителю и получателю"""
        request = FriendRequest.query.filter(
            FriendRequest.sender == sender and
            FriendRequest.receiver == receiver).first()
        return request

    def get_for(self, user):
        """список заявок пользователю"""
        requests = FriendRequest.query.filter(
            FriendRequest.receiver == user).all()
        return requests

    def get_of(self, user):
        """список заявок от пользователя"""
        requests = FriendRequest.query.filter(
            FriendRequest.sender == user).all()
        return requests

    def accept(self, id):
        """подтвердить заявку"""
        friend_request = FriendRequest.query.filter(
            FriendRequest.id == id).first()
        FriendModel.create_connection(friend_request.sender,
                                      friend_request.receiver)
        try:
            FriendRequest.query.filter(FriendRequest.id == id).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()

    def reject(self, id):
        """отклонить заявку"""
        try:
            FriendRequest.query.filter(FriendRequest.id == id).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()


class FriendModel:
    """обработка связей между друзьями"""

    def create_connection(self, user_1, user_2):
        """создание дружбы между двумя пользователями"""
        friend_1 = Friend(base_user=user_1,
                          friend=user_2)
        friend_2 = Friend(base_user=user_2,
                          friend=user_1)
        try:
            db.session.add(friend_1)
            db.session.add(friend_2)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()

    def get_relation(self, user_1, user_2):
        """найти дружбу по двум друзьям"""
        request = Friend.query.filter(
            Friend.base_user == user_1 and
            Friend.friend == user_2).first()
        return request

    def get_friends(self, user):
        """список друзей"""
        friends = Friend.query.filter(Friend.base_user == user).all()
        return friends

    def delete_friend(self, user_1, user_2):
        """удалить друга"""
        relation_1 = FriendModel.get_relation(user_1, user_2)
        relation_2 = FriendModel.get_relation(user_2, user_1)
        try:
            Friend.query.filter(Friend.id == relation_1).delete()
            Friend.query.filter(Friend.id == relation_2).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()


class ChatMemberModel:
    """обработка участников чатов"""

    def add(self, user, chat):
        """создание участника"""
        member = ChatMember(user=user, chat=chat)
        try:
            db.session.add(member)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()


class ChatModel:
    """обработка чатов"""

    def create(self, *users, name="Unnamed", private=False):
        """создание чата"""
        chat = Chat(name=name, private=private)
        db.session.add(chat)
        db.session.commit()
        if private and len(users) != 2:
            return "Public settings for private chat"
        for user in users:
            member = ChatMember(user=user, chat=chat.id)
            db.session.add(member)
        db.session.commit()


if __name__ == '__main__':
    # первичная инициализация, уже проведена
    # users_initialization()
    db.create_all()
    print(UserModel.get_all())
    UserModel.add("User", "123", "Паша", "Соломатин")
    print(UserModel.get_all())
    app.run(port=8080, host="127.0.0.1")
