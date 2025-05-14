from flask import render_template, redirect, url_for, flash, request, session
from app import app, db
from app.forms import RegistrationFormPersonal, RegistrationFormTags, LoginForm, ProfileForm
from app.models import User, Tag, UserTag, PostTag, Post
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
import os
from datetime import datetime, timedelta


# Проверка и создание папок при запуске
os.makedirs(app.config['AVATAR_UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['POSTS_UPLOAD_FOLDER'], exist_ok=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form_personal = RegistrationFormPersonal(prefix="personal")
    form_tags = RegistrationFormTags(prefix="tags")
    form_tags.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

    if request.method == 'POST':
        if 'submit_personal' in request.form:
            if form_personal.validate_on_submit():
                session['username'] = form_personal.username.data
                session['email'] = form_personal.email.data
                session['password'] = form_personal.password.data
                return render_template('register.html', form=form_tags, step=2)
            else:
                flash('Исправьте ошибки в форме', 'error')

        elif 'submit_tags' in request.form:
            # Создаем новую форму на основе данных запроса
            form_tags = RegistrationFormTags(request.form, prefix="tags")
            form_tags.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]  # <-- Убедитесь, что это здесь

            if request.form.getlist('tags'):
                selected_tag_ids = request.form.getlist('tags')
                selected_tag_names = []

                # Получаем названия тегов на основе их ID
                for tag_id in selected_tag_ids:
                    try:
                        tag_id = int(tag_id)
                        tag = Tag.query.get(tag_id)
                        if tag:
                            selected_tag_names.append(tag.name)
                        else:
                            flash(f'Тег с ID {tag_id} не найден', 'error')
                            return render_template('register.html', form=form_tags, step=2)
                    except ValueError:
                        flash(f'Некорректный ID тега: {tag_id}', 'error')
                        return render_template('register.html', form=form_tags, step=2)

                print(f"Выбранные теги: {selected_tag_names}")  # Выводим список названий тегов

                user = User(
                    username=session.get('username'),
                    email=session.get('email')
                )
                user.set_password(session.get('password'))
                db.session.add(user)
                db.session.commit()

                # Добавляем выбранные теги
                for tag_id in selected_tag_ids:
                    # Проверка, что tag_id является целым числом
                    try:
                        tag_id = int(tag_id)
                    except ValueError:
                        flash(f'Некорректный ID тега: {tag_id}', 'error')
                        return render_template('register.html', form=form_tags, step=2)
                    # Проверка, что тег с таким ID существует в БД
                    tag = Tag.query.get(tag_id)
                    if tag:
                        user_tag = UserTag(user_id=user.id, tag_id=tag_id)
                        db.session.add(user_tag)
                    else:
                        flash(f'Тег с ID {tag_id} не найден', 'error')
                        return render_template('register.html', form=form_tags, step=2)
                db.session.commit()

                flash('Регистрация успешна!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Выберите хотя бы один тег', 'error')

    return render_template('register.html', form=form_personal, form_tags=form_tags, step=1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Неверный email или пароль.', 'error')
    return render_template('login.html', form=form)


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()  # Получаем все посты из базы данных
    return render_template('base.html', posts=posts)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Обработка аватара
        if form.avatar.data:
            avatar_filename = secure_filename(form.avatar.data.filename)
            avatar_path = os.path.join(app.config['AVATAR_UPLOAD_FOLDER'], avatar_filename)
            form.avatar.data.save(avatar_path)
            # This line is very important: store the correct path
            current_user.avatar = 'img/' + avatar_filename  # Сохраняем путь к файлу
            flash('Аватар успешно обновлен', 'success')

        # Обработка "О себе"
        current_user.bio = form.bio.data
        flash('Информация о себе успешно обновлена', 'success')

        db.session.commit()
        return render_template('profile.html', form=form)
    form.bio.data = current_user.bio
    return render_template('profile.html', form=form)


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    tags = Tag.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        selected_tags = request.form.getlist('tags')  # Убедитесь, что name="tags" в форме

        # Обработка файла
        file = request.files['file']
        file_path = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_folder = app.config['POSTS_UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join('uploads', filename).replace('\\', '/')
            file.save(os.path.join(upload_folder, filename))

        # Создание поста
        new_post = Post(
            title=title,
            content=content,
            file_path=file_path,
            author=current_user  # Используем current_user как автора
        )

        try:
            db.session.add(new_post)
            db.session.flush()  # Получаем ID поста

            # Добавляем теги
            for tag_id in selected_tags:
                if Tag.query.get(tag_id):  # Проверяем существование тега
                    post_tag = PostTag(post_id=new_post.id, tag_id=tag_id)
                    db.session.add(post_tag)

            db.session.commit()
            flash('✅ Пост успешно создан!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            db.session.rollback()
            flash(f'❌ Ошибка: {str(e)}', 'error')

    return render_template('create_post.html', tags=tags)


@app.template_filter('timeago')
def timeago(date):
    now = datetime.utcnow()
    delta = now - date
    if delta.days > 365:
        return f"{delta.days // 365} г. назад"
    if delta.days > 30:
        return f"{delta.days // 30} мес. назад"
    if delta.days > 0:
        return f"{delta.days} д. назад"
    if delta.seconds > 3600:
        return f"{delta.seconds // 3600} ч. назад"
    if delta.seconds > 60:
        return f"{delta.seconds // 60} мин. назад"
    return "только что"