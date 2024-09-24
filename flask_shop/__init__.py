from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

from config import config_map

#创建数据库对象
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    # 根据config_name获取配置类
    Config = config_map.get(config_name)
    #根据类来加载配置信息
    app.config.from_object(Config)
    #初始化db,将db与app关联
    db.init_app(app)
    #返回Flask实例,以便其他接收

    #获取user蓝图,引包问题,建议放这里
    from flask_shop.user import user_bp
    app.register_blueprint(user_bp)

    #获取menu蓝图对象
    from flask_shop.menu import menu_bp
    #注册蓝图
    app.register_blueprint(menu_bp)

    #r获取oles蓝图
    from flask_shop.role import role_bp
    app.register_blueprint(role_bp)

    #获取category蓝图
    from flask_shop.category import cate_bp
    app.register_blueprint(cate_bp)

    #获取Attribute蓝图对象
    from flask_shop.category import attr_bp
    app.register_blueprint(attr_bp)

    #获取product蓝图对象
    from flask_shop.product import product_bp
    app.register_blueprint(product_bp)


    #获取order蓝图对象  
    from flask_shop.order import order_bp
    app.register_blueprint(order_bp)

    return app

