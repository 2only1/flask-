from flask_shop import db
#generate_password_hash哈希加密,check_password_hash检查加密正确性
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class BaseModel(object):
    create_time = db.Column(db.DateTime,default=datetime.now)
    #onupdate参数用于指定在更新记录时自动更新字段的值。加()就不自动更新了
    update_time = db.Column(db.DateTime,default=datetime.now, onupdate=datetime.now)

class User(db.Model,BaseModel):
    __tablename__ = 't_users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(32), nullable=False,unique=True)
    pwd = db.Column(db.String(128))
    nick_name = db.Column(db.String(32))   #昵称
    phone = db.Column(db.String(11))
    email = db.Column(db.String(32))
    #建立用户与角色的关系,多对一关系
    role_id = db.Column(db.Integer, db.ForeignKey('t_roles.id'))
    role = db.relationship('Role', backref='users')
    
    #你可以像访问普通属性一样访问它，而不需要使用()
    @property
    def password(self):
        return self.pwd

    #setter方法中，我们可以对输入值进行验证，确保它满足我们的要求。
    #如果输入值不满足要求，我们可以抛出一个异常，或者返回一个默认值。
    #可以将加密后的密码存储在一个单独的属性中，而不是直接将加密后的密码赋值给password属性
    @password.setter
    def password(self, pwd):
        self.pwd = generate_password_hash(pwd) #加密后的密码

    #用户登录,检查密码是否正确,返回True或False
    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)
    
    #设置返回值
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'nick_name':self.nick_name,
            'phone':self.phone,
            'email':self.email,
            'role_name' : self.role.name if self.role else None,
            'role_id': self.role_id if self.role else None,
        }

#权限与角色的多对多关系(Menu/Role),第三方表
trm = db.Table('t_roles_menus',
               db.Column("roles_id",db.Integer, db.ForeignKey('t_roles.id')),
               db.Column("menus_id",db.Integer, db.ForeignKey('t_menu.id')),
               )

class Menu(db.Model):
    __tablename__ = 't_menu'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),unique=True, nullable=False)
    #default 默认等级
    level = db.Column(db.Integer, default=1)
    #跳转路由
    path = db.Column(db.String(32))

    pid = db.Column(db.Integer, db.ForeignKey('t_menu.id'))
    children = db.relationship('Menu')
    #角色与菜单多对多关系
    roles = db.relationship('Role', secondary=trm,backref='menus')

    def to_dict_tree(self):
        return {
            'id': self.id,  
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'pid': self.pid,
            #父级菜单有很多子菜单,所以需要遍历,并返回字典形式,是tree结构
            'children': [child.to_dict_tree() for child in self.children]
        }
    
    #列表函数
    def to_dict_list(self):
        #列表形式返回
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'path': self.path,
            'pid': self.pid,
        }
    
#创建角色模型
class Role(db.Model):
    __tablename__ = 't_roles'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),unique=True, nullable=False)
    desc = db.Column(db.String(128))

    #角色与菜单多对多关系
    # menus = db.relationship('Menu', secondary=trm)

    #返回字典形式
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'desc':self.desc,
            # 'menus':[menu.to_dict_list() for menu in self.menus],#列表返回
            # 'menus':[menu.to_dict_tree() for menu in self.menus if menu.level == 1],#树形结构返回  目前不友好结构,会找到不存在的数据
            'menus':self.get_menu_dict(),#树形结构返回
        }

    def get_menu_dict(self):
        # 创建一列表存储所有的菜单
        menu_list = []
        menus  = sorted(self.menus,key=lambda temp:temp.id)
        # menus = self.menus
        # 遍历所有一级菜单
        for m in menus:
            if m.level == 1:
                first_dict = m.to_dict_list()
                #查询所有二级菜单
                first_dict['children'] = []
                # 遍历所有二级菜单
                for m2 in self.menus:
                    #判断二级菜单,且菜单的pid是否等于一级的id
                    if m2.level == 2 and m2.pid == m.id:
                        first_dict['children'].append(m2.to_dict_list())
                # 将一级菜单添加到列表中
                menu_list.append(first_dict)
        return menu_list
    
#创建商品分类模型
class Category(db.Model):
    __tablename__ = 't_category'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),nullable=False)
    level = db.Column(db.Integer,default=1)
    pid = db.Column(db.Integer, db.ForeignKey('t_category.id'))

    children = db.relationship('Category')
    #反向查找商品属性
    attrs = db.relationship('Attributes', backref='category')
    def to_dict_tree(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'pid': self.pid,
    }

