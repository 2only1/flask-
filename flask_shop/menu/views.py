from flask_restful import Resource
from . import menu_api
from flask_shop.models import Menu
from flask import request

#Resource 实现请求方式功能
class Menus(Resource):
    def get(self):
        #获取前端页面要求的数据类型,是list还是tree
        type_ = request.args.get('type_')
        #判断数据是否为tree 
        if type_ == 'tree':
            #通过模型获取数据,会tree形式返回
            menu_tree = Menu.query.filter(Menu.level==1).all()
            #创建子列表,存储json
            menu_data = []
            #遍历数据
            for m in menu_tree:
                #添加数据,将数据转换为json格式
                menu_data.append(m.to_dict_tree())
            #返回数据
            return  {'status':200,'msg':'获取菜单成功','data':menu_data}
        #否则为list
        elif type_ == 'list':
            #通过模型获取数据吗,!=0就能获取所以数据
            menu_list = Menu.query.filter(Menu.level!=0).all()
            #创建子列表,存储json
            menu_data = []
            #遍历数据
            for m in menu_list:
                #添加数据
                menu_data.append(m.to_dict_list())
            #返回数据
            return  {'status':200,'msg':'获取菜单成功','data':menu_data}
        else:
            return {'status':400,'msg':'参数错误'}

#建立路由关系
menu_api.add_resource(Menus,'/menus/')