<template>
    <div class="main">
        <div class="login">
            <div class="logo">
                <img src="../assets/logo.png" alt="">
            </div>
            <!-- ref 创建一个对一个 DOM 元素的引用 且只能加在el-form-->
            <el-form :model="user" class="user_form" :rules="userRlues" ref="userFormRef">
                <el-form-item prop="name">
                    <!-- placeholder 内嵌 prefix-icon 前缀图标 -->
                    <el-input v-model="user.name" placeholder="用户名" :prefix-icon="User" autocomplete="off"/>
                </el-form-item>
                <el-form-item prop="pwd">
                    <el-input v-model="user.pwd" placeholder="密码" :prefix-icon="Lock" />
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="primary" @click="submitForm(userFormRef)">登录</el-button>
                    <el-button type="success" @click="resetForm(userFormRef)">清空信息</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<!-- vue3添加setup -->
<script setup>
import { reactive, ref } from 'vue'
import { Lock, User } from '@element-plus/icons-vue'
import api from '@/api/index.js'    //@表示当前项目根目录
// import { ElMessage } from 'element-plus'    //采用按需引入后,不需要特意声明
import { useRouter } from 'vue-router'


const user = reactive({
    name: '',
    pwd: ''
})

//创建路由实例
const router = useRouter()

//定义表单规则
const userRlues = reactive({
    name: [
        // 该字段是必填;字段验证失败显示提示信息;触发验证的事件，有 blur（失去焦点时触发）
        { required: true, message: '用户名不能为空', trigger: 'blur' },
        { min: 3, max: 10, message: '用户名长度在3到10个字符', trigger: 'blur' }
    ],
    pwd: [
        { required: true, message: '密码不能为空', trigger: 'blur' },
    ]
})
//定义表单数据  必须初始化
const userFormRef = ref(null)

//定义重置表单方法
const resetForm = (formRef) => {
    formRef.resetFields()
}

//定义登录预功能
const submitForm = (formRef) => {
    formRef.validate((valid) => {
        if (valid) {
            console.log('验证通过，可以提交!')
            api.getLogin(user).then(res=>{
                //根据响应的状态码返回不同处理
                if (res.data.status === 200) {
                    ElMessage({
                        message: res.data.msg,
                        type: 'success',
                    });
                    //将token保存到会话存储中
                    sessionStorage.setItem('token', res.data.data.token)
                    // localStorage.setItem('token', JSON.stringify(res.data.data.token))
                    //跳转到首页
                    router.push('/')
                }else {
                    ElMessage({
                        message: res.data.msg,
                        type: 'error',
                    })
                }
            })
        } else {
            console.log('验证失败')
            return false
        }
    })
}
</script>
  
<style scoped>
.main {

    width: 100%;
    height: 100%;
    background-color: rgb(134, 25, 128);
    /* 允许元素在水平或垂直方向上排列其子元素 */
    display: flex;
    /* 让元素的所有子元素在水平方向上居中 */
    justify-content: center;
    /* 元素的所有子元素在垂直方向上居中 */
    align-items: center;
}

.login {
    width: 450px;
    height: 300px;
    background-color: white;
    /* 元素的边框半径为5像素 */
    border-radius: 5px;
}

.logo {
    width: 200px;
    /* 设置元素边框为1像素宽，颜色为浅灰色（#eee） */
    border: 1px solid #eee;
    /* 素在水平方向上居中，即左右边距为0，上下边距为自动 */
    margin: 0 auto;
    /* 设置元素上边距为-65像素,向上移动 */
    margin-top: -85px;
    /* 元素内边距为5像素 */
    padding: 5px;
    /* 设置元素边框圆角为5像素 */
    border-radius: 5px;
    /* 元素阴影，水平偏移为0，垂直偏移为0，模糊半径为10像素，颜色为浅灰色（#ddd） */
    box-shadow: 0 0 10px #cabdbd;
}

img {
    width: 100%;
    height: 100%;
}

.user_form {
    padding: 50px;
}

.btns {
    display: flex;
    /* 水平方向上平均分布，两侧的子元素距离父元素边缘为其他子元素的一半。 */
    justify-content: space-between;
}

/* 选择btns的所有按钮 */
.btns button {
    /* flex属性设置为1时，元素将占据容器所有可用空间的一等份 */
    flex: 1;
}</style>
