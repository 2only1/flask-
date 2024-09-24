import os
class Config:
    #设置参数
    MYSQL_DIALECT = 'mysql'
    MYSQL_DRIVER = 'pymysql'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DB = 'flask_shop'
    MYSQL_CHARSET = 'utf8mb4'

    #数据库连接字符串URL
    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset={MYSQL_CHARSET}'
    #设置数据盐
    SECRET_KEY = os.urandom(16)
    # 设置JSON数据不使用ASCII编码
    JSON_AS_ASCII = False#老版本不生效了
    RESTFUL_JSON = {'ensure_ascii': False}
    #设置token过期时间,秒为单位
    TOKEN_EXPIRE_TIME = 60*60*24
    #设置可以上传的文件类型
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    #获取当前文件根路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #设置上传文件路径
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'flask_shop','static/upload')
    
class DevelopmentConfig(Config):
    # 开发环境
    # DEBUG模式
    DEBUG = True

class ProductionConfig(Config):
    # 生产环境
    DEBUG = False

class TestingConfig(Config):
    # 测试环境
    pass

config_map = {
    #开发环境
    'develop': DevelopmentConfig,
    #生产环境
    'product': ProductionConfig,
    #测试环境
    'test': TestingConfig
}