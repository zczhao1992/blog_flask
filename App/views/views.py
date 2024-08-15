""" 路由 """
from flask import Blueprint, render_template, request
from ..models.models import *

# 蓝图
blog = Blueprint('blog', __name__)


# 博客首页
@blog.route('/')
@blog.route('/index/')
def blog_index():
    """ 首页 """
    photos = photoModel.query.limit(6)
    categorys = CategoryModel.query.all()
    articles = ArticleModel.query.all()
    commends = articles[:4]
    return render_template('home/index.html',
                           photos=photos,
                           categorys=categorys,
                           articles=articles,
                           commends=commends
                           )


# 博客相册
@blog.route('/photos/')
def blog_photos():
    """ 相册 """
    photos = photoModel.query.all()
    return render_template('home/photos.html', photos=photos)


# 博客日记
@blog.route('/article/')
def blog_article():
    """ 日记 """
    categorys = CategoryModel.query.all()
    articles = ArticleModel.query.all()
    return render_template('home/article.html',
                           categorys=categorys,
                           articles=articles)


# 关于我
@blog.route('/about/')
def blog_about():
    """ 关于我 """
    photos = photoModel.query.limit(6)
    categorys = CategoryModel.query.all()
    return render_template('home/about.html',
                           photos=photos,
                           categorys=categorys
                           )
