import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "ваш-секретный-ключ"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"  # Локальная SQLite-база
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join("app", "static", "uploads")