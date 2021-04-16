from data.users import User
from data.cart import Cart
from data.catalog import Product
from data import db_session


def add_user():
    user = User()
    user.name = ''
    user.about = ''
    user.email = ''
    user.hashed_password = ''
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def add_product():
    product = Product()
    product.name = ''
    product.about = ''
    product.user = ''
    product.price = 12
    db_sess = db_session.create_session()
    db_sess.add(product)
    db_sess.commit()


def add_cart():
    cart = Cart()
    cart.user = ''
    cart.product = ''
    db_sess = db_session.create_session()
    db_sess.add(cart)
    db_sess.commit()
