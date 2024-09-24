from flask_shop import create_app,db
from flask_migrate import Migrate
from flask_cors import CORS

#创建app实例
app = create_app('develop')
CORS(app,supports_credentials=True) #解决跨域问题,只需一行

#创建同步数据库对象,对应实例和数据库
Migrate(app, db)

# 设置JSON数据不使用ASCII编码
app.json.ensure_ascii = False

'''
终端输入
flask db init    初始化迁移环境 仅仅一次
flask db migrate    生成迁移文件
flask db upgrade    同步到数据库
$env:FLASK_APP="manager"    加载环境变量
'''
if __name__ == '__main__':
    app.run()