import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AVATAR_UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'img')  # Для аватарок
    POSTS_UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')  # Для файлов постов