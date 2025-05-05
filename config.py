# print('Здесь будет конфигурация приложения')
import os


class Config:
    SECRET_KEY = os.environ.get('8cdb24516a629ad324dc880810ea2318') or '8cdb24516a629ad324dc880810ea2318'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем уведомления об изменениях SQLAlchemy
