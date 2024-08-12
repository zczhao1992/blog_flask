""" 数据库文件 """
from .exts import db


class User(db.Model):
    """ 用户表 """
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, index=True)
    age = db.Column(db.Integer, default=1)
