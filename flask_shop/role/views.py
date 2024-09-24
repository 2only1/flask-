from flask_restful import Resource,reqparse,request
from flask_shop import models,role,db
from flask_shop.role import role_api,role_bp
from flask import request

#多个角色
class Roles(Resource):
    def get(self):
        try:
            roles = models.Role.query.all()
            roles_list = [role.to_dict() for role in roles]
            return {'status': 200, "message": "获取角色成功","data": roles_list}
        except Exception as e:
            return {"message": "获取角色失败", "error": str(e)}
    def post(self):
        try:
            #添加角色
            role_name = request.json.get("name")
            #获取角色描述信息
            role_desc = request.json.get("desc")
            role_list = models.Role(name=role_name,desc=role_desc)
            db.session.add(role_list)
            db.session.commit()
            return {"message": "添加角色成功"}
        except Exception as e:
            return {"message": "添加角色失败"}
role_api.add_resource(Roles, "/roles/")

#单个角色
class Role(Resource):   
    def delete(self,role_id):
        try:
            role = models.Role.query.get(role_id)
            db.session.delete(role)
            db.session.commit()
            return {"message": "删除角色成功"}
        except Exception as e:
            return {"message": "删除角色失败"}
    #修改数据
    def put(self,role_id):
        try:
            role = models.Role.query.get(role_id)
            parser = reqparse.RequestParser()
            #添加参数
            parser.add_argument("name", type=str, required=True, help="角色名不能为空")
            parser.add_argument("desc", type=str,)
            #解析数据
            args = parser.parse_args()
            if args.get("name"):
                role.name = args.get("name")
            if args.get("desc"):
                role.desc = args.get("desc")
            db.session.commit()
            return {"message": "修改角色成功"}
        except Exception as e:
            return {"message": "修改角色失败"}
        
role_api.add_resource(Role, "/role/<int:role_id>")

#删除角色权限功能
@role_bp.route('/role/<int:rid>/<int:mid>/')
def del_menu(rid:int,mid:int):
    try:
        #获取角色
        role = models.Role.query.get(rid)
        #获取权限
        menu = models.Menu.query.get(mid)
        #判断是否都不为空
        if all([role,menu]):
            #判断当前角色的当前菜单权限
            if menu in role.menus:
                    #删除角色的当前权限
                    role.menus.remove(menu)
                    #判断当前菜单是否有子菜单
                    if menu.level == 1:
                        #删除角色权限,父菜单的所有子菜单权限
                        for temp in menu.children:
                            #判断角色是否有该权限的子权限
                            if temp in role.menus:
                                role.menus.remove(temp)
            else:
                return {'status':404,"message": "角色权限不存在"}
        db.session.commit()
        return {'status':200,"message": "删除角色权限成功"}
    except Exception as e:
        return {"status":"500","message": "角色或菜单不存在"}


@role_bp.route('/role/<int:rid>/',methods=['post'])
def ser_menu(rid:int):
    try:
        #获取角色
        role = models.Role.query.get(rid)
        #获取权限
        mids = request.get_json().get('mids')
        #清空角色权限
        role.menus = []
        #遍历要分配的权限
        # mids = mids.split(',')
        for mid in mids:
            #获取权限
            menu = models.Menu.query.get(int(mid))
            #判断当前权限是否存在
            if menu:
                #添加权限
                role.menus.append(menu) 
        db.session.commit()
        return {'status':200,"message": "添加角色权限成功"}
    except Exception as e:
        return {"status":500,"message": "分配权限失败"}
