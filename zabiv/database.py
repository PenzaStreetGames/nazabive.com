from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from main import db

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nazabive.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    app.config['SECRET_KEY'] = 'dryandex_corp'


class User(db.Model):
    """пользователи"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.Integer, nullable=False, default=1)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())


class Post(db.Model):
    """новости"""
    id = db.Column(db.Integer, primary_key=True)
    author_type = db.Column(db.Integer, nullable=False)
    author = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())


class Chat(db.Model):
    """беседы"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())


class Group(db.Model):
    """группы"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.Integer, nullable=False, default=1)


class Resource(db.Model):
    """ресурсы"""
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), unique=False, nullable=False)
    path = db.Column(db.String(120), unique=True, nullable=True)
    name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.Integer, nullable=False)


class Message(db.Model):
    """сообщения"""
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    chat = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now())


class Like(db.Model):
    """оценки"""
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, nullable=False)
    author = db.Column(db.Integer, nullable=False)


class ChatMember(db.Model):
    """участинки бесед"""
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    chat = db.Column(db.Integer, nullable=False)
    invite_time = db.Column(db.DateTime, nullable=False, default=datetime.now())


class FriendRequest(db.Model):
    """запросы в друзья"""
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.Integer, nullable=False)


class Friend(db.Model):
    """друзья"""
    id = db.Column(db.Integer, primary_key=True)
    base_user = db.Column(db.Integer, nullable=False)
    friend = db.Column(db.Integer, nullable=False)


class GroupMember(db.Model):
    """участники группы"""
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    group = db.Column(db.Integer, nullable=False)


class PostLink(db.Model):
    """ссылки на новости"""
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, nullable=False)
    place = db.Column(db.String(20), nullable=False)
    place_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())


class ResourceLink(db.Model):
    """ссылки на ресурсы"""
    id = db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.Integer, nullable=False)
    place = db.Column(db.String(20), nullable=False)
    place_id = db.Column(db.Integer, nullable=False)


class Description(db.Model):
    """описания пользователей или групп"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
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
            DescriptionModel().create(text="Описание отсутствует", place="user",
                                      place_id=new_user.id)
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

    def set_avatar(self, user, resource):
        """изменение портрета пользователя"""
        user = UserModel().get(user)
        resource = ResourceModel().get(resource)
        if resource.category == "image":
            user.avatar = resource.id
        db.session.commit()

    def search(self, name="", surname=""):
        """поиск пользователя по имени и/или фамилии"""
        if name and not surname:
            users = User.query.filter(User.name.like(f"%{name}%")).all()
        elif not name and surname:
            users = User.query.filter(User.surname.like(f"%{surname}%")).all()
        elif name and surname:
            users = User.query.filter(User.name.like(f"%{name}%"),
                                      User.surname.like(f"%{surname}%")).all()
        else:
            users = User.query.all()
        return users


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
            FriendRequest.sender == sender,
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
        FriendModel().create_connection(friend_request.sender,
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
            Friend.base_user == user_1,
            Friend.friend == user_2).first()
        return request

    def get_friends(self, user):
        """список друзей"""
        friends = Friend.query.filter(Friend.base_user == user).all()
        return friends

    def delete_friend(self, user_1, user_2):
        """удалить друга"""
        relation_1 = FriendModel().get_relation(user_1, user_2)
        relation_2 = FriendModel().get_relation(user_2, user_1)
        try:
            Friend.query.filter(Friend.id == relation_1.id).delete()
            Friend.query.filter(Friend.id == relation_2.id).delete()
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
        member = ChatMember.query.filter(ChatMember.user == user,
                                         ChatMember.chat == chat).first()
        if not member:
            return
        return member

    def update_invite(self, id):
        """обновление времени посещения беседы"""
        member = ChatMember.query.filter(ChatMember.id == id).first()
        member.invite_time = datetime.now()
        db.session.commit()

    def delete(self, id):
        """удаление участника беседы"""
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
        return chat

    def get(self, id):
        """получение чата по id"""
        chat = Chat.query.filter(Chat.id == id).first()
        if not chat:
            return None
        return chat

    def exists_dialog(self, user_1, user_2):
        """существует ли диалог между пользователями"""
        chats_1 = set([member.chat for member in ChatModel().get_for(user_1)])
        chats_2 = set([member.chat for member in ChatModel().get_for(user_2)])
        common_chats = list(chats_1.intersection(chats_2))
        chats = [ChatModel().get(chat) for chat in common_chats]
        dialog = list(filter(lambda chat: chat.private, chats))
        if dialog:
            return dialog[0]
        else:
            return None

    def get_for(self, user):
        """получение чатов пользователя"""
        chats = ChatMember.query.filter(ChatMember.user == user).all()
        return chats

    def get_of(self, chat):
        """получение участников группы"""
        users = ChatMember.query.filter(ChatMember.chat == chat).all()
        return users