#商品属性名称
class Attributes(db.Model):
    __tablename__ = 't_attribute'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),nullable=False)
    val = db.Column(db.String(255))
    #判断商品是否是静态资源还是动态资源
    _type = db.Column(db.Enum('static','dynamic'))

    cid = db.Column(db.Integer, db.ForeignKey('t_category.id'))

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'val':self.val,
            'type':self._type,
            'cid':self.cid,
        }

class Product(db.Model):
    __tablename__ = 't_product'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(512),nullable=False)
    price = db.Column(db.Float,default=0)
    number = db.Column(db.Integer,default=0)
    introduce = db.Column(db.Text) #商品详情
    big_img = db.Column(db.String(255)) #商品大图,图片地址
    small_img = db.Column(db.String(255)) #商品小图
    state = db.Column(db.Integer) #0未通过 1审核中 2已通过
    #商品与分类多对一关系
    is_promote = db.Column(db.Integer) #是否促销
    hot_number = db.Column(db.Integer) #热度
    weight = db.Column(db.Integer) #权重

    cid_one = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    cid_two = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    cid_three = db.Column(db.Integer, db.ForeignKey('t_category.id'))
    #商品与属性多对多关系
    category = db.relationship('Category',foreign_keys=[cid_three])

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'price':self.price,
            'number':self.number,
            'introduce':self.introduce,
            'big_img':self.big_img,
            'small_img':self.small_img,
            'state':self.state,
            'is_promote':self.is_promote, #是否促销
            'hot_number':self.hot_number, #热度
            'weight':self.weight, #权重
            'cid_one':self.cid_one,
            'cid_two':self.cid_two,
            'cid_three':self.cid_three,
            'category':[a.to_dict() for a in self.category.attrs],
        }

class Picture(db.Model):
    __tablename__ = 't_picture'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    path = db.Column(db.String(255))
    pid = db.Column(db.Integer, db.ForeignKey('t_product.id'))

class ProductAttr(db.Model):
    __tablename__ = 't_product_attr'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True) 
    pid = db.Column(db.Integer, db.ForeignKey('t_product.id'))
    aid = db.Column(db.Integer, db.ForeignKey('t_attribute.id'))
    val = db.Column(db.String(255))
    #关联表存在当前值,但是还需要在这把写,业务问题及可以更快获取属性值
    _type = db.Column(db.Enum('static','dynamic'))


class Order(db.Model,BaseModel):
    __tablename__ = 't_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, default=0)
    number = db.Column(db.Integer, default=0)
    pay_status = db.Column(db.Integer, default=0)  # 0 未支付 1 已支付
    is_send = db.Column(db.Integer, default=0)  # 0 未发货 1 已发货
    fapiao_title = db.Column(db.String(255))    #发票抬头
    fapiao_content = db.Column(db.String(255))  #发票内容
    address = db.Column(db.String(255)) #收货地址
    uid = db.Column(db.Integer, db.ForeignKey('t_users.id'))    #用户id
    
    user = db.relationship('User', foreign_keys=[uid])  #订单与用户一对一关系
    order_detail = db.relationship('OrderDetail', backref='order')  #订单详情
    express = db.relationship('Express', backref='order')    #物流信息

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'number': self.number,
            'pay_status': self.pay_status,
            'is_send': self.is_send,
            'fapiao_title': self.fapiao_title,
            'fapiao_content': self.fapiao_content,
            'address': self.address,
            'uid': self.uid,
            'user': self.user.nick_name,
        }

class OrderDetail(db.Model):
    '''订单详情表'''
    __tablename__ = 't_order_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oid = db.Column(db.Integer, db.ForeignKey('t_order.id'))
    pid = db.Column(db.Integer, db.ForeignKey('t_product.id'))  
    number = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    total_price = db.Column(db.Float, default=0)    #商品总价
    
    def to_dict(self):
        return {
            'id': self.id,
            'oid': self.oid,
            'pid': self.pid,
            'number': self.number,
            'price': self.price,
            'total_price': self.total_price,
        }
    
class Express(db.Model):
    '''快递表'''
    __tablename__ = 't_express'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oid = db.Column(db.Integer, db.ForeignKey('t_order.id'))
    content = db.Column(db.String(256)) # 快递内容
    update_time = db.Column(db.String(256)) # 物流更新时间

    def to_dict(self):
        return {
            'id': self.id,
            'oid': self.oid,
            'content': self.content,
            'update_time': self.update_time,
        }
