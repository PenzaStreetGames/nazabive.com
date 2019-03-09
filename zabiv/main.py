from flask import Flask, render_template, request, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
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
def profile():
    user_model = UserModel()
    form = AddNewsForm()
    user = user_model.get(session["user_id"])
    avaform = AvaForm()
    post = PostModel()
    if request.form.get("submit_ava"):
        print("123")
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
                                        place_id=session["user_id"])
    posts = [PostModel().get(post) for post in posts_id]
    authors = [UserModel().get(post.author) for post in posts]
    avatars = [ResourceModel().get(author.avatar) for author in authors]
    likes = [len(LikeModel().get_for(post=post.id)) for post in posts]
    liked = [bool(LikeModel().get_by(author=session["user_id"], post=post.id))
             for post in posts]
    ava = ResourceModel().get(user.avatar)
    render_data = {
        "title": f"{session['user_name']} {session['user_surname']}",
        "number": len(posts),
        "name": session["user_name"],
        "surname": session["user_surname"],
        "avatar_profile": ava.path if ava else "",
        "news": posts,
        "authors": authors,
        "likes": likes,
        "liked": liked,
        "avatars": avatars,
        "form": form,
        "ava": avaform,

    }
    return render_template("profile.html", **render_data)


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
        search_words = get_form_data("search")
    render_data = {
        "title": "Друзья",
        "friends": FriendModel().get_friends(session["user_id"]),

    }
    return render_template("friends.html", **render_data)


@app.route("/dialogs", methods=['GET', 'POST'])
def dialogs():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Друзья",
        "dialogs": ChatModel().get_for(session["user_id"]),

    }
    return render_template("messages.html", **render_data)


@app.route("/dialog/<int:id>", methods=['GET', 'POST'])
def dialog(id):
    if request.method == "POST":
        pass
    render_data = {
        "title": "Переписка",
        "messages": MessageModel().get_for(id),

    }
    return render_template("dialog.html", **render_data)


@app.route("/news/", methods=['GET', 'POST'])
def news():
    if request.method == "POST":
        pass
    posts_id = PostLinkModel().get_news_tape(user=session["user_id"])
    posts = [PostModel().get(post) for post in posts_id]
    posts.sort(key=lambda post: post.date, reverse=True)
    authors = [UserModel().get(post.author) for post in posts]
    avatars = [ResourceModel().get(author.avatar) for author in authors]
    likes = [len(LikeModel().get_for(post=post.id)) for post in posts]
    liked = [bool(LikeModel().get_by(author=session["user_id"], post=post.id))
             for post in posts]
    render_data = {
        "number": len(posts),
        "title": "Новости",
        "news": posts,
        "authors": authors,
        "likes": likes,
        "liked": liked,
        "avatars": avatars
    }
    return render_template("news.html", **render_data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=8080, host="127.0.0.1")
