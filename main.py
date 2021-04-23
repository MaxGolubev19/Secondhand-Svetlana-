import os
from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from added import add_user, add_product, add_cart
from data.users import User
from data.catalog import Product
from data.cart import Cart
from flask_login import LoginManager, login_user, current_user, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

sex = {'man': 'Мужское',
       'woman': 'Женское',
       'child': 'Детское',
       'Мужское': 'man',
       'Женское': 'woman',
       'Детское': 'child',
    }

categories = {'Одежда': 'wear',
            'Обувь': 'shoes',
            'Аксессуары': 'accessories',
            'Косметика': 'cosmetics',
            'Игрушки': 'toys',
            'Другое': 'other',
    }

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


@app.route('/catalog', methods=['post', 'get'])
def catalog():
    params = {}
    params['title'] = 'Товары'
    db_sess = db_session.create_session()
    products = db_sess.query(Product)
    if request.method == 'POST':
        my_sex = sex.get(request.form.get('sex'), None)
        my_category = categories.get(request.form.get('category'), None)
        if my_sex:
            products = products.filter(Product.sex == my_sex)
            params[f'{my_sex}'] = 'selected="selected"'
        if my_category:
            params['my_category'] = my_category
            products = products.filter(Product.category == my_category)
            params[f'{my_category}'] = 'selected="selected"'
    params['products'] = products
    return render_template('catalog.html', **params)


@app.route('/catalog/<category>')
def category(category):
    params = {}
    params['title'] = sex[category]
    db_sess = db_session.create_session()
    params['products'] = db_sess.query(Product).filter(Product.sex == category)
    return render_template(f'catalog.html', **params)


@app.route('/catalog/product/<int:id>')
def product(id):
    params = {}
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id).first()
    params['title'] = product.name
    params['product'] = product
    return render_template(f'product.html', **params)


@app.route('/add_cart/<int:product_id>')
def add_cart(product_id):
    cart = Cart()
    cart.product_id = product_id
    cart.user_id = current_user.id
    db_sess = db_session.create_session()
    db_sess.add(cart)
    db_sess.commit()
    return redirect("/cart")


@app.route('/buy/<int:product_id>')
def buy(product_id):
    pass


@app.route('/delete_cart/<int:id>')
def delete_cart(id):
    db_sess = db_session.create_session()
    cart = db_sess.query(Cart).filter(Cart.id == id).first()
    db_sess.delete(cart)
    db_sess.commit()
    return redirect('/cart')


@app.route('/delete/<int:id>')
def delete(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id).first()
    if current_user.id == product.user_id or current_user.status == 'admin':
        db_sess.delete(product)
        db_sess.commit()
    return redirect('/catalog')


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
        if category == 'cosmetics':  product.sex = 'woman'
        elif category == 'toys': product.sex = 'child'
        else: product.sex = sex[request.form.get('sex')]
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
        else:
            params['type_modal'] = 'error'
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


@app.route('/cart')
def cart():
    params = {}
    params['title'] = 'Корзина'
    db_sess = db_session.create_session()
    params['cart'] = db_sess.query(Cart).filter(Cart.user_id == current_user.id)
    return render_template('cart.html', **params)


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


























