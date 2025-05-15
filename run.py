# print('Здесь будет запуск приложения')
from app import app, db
from app.models import User, Tag


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Tag': Tag}


if __name__ == '__main__':
    with app.app_context():
        if Tag.query.count() == 0:
            tags = ['Рок', 'Электроника', 'Классика', 'Поп',
                    'Гитара', 'Пианино', 'Барабаны', 'Саксофон']
            for tag_name in tags:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            db.session.commit()
            print("Default tags created.")

    app.run(debug=True)