class MessageModel:
    """работа с сообщениями"""

    def create(self, user, chat, text):
        """отправка сообщения"""
        message = Message(sender=user, chat=chat, text=text)
        db.session.add(message)
        db.session.commit()

    def get(self, id):
        """получение сообщения по id"""
        message = Message.query.filter(Message.id == id).first()
        if not message:
            return None
        return message

    def get_for(self, chat):
        """список сообщений беседы"""
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
        message = MessageModel().get(id)
        if not message:
            return
        message.text = new_text
        db.session.commit()

    def new_messages(self, user, chat):
        """список непрочитанных сообщений"""
        member = ChatMemberModel().get(user, chat)
        messages = Message.query.filter(Message.chat == chat,
                                        Message.time > member.invite_time).all()
        return messages

    def get_latest(self, chat):
        """получение последнего сообщение беседы"""
        message = Message.query.filter(Message.chat == chat).group_by(
            Message.time).all()
        if message:
            return message[-1]
        return None


class PostLinkModel:
    """работа с ссылками на новости"""

    def create(self, post, place, place_id):
        """создание ссылки на новость"""
        link = PostLink(post=post.id, place=place, place_id=place_id)
        db.session.add(link)
        db.session.commit()
        return link

    def create_post(self, place, place_id, content):
        """публикация новости"""
        post = PostModel().create(author_type=place, author=place_id,
                                  content=content)
        PostLinkModel().create(post=post, place=place, place_id=place_id)

    def repost(self, id, place, place_id):
        """создание ссылки на новость"""
        PostLinkModel().create(post=id, place=place, place_id=place_id)

    def get_news(self, place, place_id):
        """список новостей"""
        post_links = PostLink.query.filter(PostLink.place == place,
                                           PostLink.place_id == place_id).all()
        posts = [post.post for post in post_links]
        return posts

    def get_news_tape(self, user):
        """новостная лента пользователя"""
        news = PostLinkModel().get_news("user", user)
        friends = FriendModel().get_friends(user)
        for friend in friends:
            news += PostLinkModel().get_news("user", friend.friend)
        groups = [member.group for member in GroupModel().get_for(user)]
        for group in groups:
            news += PostLinkModel().get_news(place="group", place_id=group)
        return news


