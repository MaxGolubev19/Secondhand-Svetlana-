import datetime
import sqlalchemy as sql
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'catalog'
    
    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name = sql.Column(sql.String)
    about = sql.Column(sql.String, nullable=True)
    size = sql.Column(sql.String, nullable=True)
    price = sql.Column(sql.Integer)
    sex = sql.Column(sql.String, default='all')
    category = sql.Column(sql.String)
    user_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    user = sql.orm.relation('User')
    image = sql.Column(sql.String, default='/static/images/pictures/no_image.jpg')
    created_date = sql.Column(sql.DateTime, default=datetime.datetime.now)
