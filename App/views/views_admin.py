""" 后台路由 """
import time
from functools import wraps
from flask import Blueprint, render_template, request, redirect, jsonify
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
    categorys = CategoryModel.query.all()
    return render_template('admin/category.html',
                           username=user.name,
                           categorys=categorys)


# 后台管理-添加分类
@admin.route("/admin/addcategory/", methods=["GET", "POST"])
@login_required
def admin_add_category():
    """ 添加分类 """
    if request.method == 'POST':
        name = request.form.get("name")
        describe = request.form.get("describe")

        category = CategoryModel()
        category.name = name
        category.describe = describe

        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

        return redirect('/admin/category/')

    return '请求方式错误！'


# 后台管理-删除分类
@admin.route("/admin/delcategory/", methods=["GET", "POST"])
@login_required
def admin_del_category():
    """ 删除分类 """
    if request.method == 'POST':
        id = request.form.get('id')
        category = CategoryModel.query.get(id)

        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            print(e)

        return jsonify({"code": 200, "msg": '删除成功'})

    return jsonify({"code": 400, "msg": '请求方式错误'})


# 后台管理-修改分类
@admin.route("/admin/updatecategory/<id>/", methods=["GET", "POST"])
@login_required
def admin_update_category(id):
    """ 修改分类 """
    if request.method == 'GET':
        user = request.user
        category = CategoryModel.query.get(id)
        return render_template('admin/category_update.html',
                               username=user.name,
                               category=category
                               )
    elif request.method == 'POST':
        name = request.form.get("name")
        describe = request.form.get("describe")

        category = CategoryModel.query.get(id)
        category.name = name
        category.describe = describe

        try:
            db.session.commit()
        except Exception as e:
            print(e)

        return redirect('/admin/category/')
    else:
        return '请求方式错误'


# 后台管理-文章
@admin.route("/admin/article/")
@login_required
def admin_article():
    """ 文章列表 """
    articles = ArticleModel.query.all()
    return render_template('admin/article.html',
                           username=request.user.name,
                           articles=articles)


# 后台管理-添加文章
@admin.route("/admin/addarticle/", methods=["GET", "POST"])
@login_required
def admin_add_article():
    """ 添加文章 """
    if request.method == "GET":
        articles = ArticleModel.query.all()
        categorys = CategoryModel.query.all()
        return render_template('admin/article_add.html',
                               username=request.user.name,
                               categorys=categorys,
                               articles=articles)
    elif request.method == "POST":
        name = request.form.get("name")
        keywords = request.form.get("keywords")
        content = request.form.get("content")
        category = request.form.get("category")
        img = request.files.get("img")

        # 图片的存储路径
        img_name = f'{time.time()}-{img.filename}'
        img_url = f'/static/home/uploads/{img_name}'

        try:
            article = ArticleModel()
            article.name = name
            article.keywords = keywords
            article.content = content
            article.img = img_url
            article.category_id = category

            db.session.add(article)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print(e)

        return redirect('/admin/article/')


# 后台管理-修改文章
@admin.route("/admin/updatearticle/<id>/", methods=["GET", "POST"])
@login_required
def admin_update_article(id):
    """ 修改文章 """
    article = ArticleModel.query.get(id)
    categorys = CategoryModel.query.all()

    if request.method == 'GET':

        return render_template('admin/article_update.html',
                               username=request.user.name,
                               article=article,
                               categorys=categorys
                               )
    elif request.method == 'POST':
        pass


# 后台管理-删除文章
@admin.route("/admin/deletearticle/", methods=["GET", "POST"])
@login_required
def admin_del_article():
    """ 删除文章 """
    if request.method == 'POST':
        id = request.form.get("id")
        article = ArticleModel.query.get(id)
        try:
            db.session.delete(article)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({'code': 500, "msg": '删除失败！'})

        return jsonify({'code': 200, "msg": '删除成功！'})

    return jsonify({'code': 400, "msg": '请求方式错误！'})
