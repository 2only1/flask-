from flask_restful import Resource,reqparse
from flask_shop import models
from flask_shop import db
from flask_shop.category import cate_api,attr_api,cate_bp
from flask import request
from sqlalchemy import func,text

class Category(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        #获取一级目录
        parser.add_argument('level',type=int,default=1,location='args')
        args = parser.parse_args()
        level = args.get('level')
        # level = int(request.args.get('level'))
        psize = request.args.get('psize')   #每页显示几条数据
        pnum = request.args.get('pnum')     #当前页码
        base_query = models.Category.query.filter(models.Category.level == 1)
        #判断分页
        if all([pnum,psize]):
            #分页查询
            cates = base_query.paginate(page=int(pnum),per_page=int(psize))
        else:
            cates = base_query.all()
        #定义一个列表用于存储分类信息
        cate_list = self.to_tree(cates,level)
        #这种方式不友好
        # for c in cates:
        #     #遍历一级分类
        #     first_dict = c.to_dict_tree()
        #     first_dict['second_children'] = []
        #     #遍历二级目录
        #     for sc in c.children:
        #         second_dict = sc.to_dict_tree()
        #         second_dict['third_children'] = []
        #         #遍历三级目录
        #         for tc in sc.children:
        #             third_dict = tc.to_dict_tree()
        #             second_dict['third_children'].append(third_dict)
        #         first_dict['second_children'].append(second_dict)
        #     cate_list.append(first_dict)
        return {'status':200,'message': '商品分类获取成功','data':cate_list}
    
    def to_tree(self,info:list,level):
        #定义空列表,存储所有分类信息
        info_list = []
        #遍历所有分类信息
        for i in info:
            i_dict = i.to_dict_tree()
            #判断当前分类是否有子分类
            if i.level < level:
                #递归调用tp_tree函数
                i_dict['children'] = self.to_tree(i.children,level)
            info_list.append(i_dict)
        return info_list
    
    def post(self):
        try:
            # 创建一个ReuqestParser对象
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True,)
            parser.add_argument('level', type=int, required=True,)
            parser.add_argument('pid', type=int, )
            args = parser.parse_args()
            #判断pid是否传递
            if args.get('pid'):
                category = models.Category(name=args.get('name'), level=args.get('level'), pid=args.get('pid'))
            else:
                category = models.Category(name=args.get('name'), level=args.get('level'))
            db.session.add(category)
            db.session.commit()
            return {'status':200,'message': '商品分类添加成功'}
        except Exception as e:
            return {'status':500,'message': str(e)}

cate_api.add_resource(Category,'/categorys/')

class Attributes(Resource):
    def get(self):
        try:
            #创建一个ReuqestParser对象
            parser = reqparse.RequestParser()
            #添加参数
            parser.add_argument('cid', type=int,required=True,location='args')
            parser.add_argument('_type', type=str,required=True,location='args')
            #解析参数
            args = parser.parse_args()
            
            #根据cid获取信息
            cate = models.Category.query.get(args.get('cid'))
            attr_list = []
            if args.get('_type') == 'static':
                attr_list = [attr.to_dict() for attr in cate.attrs if attr._type == 'static']
            elif args.get('_type') == 'dynamic':
                attr_list = [attr.to_dict() for attr in cate.attrs if attr._type == 'dynamic']

            return  {'status':200,'message': '属性获取成功','data':attr_list}
        except Exception as e:
            return {'status':500,'message': '属性获取失败'}

    #添加属性
    def post(self):
        try:
            #创建一个ReuqestParser对象
            parser = reqparse.RequestParser()
            #添加参数
            parser.add_argument('name', type=str, required=True,)
            parser.add_argument('val', type=str,)
            parser.add_argument('_type', type=str,required=True,)
            parser.add_argument('cid', type=int,required=True,)
            #解析参数
            args = parser.parse_args()
            #判断参数是否传递
            if args.get('val'):
                attribute = models.Attributes(name=args.get('name'), val=args.get('val'), _type=args.get('_type'), cid=args.get('cid'))
            else:
                attribute = models.Attributes(name=args.get('name'), _type=args.get('_type'), cid=args.get('cid'))
            db.session.add(attribute)
            db.session.commit()
            return {'status':200,'message': '属性添加成功'}
        except Exception as e:
            return {'status':500,'message': '属性添加失败'}
attr_api.add_resource(Attributes,'/attributes/')

#获取单个数据
class Attribute(Resource):
    def get(self,id):
        try:
            #根据id获取信息
            attr = models.Attributes.query.get(id)
            return {'status':200,'message': '属性获取成功','data':attr.to_dict()}
        except Exception as e:
            print(e)
            return {'status':500,'message': '属性获取失败'}
    def put(self,id):
        try:
            #根据id获取信息
            attr = models.Attributes.query.get(id)
            #创建一个ReuqestParser对象
            parser = reqparse.RequestParser()
            #添加参数
            parser.add_argument('name', type=str)
            parser.add_argument('val', type=str)
            parser.add_argument('_type', type=str)
            parser.add_argument('cid', type=int)
            #解析参数
            args = parser.parse_args()
            #判断参数是否传递
            if args.get('val'):
                attr.val = args.get('val')
            if args.get('name'):
                attr.name = args.get('name')
            if args.get('_type'):
                attr._type = args.get('_type')
            if args.get('cid'):
                attr.cid = args.get('cid')
            db.session.commit()
            return {'status':200,'message': '属性修改成功'}
        except Exception as e:
            print(e)
            return {'status':500,'message': '属性修改失败'}
    def delete(self,id):
        try:
            #根据id获取信息
            attr = models.Attributes.query.get(id)  
            db.session.delete(attr)
            db.session.commit()
            return {'status':200,'message': '属性删除成功'}
        except Exception as e:
            print(e)
            return {'status':500,'message': '属性删除失败'}
attr_api.add_resource(Attribute,'/attribute/<int:id>/')

@cate_bp.route('/cate_grup/')
def cate_grup():
    '''
    根据level获取分类分组信息
    '''
    try:
        re = db.session.query(models.Category.level,func.count(1)).group_by(models.Category.level).all()

        #采用原生sql实现同样功能 复制情况下使用
        sql = 'select level,count(1) from t_category group by level'
        # sqlalchemy.exc.ArgumentError: Textual
        '''SQL expression 'select level,count(1)fro...' should be explicitly declared as text('select level,count(1) f
        # 这个错误就是告诉我们sql用声明是一个text文本'''
        rs = db.session.execute(text(sql)).all() # [(1,5),(2,20),(3,60)]

        data = {
            'name':'分类数量',
            'xAxis' : [f'{i[0]}级分类' for i in re],
            'series': [i[1] for i in re]
        }
        return {'status':200,'message': '分类分组获取成功','data':data}
    except Exception as e:
        return {'status':500,'message': '分类分组获取失败'}