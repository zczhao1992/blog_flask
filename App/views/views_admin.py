""" 后台路由 """
from functools import wraps
from flask import Blueprint, render_template, request, redirect
from ..models.models_admin import *
from ..models.models import *

# 蓝图
admin = Blueprint('admin', __name__)


# 装饰器: 登录验证


def login_required(fn):
    """  登录验证 """
    @wraps(fn)
    def inner(*args, **kwargs):
        """ 获取cookie,得到登录的用户 """
        user_id = request.cookies.get("user_id", None)
        if user_id:
            user = AdminUserModel.query.get(user_id)
            request.user = user
            return fn(*args, **kwargs)
        else:
            # 如果没有登录，则跳转到登录页面
            return redirect("/admin/login/")

    return inner


# 后台管理-首页
@admin.route('/admin/')
@admin.route('/admin/index/')
@login_required
def index():
    """ 首页 """

    # # 获取cookie,得到登录的用户
    # user_id = request.cookies.get("user_id", None)

    # if user_id:
    #     # 登陆过，进入后台管理系统
    #     user = AdminUserModel.query.get(user_id)

    #     categorys = CategoryModel.query.filter()
    #     articles = ArticleModel.query.filter()
    #     photos = photoModel.query.filter()

    #     return render_template("admin/index.html",
    #                            username=user.name,
    #                            categorys=categorys,
    #                            articles=articles,
    #                            photos=photos
    #                            )
    # else:
    #     # 如果没有登录，则跳转到登录页面
    #     return redirect("/admin/login/")

    user = request.user
    categorys = CategoryModel.query.filter()
    articles = ArticleModel.query.filter()
    photos = photoModel.query.filter()

    return render_template("admin/index.html",
                           username=user.name,
                           categorys=categorys,
                           articles=articles,
                           photos=photos
                           )


# 后台管理-登录
@admin.route('/admin/login/', methods=["GET", "POST"])
def admin_login():
    """ 登录 """
    if request.method == 'GET':
        return render_template("admin/login.html")
    elif request.method == 'POST':
        username = request.form.get("username")
        userpwd = request.form.get("userpwd")

        # 登录验证
        user = AdminUserModel.query.filter_by(
            name=username, passwd=userpwd).first()

        if user:
            response = redirect("/admin/index/")
            response.set_cookie('user_id', str(user.id), max_age=7*24*3600)
            return response
        else:
            return 'Login Failed'


# 后台管理-退出登录
@admin.route('/admin/logout/')
def admin_logout():
    """ 退出登录 """
    response = redirect("/admin/login/")
    response.delete_cookie("user_id")
    return response


# 后台管理-分类管理
@admin.route("/admin/category/")
@login_required
def admin_category():
    """ 分类管理 """
    # # 获取cookie,得到登录的用户
    # user_id = request.cookies.get("user_id", None)

    # if user_id:
    #     return render_template('admin/category.html')
    # else:
    #     # 如果没有登录，则跳转到登录页面
    #     return redirect("/admin/login/")
    user = request.user
    return render_template('admin/category.html', username=user.name)
