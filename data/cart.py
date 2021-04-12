import datetime
import sqlalchemy as sql
from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase):
    __tablename__ = 'cart'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    product = sql.Column(sql.Integer, sql.ForeignKey("catalog.id"))
    user = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    created_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
