from flask import Flask, render_template, request, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AuthForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


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



if __name__ == '__main__':
    app.run(port=8080, host="127.0.0.1")
