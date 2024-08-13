""" 后台路由 """
from flask import Blueprint
from ..models.models_admin import *

# 蓝图
admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    """ 首页 """
    return 'index'
