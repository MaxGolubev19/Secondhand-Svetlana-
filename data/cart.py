import datetime
import sqlalchemy as sql
from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase):
    __tablename__ = 'cart'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    product_id = sql.Column(sql.Integer, sql.ForeignKey("catalog.id"))
    product = sql.orm.relation('Product')
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    user = sql.orm.relation('User')
    created_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
