from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired
from flask import Flask, redirect, request, render_template, session
from datetime import datetime

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
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())


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
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())


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
    invite_time = db.Column(db.DateTime, nullable=False, default=datetime.now())


class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.Integer, nullable=False)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_user = db.Column(db.Integer, nullable=False)
    friend = db.Column(db.Integer, nullable=False)


class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    group = db.Column(db.Integer, nullable=False)


class PostLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, nullable=False)
    place = db.Column(db.String(20), nullable=False)
    place_id = db.Column(db.Integer, nullable=False)


class ResourceLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.Integer, nullable=False)
    place = db.Column(db.String(20), nullable=False)
    place_id = db.Column(db.Integer, nullable=False)


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

    def get(self, id):
        """получеие пользователя по id"""
        user = User.query.filter(User.id == id).first()
        if not user:
            return
        return user

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
        """проверка на существование пользователя"""
        user = User.query.filter(User.username == username).first()
        if not user:
            return "Not found"
        if user.password != password:
            return "Wrong password"
        return user

    def create_post(self, user, content):
        """публикация новости у пользователя на странице"""
        post = PostModel.create(author=user, content=content)
        PostLinkModel.create(post=post.id, place="user", place_id=user)

    def repost(self, id, user):
        """создание ссылки на новость на странице пользователя"""
        PostLinkModel.create(post=id, place="user", place_id=user)

    def get_news(self, user):
        """список новостей пользователя"""
        post_links = PostLink.query.filter(PostLink.place == "user" and
                                           PostLink.place_id == user).all()
        posts = [post.post for post in post_links]
        return posts


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

    def get(self, user, chat):
        """получение участника группы по пользователю и группе"""
        member = ChatMember.query.filter(ChatMember.user == user and
                                         ChatMember.chat == chat).first()
        if not member:
            return "Not found"
        return member

    def update_invite(self, id):
        """обновление времени посещения беседы"""
        member = ChatMember.query.filter(ChatMember.id == id).first()
        member.invite_time = datetime.now()
        db.session.commit()

    def delete(self, id):
        """удаление участника группы"""
        try:
            ChatMember.query.filter(ChatMember.id == id).delete()
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

    def get(self, id):
        """получение чата по id"""
        chat = Chat.query.filter(Chat.id == id).first()
        if not chat:
            return None
        return chat

    def get_for(self, user):
        """получение чатов пользователя"""
        chats = ChatMember.query.filter(ChatMember.user == user).all()
        return chats

    def get_of(self, chat):
        """получение участников группы"""
        users = ChatMember.query.filter(ChatMember.chat == chat).all()
        return users


class MessageModel:

    def create(self, user, chat, text):
        """отправка сообщения"""
        message = Message(user=user, chat=chat, text=text)
        db.session.add(message)
        db.session.commit()

    def get(self, id):
        """получение сообщения по id"""
        message = Message.query.filter(Message.id == id).first()
        if not message:
            return None
        return message

    def get_for(self, chat):
        """список сообщений группы"""
        messages = Message.query.filter(Message.chat == chat).all()
        return messages

    def delete(self, id):
        """удаление сообщения"""
        try:
            Message.query.filter(Message.id == id).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()

    def edit(self, id, new_text):
        """редактирование сообщения"""
        message = MessageModel.get(id)
        if not message:
            return
        message.text = new_text
        db.session.commit()

    def new_messages(self, user, chat):
        """список непрочитанных сообщений"""
        user = UserModel.get(user)
        messages = Message.query.filter(Message.chat == chat and
                                        Message.time > user.time).all()
        return messages


