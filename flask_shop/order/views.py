from flask_restful import Resource,reqparse
from flask_shop import models,db
from . import order_api

class Orders(Resource):
    def get(self):
        #定义解析器
        parser = reqparse.RequestParser()
        #添加参数
        parser.add_argument('name',type=str,location='args')
        #获取参数
        args = parser.parse_args()
        name = args.get('name')
        if name:
            orders_list = models.Order.query.filter(models.Order.name.like(f'%{name}%')).all()
        else:
            orders_list = models.Order.query.all()
        return {
            'status':200,
            'msg':'获取订单成功',
            'data':[order.to_dict() for order in orders_list]
        }
order_api.add_resource(Orders,'/orders/')

class Order(Resource):
    def get(self,id):
        '''
        通过id获取单个用户订单
        '''
        order = models.Order.query.get(id)
        if order:
            return {
                'status':200,
                'msg':'获取订单成功',
                'data':order.to_dict()
            }
        else:
            return {
                'status':404,
                'msg':'订单不存在'
            }
order_api.add_resource(Order,'/order/<int:id>/')

#物流信息
class Expresses(Resource):
    def get(self,id):
        '''
        获取快递列表
        :param id:订单id
        '''
        #order_by根据时间排序,.desc()降序
        express_list = models.Express.query.filter(models.Express.oid==id).order_by(models.Express.update_time.desc()).all()
        return {
            'status':200,
            'msg':'获取快递信息成功',
            'data':[express.to_dict() for express in express_list]
        }
order_api.add_resource(Expresses,'/express/<int:id>/')