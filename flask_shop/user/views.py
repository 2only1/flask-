from flask_shop.user import user_bp,user_api
from flask import request
from flask_restful import Resource,reqparse
#在视图函数中引入模型
from flask_shop import models,db
from flask_shop.utils.token import generate_token,verify_token,login_required
import re
#创建视图
@user_bp.route('/')
def index():
    return 'user index'

#登录功能 函数
@user_bp.route('/login/',methods=['POST'])
def login():
    #获取用户名
    name = request.get_json().get('name')
    #获取密码
    pwd = request.get_json().get('pwd')
    #验证用户名和密码的合法性
    if not all([name,pwd]):
        return {'status':400,'msg':'用户名或密码不能为空'}
    #验证用户名和密码是否正确
    else:
        # 通过用户名获取用户对象
        user = models.User.query.filter(models.User.name == name).first()
        #判断用户是否存在
        if user:
            #判断密码是否正确
            if user.pwd == pwd:
                # 生成token
                token = generate_token({'id':user.id})
                return {'status':200,'msg':'登录成功',"data":{'token':token}}
        return {'status':400,'msg':'用户名或密码错误'}
            

#注册功能类
class Users(Resource):
    '''
    继承Resource类并实现其方法,可以创建各种RESTful API资源。
    例如,可以使用GET、POST、PUT、DELETE等HTTP方法来操作资源。
    '''
    #get
    def get(self):
        #创建RequestParser对象
        parser = reqparse.RequestParser()
        #添加参数   设置默认值后不能在请求添加
        parser.add_argument('pnum',type=int,default=1,location='args')
        parser.add_argument('psize',type=int,default=20,location='args')
        parser.add_argument('name',type=str,location='args')
        #解析参数
        args = parser.parse_args()
        #获取参数
        name = args.get('name')
        pnum = args.get('pnum')
        psize = args.get('psize')
        #判断是否传递了name
        if name:
            #查询用户 like模糊查询,paginate分页
            user_list = models.User.query.filter(models.User.name.like(f'%{name}%')).paginate(page=pnum,per_page=psize)
        else:
            #查询所有用户
            user_list = models.User.query.paginate(page=pnum,per_page=psize)
        data = {
            'total':user_list.total,
            'pnum':pnum,
            'data':[u.to_dict() for u in user_list.items],
        }
        return {'status':200,'msg':'获取用户列表成功','data':data}
    #post
    def post(self):
        #注册用户
        # 接收用户名和密码
        name = request.get_json().get('name')
        pwd = request.get_json().get('pwd')
        real_pwd = request.get_json().get('real_pwd')
        #验证数据的合法性
        if not all([name,pwd,real_pwd]):
            return {'status':400,'msg':'参数不完整'}
        #判断两次密码是否一致
        if pwd != real_pwd:
            return {'status':400,'msg':'两次密码不一致'}
        #判断用户名是否合法
        if len(name) < 2 or len(name) > 12:
            return {'status':400,'msg':'用户名长度不合法'}
        #接收手机号,邮箱,昵称
        phone = request.get_json().get('phone')
        email = request.get_json().get('email')
        nick_name = request.get_json().get('nick_name')
        #接收角色ID信息
        role_id = request.get_json().get('role_id')
        #判断手机号和邮箱是否合法
        if not re.match(r'^1[3-9]\d{9}$',phone):
            return {'status':400,'msg':'手机号不合法'}
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
            return {'status':400,'msg':'邮箱不合法'}
        #try 判断用户是否存在
        try:
            #判断用户是否存在
            user = models.User.query.filter(models.User.name == name).first()
            if user:
                return {'status':400,'msg':'用户已存在'}
        except Exception as e:
            print(e)
        #创建用户对象
        if role_id:
            user =models.User(name=name,pwd=pwd,phone=phone,email=email,nick_name=nick_name,role_id=role_id)
        else:
            user =models.User(name=name,pwd=pwd,phone=phone,email=email,nick_name=nick_name)
        #保存用户对象
        db.session.add(user)
        db.session.commit()
        return {'status':200,'msg':'注册成功'}
user_api.add_resource(Users,'/users/')

#对单一数据获取
class User(Resource):
    #get请求
    def get(self,id):
    #查询用户
        user = models.User.query.get(id)
        #判断用户是否存在
        if user :
            # 成功返回
            return {'status':200,'msg':'查询成功',"data":user.to_dict()}
        #否则
        else:
            # 失败返回
            return {'status':400,'msg':'用户不存在'}
    #put请求    修改用户信息
    def put(self,id):
        try:
            user = models.User.query.get(id)
            #创建RequestParser对象
            paser = reqparse.RequestParser()
            #添加参数
            paser.add_argument('nick_name',type=str)
            paser.add_argument('phone',type=str)
            paser.add_argument('email',type=str)
            #增加角色ID
            paser.add_argument('role_id',type=int)
            #解析参数
            args = paser.parse_args()
            if args.get('nick_name'):
                user.nick_name = args.get('nick_name')
            if args.get('phone'):
                user.phone = args.get('phone')
            if args.get('email'):
                user.email = args.get('email')
            if args.get('role_id'):
                user.role_id = args.get('role_id')
            #保存用户对象
            db.session.commit()
            return {'status':200,'msg':'修改成功','data':user.to_dict()}
        except Exception as e:
            print('捕获错误----',e)
            return {'status':400,'msg':'修改失败'}
    #delete请求
    def delete(self,id):
        try:
            #删除用户
            user = models.User.query.get(id)
            #判断用户是否存在
            if user:
                #删除用户
                db.session.delete(user)
                #提交
                db.session.commit()
                return {'status':200,'msg':'删除成功'}
        except Exception as e:
            print('捕获错误----',e)
            return {'status':400,'msg':'删除失败'}
user_api.add_resource(User,'/user/<int:id>/')

# 重置密码
@user_bp.route('/reset_pwd/<int:id>/')
def reset_pwd(id):
    try:
        user = models.User.query.get(id)
        #判断用户是否存在
        if user:
            #重置密码   
            user.pwd = '123456'
            db.session.commit()            
            return {'status':200,'msg':'重置密码成功!密码为----123456'}
    except Exception as e:
        print('捕获错误----',e)
        return {'status':400,'msg':'重置密码失败'}


@user_bp.route('/test/')
@login_required
def test_login_required():
    return {'status':200,'msg':'验证成功123'}