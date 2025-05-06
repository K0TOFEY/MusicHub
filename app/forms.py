# print("Здесь будет разработка форм (регистрации, вход, создание постов)")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Tag


class RegistrationFormPersonal(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите пароль',
                              validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit_personal = SubmitField('Далее')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя пользователя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот email уже зарегистрирован.')


class RegistrationFormTags(FlaskForm):
    tags = SelectMultipleField('Выберите теги', coerce=int, validators=[DataRequired()],
                                widget=None)  # Remove widget=SelectMultipleField
    submit_tags = SubmitField('Зарегестрироваться')

    def __init__(self, *args, **kwargs):
        super(RegistrationFormTags, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')