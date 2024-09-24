from flask import Blueprint
from flask_restful import Api

user_bp = Blueprint('user', __name__, url_prefix='/user')
#创建Api对象,放入蓝图通过蓝图管理
user_api = Api(user_bp)
# 导入视图,这里需要引用视图对象，而不是导入模块
from . import views