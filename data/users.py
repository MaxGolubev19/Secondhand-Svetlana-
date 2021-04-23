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
    sex = sql.Column(sql.String, nullable=True)
    status = sql.Column(sql.String, default='user')
    address = sql.Column(sql.String, nullable=True)
    email = sql.Column(sql.String, index=True, nullable=True)
    phone = sql.Column(sql.Integer, index=True, nullable=True)
    size = sql.Column(sql.String, nullable=True)
    login = sql.Column(sql.String)
    password = sql.Column(sql.String)
    image = sql.Column(sql.String, nullable=True)
    created_date = sql.Column(sql.DateTime, default=datetime.datetime.now)


