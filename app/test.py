from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'
categories = ['Ноты', 'Гитара', 'Фортепиано', 'Ударные', 'Вокал']


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Шаг 1: Сохраняем данные в сессию
        if 'step' not in session or session['step'] == 1:
            session['email'] = request.form['email']
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['step'] = 2
            return render_template('register.html', step=2, categories=categories)

        # Шаг 2: Обработка выбранных категорий
        elif session['step'] == 2:
            selected_categories = request.form.getlist('categories')
            # Здесь сохраняем данные в БД
            session.clear()
            return render_template('base.html')

    # Первый вход
    session['step'] = 1
    return render_template('register.html', step=1)


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')