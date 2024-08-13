""" 
    __init__.py ：初始化文件，创建Flask应用 
"""

from flask import Flask
from .views.views import blog
from .views.views_admin import admin
from .exts import init_exts


def create_app():
    """ 创建项目 """
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(blueprint=blog)
    app.register_blueprint(blueprint=admin)

    # 配置数据库
    db_uri = 'mysql+pymysql://root:123456@localhost:3360/blogdb'  # mysql的配置
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止对象追踪修改

    # 初始化插件
    init_exts(app=app)

    return app
