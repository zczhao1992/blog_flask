""" 数据库文件 """
from ..exts import db


# 分类：文章 = 1 ：N


# 分类

class CategoryModel(db.Model):
    """ 分类表 """
    __tablename__ = 'tb_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    describe = db.Column(db.Text, default="describe")
    # 所有文章
    articles = db.relationship(
        "ArticleModel", backref="category", lazy='dynamic')

# 文章


class ArticleModel(db.Model):
    """ 文章表 """
    __tablename__ = 'tb_article'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    keyword = db.Column(db.String(255), default="keyword")
    content = db.Column(db.Text, default="content")
    img = db.Column(db.Text, default="img")
    # 所属分类、外键
    category_id = db.Column(db.Integer, db.ForeignKey(CategoryModel.id))


# 相册

class photoModel(db.Model):
    """相册表 """
    __tablename__ = 'tb_photo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text)
    name = db.Column(db.String(30), unique=True)
    describe = db.Column(db.Text, default="describe")
