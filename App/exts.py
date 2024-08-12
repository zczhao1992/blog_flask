""" 
    数据库
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_exts(app):
    """ 初始化数据库 """
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
