""" 路由 """
from flask import Blueprint
from ..models.models import *

# 蓝图
blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    """ 首页 """
    return 'index'
