import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import WelcomeView from '../views/WelcomeView.vue'
import UsersView from '../views/UsersView.vue'
import MenuView from '../views/MenuView.vue'
import { nextTick } from 'vue'
import { componentSizes } from 'element-plus'

const routes = [

  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "home" */ '../views/HomeView.vue'),
    redirect:'/welcome', //自动跳转到这个路由
    children:[
      {
        path:'/welcome',
        name: 'welcome',
        component: WelcomeView,
      },
      {
        path:'/user_list',
        name: 'user_list',
        component: () => import(/* webpackChunkName: "users" */ '../views/UsersView.vue'),
      },
      {
        path:'/role_list',
        name: 'role_list',
        component: () => import(/* webpackChunkName: "roles" */ '../views/MenuView.vue'),
      },
      {
        path: '/author_list',
        name: 'author_list',
        component: () => import(/* webpackChunkName: "roles" */ '../views/AuthorView.vue'),
      },
      {
        path: '/group_list',  
        name: 'group_list',
        component: () => import(/* webpackChunkName: "roles" */ '../views/GroupView.vue'),
      },
      {
        path: '/attribute_list',
        name: '/attribute_list',
        component: () => import(/* webpackChunkName: "roles" */ '../views/AttributeView.vue'),
      },
      {
        path: '/product_list',
        name: '/product_list',
        component: () => import(/* webpackChunkName: "roles" */ '../views/ProductView.vue'),
      },
      {
        path: '/add_product',
        name: '/add_product',
        component: () => import(/* webpackChunkName: "roles" */ '../views/AddProductView.vue'),
      },
      {
        path: '/order_list',
        name: '/order_list',
        component: () => import(/* webpackChunkName: "roles" */ '../views/OrderView.vue'),
      },
      {
        path: '/data_list',
        name: '/data_list',
        component: () => import(/* webpackChunkName: "roles" */ '../views/DataView.vue'),
      }
    ]
  },
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


//做一个touter跳转login_required验证器
router.beforeEach((to, from, next) => {
  if (to.path == '/login'){
    next()
  }else{
    //获取token值
    const token = sessionStorage.getItem('token') ? next() : next('/login')
  }
})
export default router