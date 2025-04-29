from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[validators.DataRequired()])
    password = PasswordField('Пароль', validators=[validators.DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Пароль', validators=[validators.DataRequired(), validators.Length(min=6)])