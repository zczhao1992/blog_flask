""" 后台路由 """
from flask import Blueprint, render_template, request
from ..models.models_admin import *

# 蓝图
admin = Blueprint('admin', __name__)


# 后台管理-首页
@admin.route('/admin/')
def index():
    """ 首页 """
    return render_template("admin/index.html")


# 后台管理-登录
@admin.route('/admin/login/', methods=["GET", "POST"])
def admin_login():
    """ 登录 """
    if request.method == 'GET':
        return render_template("admin/login.html")
    elif request.method == 'POST':
        pass
