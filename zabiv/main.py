from flask import Flask, render_template, request, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField, BooleanField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import *


class AddNewsForm(FlaskForm):
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    document = FileField('Документ', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AuthForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ImageForm(FlaskForm):
    img = FileField('Изображение', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class VideoForm(FlaskForm):
    video = FileField('Изображение', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AudioForm(FlaskForm):
    audio = FileField('Аудиозапись', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class DocumentForm(FlaskForm):
    document = FileField('Документ', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class SearchForm(FlaskForm):
    login = StringField('', validators=[DataRequired()])
    submit = SubmitField('Найти')


class AddGroupForm(FlaskForm):
    name = StringField('Название: ', validators=[DataRequired()])
    submit = SubmitField('Создать')


class AddDialogGroupForm(FlaskForm):
    name = StringField('Название: ', validators=[DataRequired()])
    submit = SubmitField('Создать')


class AddUserToDialogForm(FlaskForm):
    friends = SelectField('Выберете участников', choices=[  # cast val as int
        (0, '1'),
        (1, '2'),
    ])
    submit = SubmitField('Создать')


class AvaForm(FlaskForm):
    document = FileField('', validators=[DataRequired()])
    submit_ava = SubmitField('Сменить аватарку')


class Config:
    DIR_IMG = "/static/images/"


def get_form_data(*params):
    return [request.form.get(param) for param in params]


def is_auth():
    return "user_login" in session \
           and UserModel().exists(session["user_login"], session["user_password"]) != "Not found"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nazabive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dryandex_corp'


# dbo = DB()


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if is_auth():
        return redirect("/profile")
    auth = AuthForm()
    if request.method == "POST":
        if auth.validate_on_submit():
            login, password = get_form_data("login", "password")
            user = UserModel()
            user_object = user.exists(login, password)
            if user_object and user_object != "Not found":
                session["user_id"] = user_object.id
                session["user_login"] = user_object.username
                session["user_password"] = user_object.password
                session["user_name"] = user_object.name
                session["user_surname"] = user_object.surname

                return redirect("/profile")

    render_data = {
        "title": "Главная",
        "form": auth

    }
    return render_template("index.html", **render_data)


@app.route("/logout")
def logout():
    session.pop('user_login', 0)
    session.pop('user_password', 0)
    session.pop('user_name', 0)
    session.pop('user_surname', 0)
    session.pop('user_id', 0)
    return redirect('/')


@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if is_auth():
        return redirect("/profile")
    if request.method == "POST":
        name, surname, login, password = get_form_data("name", "surname", "login", "password")
        if login and password:
            user = UserModel()
            user.add(login, password, name, surname)
            user_object = user.exists(login, password)
            print(user_object)
            if user_object and user_object != "Not found":
                session["user_id"] = user_object.id
                session["user_login"] = user_object.username
                session["user_password"] = user_object.password
                session["user_name"] = user_object.name
                session["user_surname"] = user_object.surname

                return redirect("/profile")

    render_data = {
        "title": "Регистрация",

    }
    return render_template("reg.html", **render_data)


@app.route("/profile", methods=['GET', 'POST'])
def profile_me():
    return redirect(f"/profile/{session['user_id']}")


@app.route("/profile/<id>", methods=['GET', 'POST'])
def profile(id):
    user_model = UserModel()
    form = AddNewsForm()
    user = user_model.get(id)
    avaform = AvaForm()
    post = PostModel()
    title = f"{user.name} {user.surname}"

    if request.form.get("submit_ava"):
        file = request.files.get("document")
        res = ResourceModel().create(file.filename, file, session["user_id"])
        link = ResourceLinkModel().create(res, "user", session["user_id"])
        user_model.set_avatar(session["user_id"], res.id)
    if form.validate_on_submit():
        content = get_form_data("content")[0]
        print(type(content), content)
        PostLinkModel().create_post(place="user",
                                    place_id=session["user_id"],
                                    content=content)
    posts_id = PostLinkModel().get_news(place="user",
                                        place_id=user.id)
    posts = [PostModel().get(post) for post in posts_id]
    posts.sort(key=lambda post: post.date, reverse=True)
    dates = [str(post.date)[:19] for post in posts]
    authors = [UserModel().get(post.author) for post in posts]
    avatars = [ResourceModel().get(author.avatar) for author in authors]
    likes = [len(LikeModel().get_for(post=post.id)) for post in posts]
    liked = [bool(LikeModel().get_by(author=session["user_id"], post=post.id))
             for post in posts]
    ava = ResourceModel().get(user.avatar)
    is_friends = bool(FriendModel().get_relation(user_1=session["user_id"],
                                                 user_2=user.id))
    render_data = {
        "title": title,
        "number": len(posts),
        "name": user.name,
        "surname": user.surname,
        "avatar_profile": ava.path if ava else "static/images/no_photo.png",
        "news": posts,
        "authors": authors,
        "posts_id": posts_id,
        "likes": likes,
        "liked": liked,
        "avatars": avatars,
        "form": form,
        "ava": avaform,
        "user": user,
        "is_friend": is_friends, # Друзья ли они?
        "page_profile": True,
        "dates": dates

    }
    return render_template("profile.html", **render_data)


@app.route("/group/<int:id>", methods=['GET', 'POST'])
def group(id):
    form = AddNewsForm()
    group = GroupModel().get(id)
    form_add_user = AddUserToDialogForm()

    if form.validate_on_submit():
        content = get_form_data("content")[0]
        PostLinkModel().create_post(place="group",
                                    place_id=id,
                                    content=content)
    user = UserModel().get(session["user_id"])
    posts_id = PostLinkModel().get_news(place="group",
                                        place_id=group.id)
    posts = [PostModel().get(post) for post in posts_id]
    posts.sort(key=lambda post: post.date, reverse=True)
    dates = [str(post.date)[:19] for post in posts]
    authors = [UserModel().get(post.author) for post in posts]
    avatars = [ResourceModel().get(author.avatar) for author in authors]
    likes = [len(LikeModel().get_for(post=post.id)) for post in posts]
    liked = [bool(LikeModel().get_by(author=session["user_id"], post=post.id))
             for post in posts]
    ava = ResourceModel().get(group.avatar)
    in_group = GroupMemberModel().get_by(user=user.id, group=id)
    render_data = {
        "user": user,
        "title": group.name,
        "number": len(posts),
        "name": group.name,
        "avatar_group": ava.path,
        "news": posts,
        "authors": authors,
        "likes": likes,
        "liked": liked,
        "avatars": avatars,
        "form": form,
        "form_add_user": form_add_user,
        "group": group,
        "in_group": in_group,  # В группе ли пользователь?
        "page_group": True,
        "dates": dates,
        "session": session

    }
    return render_template("group.html", **render_data)


@app.route("/groups", methods=['GET', 'POST'])
def groups():
    form_add_group = AddGroupForm()
    if request.method == "POST":
        search_words = get_form_data("search")
    if form_add_group.validate_on_submit():
        name = form_add_group.name.data
        GroupModel().create(session["user_id"], name=name)
    groups_id = GroupModel().get_for(session["user_id"])
    groups_list = [GroupModel().get(group.group) for group in groups_id]
    avatars = [ResourceModel().get(group.avatar) for group in groups_list]
    render_data = {
        "title": "Группы",
        "groups": groups_list,
        "groups_number": len(groups_list),
        "avatars": avatars,
        "form_add_group": form_add_group,
        "page_groups": True,

    }
    return render_template("groups.html", **render_data)


@app.route("/photo", methods=['GET', 'POST'])
def photo():
    if not is_auth():
        return redirect("/")
    if request.method == "POST":
        file = request.files["img"]
        filename = file.filename
        resource = ResourceModel().create(name=filename, file=file,
                                          author=session["user_id"])
        ResourceLinkModel().create(resource=resource, place="user",
                                   place_id=session["user_id"])
    render_data = {
        "title": "Фотографии",
        "photos": ResourceModel().get_for(session["user_id"], category="image"),
        "form": ImageForm()

    }
    return render_template("photo.html", **render_data)


@app.route("/videos", methods=['GET', 'POST'])
def videos():
    if not is_auth():
        return redirect("/")
    if request.method == "POST":
        file = request.files["video"]
        filename = file.filename
        resource = ResourceModel().create(name=filename, file=file,
                                          author=session["user_id"])
        ResourceLinkModel().create(resource=resource, place="user",
                                   place_id=session["user_id"])
    render_data = {
        "title": "Видеозаписи",
        "videos": ResourceModel().get_for(session["user_id"], category="video"),
        "form": VideoForm()

    }
    return render_template("video.html", **render_data)


@app.route("/audio", methods=['GET', 'POST'])
def audio():
    if not is_auth():
        return redirect("/")
    if request.method == "POST":
        file = request.files["audio"]
        filename = file.filename
        resource = ResourceModel().create(name=filename, file=file,
                                          author=session["user_id"])
        ResourceLinkModel().create(resource=resource, place="user",
                                   place_id=session["user_id"])
    render_data = {
        "title": "Аудиозаписи",
        "audios": ResourceModel().get_for(session["user_id"], category="audio"),
        "form": AudioForm()

    }
    return render_template("audio.html", **render_data)


@app.route("/documents", methods=['GET', 'POST'])
def documents():
    if not is_auth():
        return redirect("/")
    if request.method == "POST":
        file = request.files["document"]
        filename = file.filename
        resource = ResourceModel().create(name=filename, file=file,
                                          author=session["user_id"])
        ResourceLinkModel().create(resource=resource, place="user",
                                   place_id=session["user_id"])
    render_data = {
        "title": "Документы",
        "documents": ResourceModel().get_for(session["user_id"],
                                             category="document"),
        "form": DocumentForm()

    }
    return render_template("documents.html", **render_data)


@app.route("/friends", methods=['GET', 'POST'])
def friends():
    if request.method == "POST":
        search_words = get_form_data("search")[0].split()[:2]
        searched_friends = UserModel().search(name=search_words[0]) + \
                            UserModel().search(surname=search_words[0])
        if len(search_words) == 2:
            searched_friends += UserModel().search(
                name=search_words[0], surname=search_words[1]) + \
                UserModel().search(
                    name=search_words[1], surname=search_words[0])
        searched_friends = list(set(searched_friends))
        real_friends, searched_people = [], []
        for friend in searched_friends:
            if bool(FriendModel().get_relation(user_1=session["user_id"],
                                               user_2=friend.id)):
                real_friends += [friend]
            else:
                searched_people += [friend]
        real_avatars = [ResourceModel().get(author.avatar)
                        for author in real_friends]
        other_avatars = [ResourceModel().get(author.avatar)
                         for author in searched_people]
        search = True
    else:
        friends_id = FriendModel().get_friends(session["user_id"])
        real_friends = [UserModel().get(user.friend) for user in friends_id]
        searched_people = []
        real_avatars = [ResourceModel().get(author.avatar)
                        for author in real_friends]
        other_avatars = []
        search = False
    render_data = {
        "title": "Друзья",
        "search": search,
        "friend_number": len(real_friends),
        "friends": real_friends,
        "friends_avatars": real_avatars,
        "people_number": len(searched_people),
        "people": searched_people,
        "other_avatars": other_avatars

    }
    return render_template("friends.html", **render_data)


@app.route("/dialogs", methods=['GET', 'POST'])
def dialogs():
    form_add_group = AddDialogGroupForm()
    if request.method == "POST":
        pass
    chats_id = ChatModel().get_for(session["user_id"])
    chats = [ChatModel().get(member.chat) for member in chats_id]
    messages = [MessageModel().get_latest(chat.id) for chat in chats]
    authors_id = [message.sender if message else None for message in messages]
    authors = [UserModel().get(author) if author else None
               for author in authors_id]
    avatars = [ResourceModel().get(author.avatar) if author else None
               for author in authors]
    render_data = {
        "title": "Друзья",
        "chats_number": len(chats),
        "chats": chats,
        "avatars": avatars,
        "messages": messages,
        "form_add_group": form_add_group,
        "page_dialogs": True,

    }
    return render_template("messages.html", **render_data)


@app.route("/dialog/<int:id>", methods=['GET', 'POST'])
def dialog(id):
    form_add_user = AddUserToDialogForm()
    if request.method == "POST":
        pass
    messages = MessageModel().get_for(id)
    messages.sort(key=lambda message: message.time)
    authors_id = [message.sender for message in messages]
    authors = [UserModel().get(user) for user in authors_id]
    avatars_id = [user.avatar for user in authors]
    avatars = [ResourceModel().get(avatar) for avatar in avatars_id]
    render_data = {
        "title": "Переписка",
        "messages": messages,
        "authors": authors,
        "avatars": avatars_id,
        "form_add_user": form_add_user,
        "page_dialog": True,
        "message_number": len(messages)

    }
    return render_template("dialog.html", **render_data)


@app.route("/get_dialog/<int:id>", methods=["GET", "POST"])
def get_dialog(id):
    if request.method == "POST":
        pass
    user = UserModel().get(id)
    dialog = ChatModel().exists_dialog(session["user_id"], user.id)
    if not dialog:
        dialog = ChatModel().create(
            session["user_id"], id,
            name=f"{session['user_name']} & {user.name}", private=True)
    return redirect(f"/dialog/{dialog.id}")


@app.route("/news/", methods=['GET', 'POST'])
def news():
    if request.method == "POST":
        pass
    posts_id = PostLinkModel().get_news_tape(user=session["user_id"])
    posts = [PostModel().get(post) for post in posts_id]
    posts.sort(key=lambda post: post.date, reverse=True)
    dates = [str(post.date)[:19] for post in posts]
    authors = [UserModel().get(post.author) for post in posts]
    avatars = [ResourceModel().get(author.avatar) for author in authors]
    likes = [len(LikeModel().get_for(post=post.id)) for post in posts]
    liked = [bool(LikeModel().get_by(author=session["user_id"], post=post.id))
             for post in posts]
    render_data = {
        "number": len(posts),
        "title": "Новости",
        "news": posts,
        "posts_id": posts_id,
        "authors": authors,
        "likes": likes,
        "liked": liked,
        "avatars": avatars,
        "dates": dates
    }
    return render_template("news.html", **render_data)


@app.route("/like", methods=['GET', 'POST'])
def like():
    if request.method == "POST":
        user = session["user_id"]
        post = request.form["post_id"]
        like = LikeModel().get_by(user, post)
        if not like:
            LikeModel().create(author=user, post=post)
        else:
            LikeModel().delete(author=user, post=post)
        return "liked"

    return redirect("/")


@app.route("/setfriend", methods=['POST'])
def setfriend():
    if request.method == "POST":
        print("aaa")
        user = UserModel().get(session["user_id"])
        friend = UserModel().get(request.form["user"])
        is_friends = FriendModel().get_relation(user_1=user.id, user_2=friend.id)
        if is_friends:
            FriendModel().delete_friend(user_1=user.id, user_2=friend.id)
        else:
            FriendModel().create_connection(user_1=user.id, user_2=friend.id)

        return "friendship changed"
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=8080, host="127.0.0.1")
