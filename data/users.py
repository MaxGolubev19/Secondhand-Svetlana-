import datetime
import sqlalchemy as sql
from werkzeug.security import generate_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    surname = sql.Column(sql.String)
    name = sql.Column(sql.String)
    email = sql.Column(sql.String, index=True, nullable=True)
    phone = sql.Column(sql.Integer, index=True, nullable=True)
    address = sql.Column(sql.String, nullable=True)
    size = sql.Column(sql.String, nullable=True)
    sex = sql.Column(sql.String, nullable=True)
    login = sql.Column(sql.String)
    password = sql.Column(sql.String)
    created_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
    status = sql.Column(sql.String, default='user')


def add_admins(n):
    from data import db_session

    for i in range(1, n + 1):
        admin = User()
        admin.surname = 'Admin'
        admin.name = f'{i}'
        admin.login = f'admin{i}'
        admin.password = generate_password_hash(f'admin{i}')
        admin.status = 'admin'
        db_sess = db_session.create_session()
        db_sess.add(admin)
        db_sess.commit()



