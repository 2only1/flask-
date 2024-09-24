<template>
    <!-- 两个类 -->
    <div class="common-layout container">
        <el-container class="container">
            <el-header class="header">
                <div class="logo">
                    <img src="../assets/logo.png" alt="">
                    <span>电商后台管理系统</span>
                </div>
                <div class="user">
                    <el-button @click="logout">退出</el-button>
                </div>
            </el-header>
            <el-container>
                <el-aside class="aside">
                    <!-- router激活路由 -->
                    <el-menu active-text-color="#ffd04b" background-color="#001529" 
                        class="el-menu-vertical-demo" default-active="2" text-color="#fff" 
                        unique-opened router>
                        <el-sub-menu :index="index+''" v-for=" (item,index) in menulist.menus" :key="index">
                                <template #title>
                                    <el-icon> 
                                        <!-- <User />这是图标 -->
                                         <!-- 通过属性可以直接修值了 -->
                                        <component :is="menulist.icons[`${item.id}`]"></component>
                                    </el-icon>
                                    <span>{{item.name}}</span>
                                </template>
                            <el-menu-item :index="childItem.path" v-for="childItem in item.children" > 
                                {{childItem.name}} 
                            </el-menu-item>
                        </el-sub-menu>
                        
                    </el-menu>
                </el-aside>
                <el-main>
                    <!-- 子路由会跳转这里 -->
                    <router-view/>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>


<script setup>
    import { useRouter } from "vue-router";
    import api from "@/api/index.js";
    import { onMounted,reactive } from "vue";

    const menulist = reactive({
        menus:[],
        icons:{
            '1':'User',
            '2':'Tools',
            '3':'Goods',
            '4':'Shop',
            '5':'PieChart',
        }
    })
    const router = useRouter()
    const logout = () => {
        // 退出登录，清除token
        sessionStorage.removeItem('token')
        // 跳转到登录页
        router.push('/login')
    }
    //当dom元素加载完后调用
    onMounted(()=>{
        get_menu()
    })
    const get_menu = () =>{
        api.get_menus().then(res=>{
            menulist.menus = res.data.data
            // console.log(res.data.data)
        })
    }


</script>


<style scoped>
.header {
    background-color: #fff;
    box-shadow: 0 0 5px raba(0, 0, 0, 0.3);
    font-size: 20px;
    color: #999;
    height: 50px;
    width: 100%;
}

.logo {
    float: left;
    height: 50px;
    align-items: center;
    display: flex;
    justify-content: center;
}

/* 单独设置 logo的img元素 */
.logo img {
    width: 50px;
    height: 30px;
    margin-right: 10px;
}

.user {
    float: right;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
}

.aside {
    width: 200px;
    background-color: #001529;
}

.container {
    height: 100%;
}</style>