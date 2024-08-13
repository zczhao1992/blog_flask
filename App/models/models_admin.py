""" 数据库文件 """
from ..exts import db


class AdminUserModel(db.Model):
    """ 用户表 """
    __tablename__ = 'tb_adminuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    passwd = db.Column(db.String(30))
