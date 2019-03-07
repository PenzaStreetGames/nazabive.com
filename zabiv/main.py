from flask import Flask, render_template, request, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AuthForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ImageForm(FlaskForm):
    img = FileField('Изображение', validators=[DataRequired()])
    text = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class VideoForm(FlaskForm):
    video = FileField('Изображение', validators=[DataRequired()])
    text = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AudioForm(FlaskForm):
    audio = FileField('Аудиозапись', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class DocumentForm(FlaskForm):
    document = FileField('Документ', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class Config:
    DIR_IMG = "/static/images/"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dryndex_corp'


# dbo = DB()


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Главная",
        "form": AuthForm()

    }
    return render_template("index.html", **render_data)


@app.route("/reg", methods=['GET', 'POST'])
def reg():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Регистрация",

    }
    return render_template("reg.html", **render_data)


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Регистрация",
        "avatar_profile": Config.DIR_IMG + "ava.jpg",
        "form": AddNewsForm()

    }
    return render_template("profile.html", **render_data)


@app.route("/photo", methods=['GET', 'POST'])
def photo():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Фотографии",
        "form": ImageForm()

    }
    return render_template("photo.html", **render_data)


@app.route("/videos", methods=['GET', 'POST'])
def videos():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Видеозаписи",
        "form": VideoForm()

    }
    return render_template("video.html", **render_data)


@app.route("/audio", methods=['GET', 'POST'])
def audio():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Аудиозаписи",
        "form": AudioForm()

    }
    return render_template("audio.html", **render_data)


@app.route("/documents", methods=['GET', 'POST'])
def documents():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Документы",
        "form": DocumentForm()

    }
    return render_template("documents.html", **render_data)


@app.route("/friends", methods=['GET', 'POST'])
def friends():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Друзья",

    }
    return render_template("friends.html", **render_data)


@app.route("/dialogs", methods=['GET', 'POST'])
def dialogs():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Друзья",

    }
    return render_template("messages.html", **render_data)


@app.route("/dialog/<int:id>", methods=['GET', 'POST'])
def dialog(id):
    if request.method == "POST":
        pass
    render_data = {
        "title": "Переписка",

    }
    return render_template("dialog.html", **render_data)


@app.route("/news/", methods=['GET', 'POST'])
def news():
    if request.method == "POST":
        pass
    render_data = {
        "title": "Новости",

    }
    return render_template("news.html", **render_data)


if __name__ == '__main__':
    app.run(port=8080, host="127.0.0.1")
