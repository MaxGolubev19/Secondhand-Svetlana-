import os
from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from added import add_user, add_product, add_cart
from data.users import User
from data.catalog import Product
from flask_login import LoginManager, login_user, current_user, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


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
    db_sess = db_session.create_session()
    params['products'] = db_sess.query(Product)
    return render_template('catalog.html', **params)


@app.route('/catalog/<category>')
def category(category):
    params = {}
    params['title'] = category
    db_sess = db_session.create_session()
    params['products'] = db_sess.query(Product).filter(Product.category == category)
    return render_template(f'catalog.html', **params)


@app.route('/<product>')
def product(product):
    params = {}
    params['title'] = product
    return render_template(f'{product}.html', **params)


@app.route('/create')
def choice():
    params = {}
    params['title'] = 'Добавление товара'
    return render_template('choice.html', **params)


@app.route('/create/<category>', methods=['post', 'get'])
def create(category):
    params = {}
    params['title'] = 'Добавление товара'
    if request.method == 'POST':
        product = Product()
        product.name = request.form.get('product_name')
        product.about = request.form.get('description')
        product.size = request.form.get('size')
        product.price = request.form.get('price')
        product.category = category
        product.user_id = current_user.id
        db_sess = db_session.create_session()
        db_sess.add(product)
        db_sess.commit()
        return redirect("/")
    return render_template(f'{category}.html', **params)


@app.route('/logup', methods=['post', 'get'])
def logup():    
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
        user.password = generate_password_hash(request.form.get('password'))
        user.size = request.form.get('size')
        user.sex = request.form.get('sex')
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect("/")
    return render_template('logup.html', **params)


@app.route('/login', methods=['post', 'get'])
def login():
    from data.users import User
    global user
    params = {}
    params['title'] = 'Вход'
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == request.form.get('login')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect("/")
    return render_template('login.html', **params)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/account')
def account():
    params = {}
    params['title'] = 'Аккаунт'
    return render_template('account.html', **params)

@app.route('/exit')
def exit():
    logout_user()
    return redirect('/login')


if __name__ == '__main__':
    db_session.global_init("db/shop.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
"""
if __name__ == '__main__':
    db_session.global_init("db/shop.db")
    app.run()
"""


























