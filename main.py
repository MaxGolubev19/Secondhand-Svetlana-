import os
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from added import add_user, add_product, add_cart


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    params = {}
    params['title'] = 'Главная'
    return render_template('index.html', **params)


@app.route('/about')
def about():
    params = {}
    params['title'] = 'О нас'
    return render_template('about.html', **params)


@app.route('/catalog')
def catalog():
    params = {}
    params['title'] = 'Товары'
    return render_template('catalog.html', **params)


@app.route('/catalog/<product>')
def product(product):
    params = {}
    params['title'] = product
    return render_template('product.html', **params)


@app.route('/catalog/<category>')
def category(category):
    params = {}
    params['title'] = category
    return render_template(f'{category}.html', **params)


@app.route('/create')
def choice():
    params = {}
    params['title'] = 'Добавление товара'
    return render_template('choice.html', **params)


@app.route('/create/<category>')
def create(category):
    params = {}
    params['title'] = 'Добавление товара'
    return render_template(f'{category}.html', **params)


@app.route('/login', methods=['post', 'get'])
def login():
    from data.users import User
    
    params = {}
    params['title'] = 'Регистрация'
    if request.method == 'POST':
        user = User()
        user.surname = request.form.get('surname')
        user.name = request.form.get('name')
        user.phone = request.form.get('phone_number')
        user.email = request.form.get('email')
        user.address = request.form.get('address')
        user.login = request.form.get('login')
        user.hashed_password = generate_password_hash(request.form.get('password'))
        user.size = request.form.get('size')
        user.sex = request.form.get('sex')
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
    return render_template('login.html', **params)


@app.route('/logup', methods=['post', 'get'])
def logup():
    from data.users import User
    
    params = {}
    params['title'] = 'Вход'
    return render_template('logup.html', **params)


@app.route('/account')
def account():
    params = {}
    params['title'] = 'Аккаунт'
    return render_template('account.html', **params)


if __name__ == '__main__':
    db_session.global_init("db/shop.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
"""
if __name__ == '__main__':
    db_session.global_init("db/shop.db")
    app.run()
"""


























