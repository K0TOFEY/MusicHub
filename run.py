from app import create_app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        from app.models import User
        from app import db
        db.create_all()  # Создание таблиц в базе
    app.run(host="0.0.0.0", port=5000, debug=True)