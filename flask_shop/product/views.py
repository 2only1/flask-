from flask_restful import Resource, reqparse
from flask import request,current_app
from flask_shop import models,db
from flask_shop.product import product_api,product_bp
import hashlib 
from time import time
class Products(Resource):

    #获取商品
    def get(self):
        #创建参数解析器
        parser = reqparse.RequestParser()

        #添加参数   
        parser.add_argument('name', type=str, location='args')
        #解析参数
        args = parser.parse_args()

        #返回商品
        name = args['name']
        if name :
            product_list = models.Product.query.filter(models.Product.name.like(f'%{name}%')).all()
        else:
            product_list = models.Product.query.all()

        return {'status':200,
                'msg':'获取商品列表成功',
                'data':[product.to_dict() for product in product_list],
        }

    def post(self):
        '''
        添加商品
        '''
        try:
            #创建参数解析器
            parser = reqparse.RequestParser()
            #添加参数
            parser.add_argument('name', type=str, required=True, help='商品名称不能为空')
            parser.add_argument('price', type=float, help='商品价格不能为空')
            parser.add_argument('number', type=int, )
            parser.add_argument('introduce', type=str, )
            parser.add_argument('weight', type=int, )
            parser.add_argument('cid_one', type=int, )
            parser.add_argument('cid_two', type=int, )
            parser.add_argument('cid_three', type=int, )
            

            parser.add_argument('attr_static', type=list,location='json')
            parser.add_argument('attr_dynamic', type=list,location='json')
            parser.add_argument('pics', type=list, location='json')
            #解析参数
            args = parser.parse_args()
            #创建商品对象
            product = models.Product(
                name=args['name'],
                price=args['price'],
                number=args['number'],
                introduce=args['introduce'],
                weight=args['weight'],
                cid_one=args['cid_one'],
                cid_two=args['cid_two'],
                cid_three=args['cid_three'],
            )
            #保存商品
            db.session.add(product)
            db.session.commit()

            #增加商品图片
            for p in args.get('pics'):
                pic = models.Picture(path = p,pid = product.id)
                db.session.add(pic)
            #增加商品静态属性
            for a in args.get('attr_static'):
                attr = models.ProductAttr(
                    pid = product.id,
                    aid = a.get('id') ,
                    val  = a.get('val') ,
                    _type= 'static')
                db.session.add(attr)
            #增加商品动态属性
            for a in args.get('attr_dynamic'):
                attr = models.ProductAttr(
                    pid = product.id,
                    aid = a.get('id') ,
                    val  = ','.join(a.get('val')) ,
                    _type= 'dynamic')
                db.session.add(attr)
            #提交事务
            db.session.commit()
            return {'status':200,'msg':'添加商品成功'}
        except Exception as e:
            print(e)
            return {'status':500,'msg':'添加商品失败'}


product_api.add_resource(Products, '/products/')        

class Product(Resource):
    def delete(self,id):
        #删除商品
        try:
            #根据id查询商品
            product = models.Product.query.get(id)
            #删除商品
            db.session.delete(product)
            #提交事务
            db.session.commit()
            return {'status':200,'msg':'删除商品成功'}
        except Exception as e:
            return {'status':500,
                    'msg':'删除商品失败',
            }
product_api.add_resource(Product, '/product/<int:id>/')


@product_bp.route('/upload_img/', methods=['POST'])
def upload_img():
    try:
        # 获取上传的图片
        img_file = request.files.get('file')
        if img_file:
            # 判断图片类型是否能上传
            if allowed_img(img_file.filename):
                #以时间戳的方式保存图片
                file_name = md5_file() + '.' + img_file.filename.split('.')[-1]
                #保存图片
                img_file.save(current_app.config.get('UPLOAD_FOLDER') +'/'+ file_name)
                #封装返回数据
                data = {
                    'path':f'/static/upload/{file_name}',
                    'url':f'http://127.0.0.1:5000//static/upload/{file_name}',
                }
                return {'status':200,'msg':'上传图片成功','data':data}
            else:
                return {'status':400,'msg':'图片类型不合法'}
        return {'status':200,'msg':'图片不存在'}
    except Exception as e:
        return {'status':500,'msg':'上传图片失败'}
    
def allowed_img(filename):
    '''
    判断上传的图片类型是否合法
    :oaram filename: 文件名
    '''
    if '.' in filename :
        #获取文件后缀
        suffix = filename.split('.')[-1]
        #判断后缀是否合法
        if suffix in current_app.config.get('ALLOWED_EXTENSIONS'):
            return True
        else:
            return False
    return False

def md5_file():
    '''
    通过md5实现时间戳加密    
    '''
    md5 = hashlib.md5()
    md5.update(str(time()).encode('utf-8'))
    #获取加密后的字符串
    file_name = md5.hexdigest()
    return file_name
