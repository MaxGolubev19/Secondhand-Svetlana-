import datetime
import sqlalchemy as sql
from .db_session import SqlAlchemyBase


class Catalog(SqlAlchemyBase):
    __tablename__ = 'catalog'

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name = sql.Column(sql.String, nullable=True)
    about = sql.Column(sql.String, nullable=True)
    price = sql.Column(sql.Float, nullable=True)
    user = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    created_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
