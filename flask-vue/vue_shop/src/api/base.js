/**
 * 存放所有网络请求地址
 */
const base = {

    baseUrl: "http://localhost:5000",    // 公共地址
    login: "/user/login/",    // 登录地址,拼接baseUrl
    // logout: "/user/logout/",
    get_menus: "/menu/menus/?type_=tree",    //获取菜单,树形结构返回
    get_menu_list: "/menu/menus/?type_=list",   //获取菜单列表,以列表形式返回
    get_users: "/user/users/",   //获取用户列表
    add_user: "/user/users/",   //添加用户 post请求
    get_user_by_id : "/user/user/",   //根据id获取用户信息
    edit_user: "/user/user/",   //编辑用户信息
    delete_user:'/user/user/', //删除用户
    reset_user_password:'/user/reset_pwd/', //重置密码
    get_roles: "/roles/",   //获取角色列表
    delete_role_menu:'/role/',   //删除角色菜单
    set_menu:'/role/',   //分配权限
    get_category: "/categorys/",   //获取商品分类
    add_category: "/categorys/",   //添加商品分类
    get_attr_by_category: "/attributes/",   //根据分类id获取属性
    add_attr: "/attributes/",   //添加属性
    add_attr_value:'/attribute/',   //添加属性值
    update_attr_value:'/attribute/',    //更新属性值
    get_product_list: "/products/",   //获取商品列表
    delete_product_list :"/product/" ,   //删除商品
    upload_img: "/upload_img/",   //上传图片
    add_product:'/products/',   //添加商品
    get_orders_list:'/orders/',   //获取订单列表
    get_express: "/express/",   //获取物流信息
    get_cate_group:'/cate_grup/',   //获取分类组
} 
export default base