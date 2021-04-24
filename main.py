import os
from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from added import add_user, add_product, add_cart
from data.users import User
from data.catalog import Product
from data.cart import Cart
from flask_login import LoginManager, login_user, current_user, logout_user
from random import randint
from translate import sex, categories, sizes
import smtplib


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
smtpObj.starttls()
smtpObj.login('svetlana_shop.info@mail.ru', 'juoRTt%o1IO1')


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
        my_size = request.form.get('size')
        if my_sex:
            products = products.filter(Product.sex == my_sex)
            params[f'{my_sex}'] = 'selected="selected"'
        if my_category:
            params['my_category'] = my_category
            products = products.filter(Product.category == my_category)
            params[f'{my_category}'] = 'selected="selected"'
        if my_size:
            products = products.filter(Product.size == my_size)
            params[f'{sizes.get(my_size, None)}'] = 'selected="selected"'
    params['products'] = products
    return render_template('catalog.html', **params)


@app.route('/catalog/<category>', methods=['post', 'get'])
def category(category):
    params = {}
    params['title'] = sex[category]
    db_sess = db_session.create_session()
    products = db_sess.query(Product)
    if request.method == 'POST':
        my_sex = sex.get(request.form.get('sex'), None)
        my_category = categories.get(request.form.get('category'), None)
        my_size = request.form.get('size')
        if my_sex:
            products = products.filter(Product.sex == my_sex)
            params[f'{my_sex}'] = 'selected="selected"'
        if my_category:
            params['my_category'] = my_category
            products = products.filter(Product.category == my_category)
            params[f'{my_category}'] = 'selected="selected"'
        if my_size:
            products = products.filter(Product.size == my_size)
            params[f'{sizes.get(my_size, None)}'] = 'selected="selected"'
    else:
        products = products.filter(Product.sex == category)
        params[f'{category}'] = 'selected="selected"'
    params['products'] = products
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
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == product_id).first()
    user = product.user
    smtpObj.sendmail('svetlana_shop.info@mail.ru', user.email, f"""Hello, your item #{product.id} has been purchased.""")
    return redirect(f'/delete/{product_id}')


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
        image = request.files['file']
        unic_name = f'{product.user_id}{product.name}{randint(1, 999999999)}'
        with open(f'static/images/pictures/{unic_name}.jpg', 'wb') as file:
            file.write(image.read())
        if image:
            product.image = f'/static/images/pictures/{unic_name}.jpg'
        db_sess = db_session.create_session()
        db_sess.add(product)
        db_sess.commit()
        return redirect("/")
    return render_template(f'{category}.html', **params)


@app.route('/logup', methods=['post', 'get'])
def logup():    
    params = {}
    params['title'] = 'Регистрация'
    params['boxes'] = ['* - обязательные поля',
                       'Введите фамилию*',
                       'Введите имя*',
                       'Введите адрес почты*',
                       'Введите свой номер телефона',
                       'Введите свой адрес',
                       'Придумайте логин*',
                       'Придумайте пароль*',
                       'Повторите пароль*',
                       'Укажите пол',
                       'Приложите фотографию',
                       'Зарегистрироваться']
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = User()
        user.surname = request.form.get('surname')
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone_number')
        user.address = request.form.get('address')
        user.login = request.form.get('login')
        password = generate_password_hash(request.form.get('password'))
        if check_password_hash(password, request.form.get('password2')):
            user.password = password
        user.size = request.form.get('size')
        user.sex = request.form.get('sex')
        image = request.files['file']
        with open(f'static/images/pictures/{user.login}.jpg', 'wb') as file:
            file.write(image.read())
        if image:
            user.image = f'/static/images/pictures/{user.login}.jpg'
        check_user = db_sess.query(User).filter(User.login == user.login).first()
        if check_user:
            return render_template('logup.html', **params)
        if user.surname and user.name and user.email and user.login and user.password:
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


@app.route('/edit_user', methods=['post', 'get'])
def edit_user():  
    params = {}
    params['title'] = 'Редактирование'
    params['boxes'] = ['Впишите новые данные в поля, которые хотите изменить',
                       'Введите фамилию',
                       'Введите имя',
                       'Введите адрес почты',
                       'Введите свой номер телефона',
                       'Введите свой адрес',
                       'Придумайте логин',
                       'Придумайте пароль',
                       'Повторите пароль',
                       'Укажите пол',
                       'Приложите фотографию',
                       'Изменить']
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == current_user.login).first()
        surname = request.form.get('surname')
        if surname:
            user.surname = surname
        name = request.form.get('name')
        if name:
            user.name = name
        email = request.form.get('email')
        if email:
            user.email = email
        phone = request.form.get('phone_number')
        if phone:
            user.phone = phone
        address = request.form.get('address')
        if address:
            user.address = address
        login = request.form.get('login')
        if login:
            check_user = db_sess.query(User).filter(User.login == user.login).first()
            if check_user:
                return render_template('logup.html', **params)
            user.login = login
        password = generate_password_hash(request.form.get('password'))
        if password and check_password_hash(password, request.form.get('password2')):
            user.password = password
        elif password:
            return render_template('logup.html', **params)
        sex = request.form.get('sex')
        if sex:
            user.sex = sex
        image = request.files['file']
        with open(f'static/images/pictures/{user.login}.jpg', 'wb') as file:
            file.write(image.read())
        if image:
            user.image = f'/static/images/pictures/{user.login}.jpg'
        db_sess.commit()
        return redirect("/account")
    return render_template('logup.html', **params)


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


