class PostLinkModel:

    def create(self, post, place, place_id):
        """создание ссылки на новость"""
        link = PostLink(post=post.id, place=place, place_id=place_id)
        db.session.add(link)
        db.session.commit()
        return link

    def create_post(self, place, place_id, content):
        """публикация новости в нужном месте"""
        post = PostModel.create(author=user, content=content)
        PostLinkModel.create(post=post.id, place="user", place_id=user)

    def repost(self, id, user):
        """создание ссылки на новость в нужном объекте"""
        PostLinkModel.create(post=id, place="user", place_id=user)

    def get_news(self, user):
        """список новостей в нужном объекте"""
        post_links = PostLink.query.filter(PostLink.place == "user" and
                                           PostLink.place_id == user).all()
        posts = [post.post for post in post_links]
        return posts


class PostModel:

    def create(self, author, content):
        """создание новости"""
        post = Post(author=author, content=content)
        db.session.add(post)
        db.session.commit()
        return post

    def get(self, id):
        """получение новости по id"""
        post = Post.query.filter(Post.id == id).first()
        if not post:
            return
        return post

    def edit(self, id, new_content):
        """редактирование новости"""
        post = PostModel.get(id)
        if not post:
            return "Not found"
        post.content = new_content
        db.session.commit()


class LikeModel:
    """обработка оценок"""

    def create(self, author, post):
        """создание оценки"""
        like = Like(author=author, post=post)
        db.session.add(like)
        db.session.commit()

    def get(self, id):
        """получение оценки по id"""
        like = Like.query.filter(Like.id == id).first()
        if not like:
            return
        return like

    def get_by(self, author, post):
        """получение оценки по автору и новости"""
        like = Like.query.filter(Like.author == author and
                                 Like.post == post).first()
        if not like:
            return
        return like

    def get_for(self, post):
        """список оценок к новости"""
        likes = Like.query.filter(Like.post == post).all()
        return likes

    def delete(self, author, post):
        """удаление оценки по автору и новости"""
        try:
            like = Like.query.filter(Like.author == author and
                                     Like.post == post).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()


class GroupMemberModel:

    def create(self, user, group):
        """создание участника группы"""
        member = GroupMember(user=user, group=group)
        db.session.add(member)
        db.session.commit()

    def get_by(self, user, group):
        """получение участника группы по пользователю и группе"""
        member = GroupMember.query.filter(GroupMember.user == user and
                                          GroupMember.group == group).first()
        if not member:
            return
        return member

    def get(self, id):
        """получение участника группы по id"""
        member = GroupMember.query.filter(GroupMember.id == id).first()
        if not member:
            return
        return member

    def delete(self, id):
        """удаление участника группы"""
        try:
            GroupMember.query.filter(GroupMember.id == id).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()


class GroupModel:

    def create(self, *users, name="Unnamed"):
        """создание группы"""
        group = Group(name=name)
        db.session.add(group)
        db.session.commit()
        for user in users:
            member = Group(user=user, group=group.id)
            db.session.add(member)
        db.session.commit()

    def get(self, id):
        """получение группы по id"""
        group = Group.query.filter(Group.id == id).first()
        if not group:
            return
        return group

    def get_for(self, user):
        """получение групп пользователей"""
        groups = GroupMember.query.filter(GroupMember.user == user).all()
        return groups

    def get_of(self, group):
        """получение участников группы"""
        members = GroupMember.query.filter(GroupMember.group == group).all()
        return members

    def create_post(self, group, content):
        """публикация новости в группе на странице"""
        post = PostModel.create(author=group, content=content)
        PostLinkModel.create(post=post.id, place="group", place_id=group)

    def repost(self, id, group):
        """создание ссылки на новость на странице группы"""
        PostLinkModel.create(post=id, place="group", place_id=group)

    def get_news(self, group):
        """список новостей группы"""
        post_links = PostLink.query.filter(PostLink.place == "group" and
                                           PostLink.place_id == group).all()
        posts = [post.post for post in post_links]
        return posts




if __name__ == '__main__':
    # первичная инициализация, уже проведена
    # users_initialization()
    db.create_all()
    print(UserModel.get_all())
    UserModel.add("User", "123", "Паша", "Соломатин")
    print(UserModel.get_all())
    app.run(port=8080, host="127.0.0.1")
