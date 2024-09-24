'''
生成浏览器token,用于用户登录
'''
import time
import jwt
from flask import current_app #获取用户对象参数
from flask import request
from functools import wraps

def generate_token(data):
    #创建token
    #设置数据过期时间
    '''
     data: 要加密的数据,数据类型是字典
     '''
    data.update({'exp':time.time()+current_app.config['TOKEN_EXPIRE_TIME']})
                        #数据,密钥,加密算法
    token = jwt.encode(data,current_app.config['SECRET_KEY'],algorithm='HS256')
    return token
def verify_token(token):
    #验证token
    try:
        data = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms='HS256')
    except Exception as e:
        return None
    return data

#验证用户登录验证器
def login_required(view_func):
    #用于保留原始函数或方法的元数据
    @wraps(view_func)
    def verify_token_info(*args,**kwargs):
        #获取用户传递来的token
        token = request.headers.get('token')
        #解析 token
        if verify_token(token):
            return view_func(*args,**kwargs)
        else:
            return {'status': 401, 'msg':'token 无效'}
    return verify_token_info