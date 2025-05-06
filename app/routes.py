from flask import render_template, redirect, url_for, flash, request, session
from app import app, db
from app.forms import RegistrationFormPersonal, RegistrationFormTags, LoginForm
from app.models import User, Tag
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/register', methods=['GET', 'POST'])
def register():
    form_personal = RegistrationFormPersonal(prefix="personal")
    form_tags = RegistrationFormTags(prefix="tags")

    # Загружаем теги из БД, чтобы отобразить в форме
    form_tags.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

    if request.method == 'POST':
        if 'submit_personal' in request.form and form_personal.validate_on_submit():
            print(form_personal.errors)
            session['username'] = form_personal.username.data
            session['email'] = form_personal.email.data
            session['password'] = form_personal.password.data
            return render_template('register.html', form=form_tags, step=2)

        if 'submit_tags' in request.form and form_tags.validate_on_submit():
            username = session.get('username')
            email = session.get('email')
            password = session.get('password')

            if not username or not email or not password:
                flash('Пожалуйста, заполните личные данные.', 'error')
                return redirect(url_for('register'))

            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            selected_tags = form_tags.tags.data

            for tag_id in selected_tags:
                tag = Tag.query.get(tag_id)
                if tag:
                    user.tags.append(tag)

            db.session.commit()

            flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form_personal, step=1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Успешный вход
            session['username'] = user.username  # Сохраняем имя пользователя в сессии
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))  # Перенаправляем на главную страницу
        else:
            flash('Неверный email или пароль.', 'error')
    return render_template('login.html', form=form)


@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:  # Проверяем, есть ли username в сессии
        return render_template('index.html', username=session['username'])  # Отображаем главную страницу с именем пользователя
    else:
        return render_template('base.html')  # Перенаправляем на страницу входа, если пользователь не залогинен


@app.route('/logout')
def logout():
    session.pop('username', None) # Удаляем имя пользователя из сессии
    return redirect(url_for('index')) # Перенаправляем на страницу входа