class PostModel:
    """работа с новостями"""

    def create(self, author_type, author, content):
        """создание новости"""
        post = Post(author_type=author_type, author=author, content=content)
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
        post = PostModel().get(id)
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
        like = Like.query.filter(Like.author == author,
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
            like = Like.query.filter(Like.author == author,
                                     Like.post == post).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()


class GroupMemberModel:
    """работа с участниками групп"""

    def create(self, user, group):
        """создание участника группы"""
        member = GroupMember(user=user, group=group)
        db.session.add(member)
        db.session.commit()

    def get_by(self, user, group):
        """получение участника группы по пользователю и группе"""
        member = GroupMember.query.filter(GroupMember.user == user,
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
    """работа с группами"""

    def create(self, *users, name="Unnamed"):
        """создание группы"""
        group = Group(name=name)
        db.session.add(group)
        db.session.commit()
        DescriptionModel().create(text="Описание отсутствует", place="group",
                                  place_id=group.id)
        db.session.commit()
        for user in users:
            member = GroupMember(user=user, group=group.id)
            db.session.add(member)
        db.session.commit()
        return group

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

    def search(self, name):
        """поиск группы по имени"""
        groups = Group.query.filter(Group.name.like(f"%{name}%")).all()
        return groups

    def set_avatar(self, group, resource):
        """изменение портрета пользователя"""
        group = GroupModel().get(group)
        resource = ResourceModel().get(resource)
        if resource.category == "image":
            group.avatar = resource.id
        db.session.commit()


class ResourceModel:
    """работа с ресурсами"""

    def choose_category(self, resolution):
        """выбрать категорию ресурса по его разрешению"""
        categories = {"image": ["png", "jpg", "gif"],
                      "music": ["mp3", "wav", "ogg", "oga", "ogx"],
                      "video": ["mp4", "avi", "mpg"],
                      "document": ["all other resolutions"]}
        if resolution in categories["image"]:
            return "image"
        elif resolution in categories["music"]:
            return "music"
        elif resolution in categories["video"]:
            return "video"
        else:
            return "document"

    def get_all(self):
        files = Resource.query.filter().all()
        return files

    def create(self, server_name, name, file, author):
        """создание файла на сервере"""
        resolution = name.split(".")[-1]
        filename = ".".join(name.split(".")[:-1])
        category = ResourceModel().choose_category(name.split(".")[-1])
        resource = Resource(author=author, name=server_name, category=category)
        db.session.add(resource)
        db.session.commit()
        file_id = resource.id
        path = f"static/resources/{file_id}.{resolution}"
        file.save(path)
        resource.path = path
        db.session.commit()
        return resource

    def get(self, id):
        """получение файла по id"""
        resource = Resource.query.filter(Resource.id == id).first()
        if not resource:
            return
        return resource

    def get_for(self, user, category=""):
        """список файлов пользователя"""
        if category:
            resources = Resource.query.filter(
                Resource.author == user, Resource.category == category).all()
        else:
            resources = Resource.query.filter(Resource.author == user).all()
        return resources

    def search(self, name, category=""):
        """поиск файла по имени"""
        if category:
            resources = Resource.query.filter(
                Resource.name.like(f"%{name}%"),
                Resource.category == category).all()
        else:
            resources = Resource.query.filter(
                Resource.name.like(f"%{name}%")).all()
        return resources


class ResourceLinkModel:
    """работа с ссылками на ресурсы"""

    def create(self, resource, place, place_id):
        """создание ссылки на ресурс"""
        link = ResourceLink(resource=resource.id, place=place,
                            place_id=place_id)
        db.session.add(link)
        db.session.commit()
        return link

    def get_for(self, place, place_id):
        """список ресурсов этого объекта"""
        resources = ResourceLink.query.filter(
            ResourceLink.place == place,
            ResourceLink.place_id == place_id).all()
        return resources


class DescriptionModel:
    """работа с описаниями"""

    def create(self, text, place, place_id):
        """создания описания"""
        description = Description(text=text, place=place, place_id=place_id)
        db.session.add(description)
        db.session.commit()

    def get(self, id):
        """получение описания по id"""
        description = Description.query.filter(Description.id == id).first()

    def get_for(self, place, place_id):
        """получение описания по месту размещения"""
        description = Description.query.filter(
            Description.place == place,
            Description.place_id == place_id).first()
        if not description:
            return
        return description

    def change(self, id, new_text):
        """изменение существующего описания"""
        description = Description.query.filter(Description.id == id).first()
        description.text = new_text
        db.session.commit()

    def delete(self, id):
        """удаление описания по id"""
        try:
            Description.query.filter(Description.id == id).delete()
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()


def init_base():
    UserModel().add("User", "123", "Паша", "Соломатин")
    UserModel().add("Login", "123", "Захар", "Тугушев")
    UserModel().add("Medal", "123", "Лёша", "Медведев")


if __name__ == '__main__':
    db.create_all()
    init_base()
