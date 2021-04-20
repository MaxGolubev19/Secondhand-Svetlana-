import datetime
import sqlalchemy as sql
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    surname = sql.Column(sql.String, nullable=True)
    name = sql.Column(sql.String, nullable=True)
    email = sql.Column(sql.String, index=True, nullable=True)
    phone = sql.Column(sql.Integer, index=True, nullable=True)
    address = sql.Column(sql.String, nullable=True)
    size = sql.Column(sql.String, nullable=True)
    sex = sql.Column(sql.String, nullable=True)
    hashed_password = sql.Column(sql.String, nullable=True)
    created_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
