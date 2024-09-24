<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Hmoe</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row :gutter="12">
            <el-col :span="8">
                <el-input v-model="user_data.queryName" style="max-width: 600px" placeholder="输入需要搜索的账号"
                    class="input-with-select">
                    <template #append>
                        <el-button :icon="Search" @click="searchUser" />
                    </template>
                </el-input>
            </el-col>
            <el-col :span="1">
                <el-button type="primary" :icon="CirclePlus" @click="addDialogVisible = true">增加用户</el-button>
            </el-col>
        </el-row>
        <el-row>

            <el-table :data="user_data.tableData " stripe class="table">
                <el-table-column prop="id" label="id" width="50" />
                <el-table-column prop="name" label="账号" width="100" />
                <el-table-column prop="nick_name" label="昵称" width="100" />
                <el-table-column prop="phone" label="手机号" />
                <el-table-column prop="email" label="邮箱" />
                <el-table-column prop="role_name" label="角色" />
                <el-table-column label="操作">
                    <template #default="scope">
                        <!-- scope.$index, scope.row前行的数值和当前行的索引当 -->
                        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
                            修改
                        </el-button>
                        <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
                            删除
                        </el-button>
                        <el-button size="small" type="success" @click="handleRest(scope.$index, scope.row)">
                            重置
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>

        <el-pagination v-model:current-page="user_data.pageNum" 
            v-model:page-size="user_data.pageSize"
            :page-sizes="pageSizes" :small="small" 
            :disabled="disabled" 
            :background="background"
            layout="total, sizes, prev, pager,next, jumper" 
            total="user_data.total" 
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange" class="table" />
    </el-card>
    <!-- 增加用户对话框 -->
    <el-dialog v-model="addDialogVisible" title="增加用户" width="500" :before-close="addFormRest">
        <el-form :model="user_form" :rules="user_rules" ref="addFormRef">
            <el-form-item label="用户名" :label-width="formLabelWidth" prop="name">
                <el-input v-model="user_form.name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="密码" :label-width="formLabelWidth" prop="pwd">
                <el-input v-model="user_form.pwd" autocomplete="off" />
            </el-form-item>
            <el-form-item label="确认密码" :label-width="formLabelWidth" prop="real_pwd">
                <el-input v-model="user_form.real_pwd" autocomplete="off" />
            </el-form-item>
            <el-form-item label="昵称" :label-width="formLabelWidth" prop="nick_namename">
                <el-input v-model="user_form.nick_namename" autocomplete="off" />
            </el-form-item>
            <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="user_form.phone" autocomplete="off" />
            </el-form-item>
            <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
                <el-input v-model="user_form.email" autocomplete="off">
                </el-input>
            </el-form-item>
            <el-form-item label="角色" :label-width="formLabelWidth" prop="rold_id">
                <el-select v-model="user_form.role_id" placeholder="请选择角色">
                    <el-option :label="r.name" :value="r.id" v-for="r in roles" :key="r.id" />
                </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="addFormRest">
                    取消
                </el-button>
                <el-button type="primary" @click="addUser(addFormRef)">
                    提交
                </el-button>
            </div>
        </template>
    </el-dialog>

    <!-- 编辑用户 -->
    <el-dialog v-model="editDialogVisible" title="修改用户">
        <el-form :model="edit_form" ref="editFormRef">
            <el-form-item label="用户名" :label-width="formLabelWidth" prop="name">
                <!-- disabled 禁用修改 -->
                <el-input v-model="edit_form.name" autocomplete="off" disabled />
            </el-form-item>
            <el-form-item label="昵称" :label-width="formLabelWidth" prop="nick_name">
                <el-input v-model="edit_form.nick_name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="手机号" :label-width="formLabelWidth" prop="phone">
                <el-input v-model="edit_form.phone" autocomplete="off" />
            </el-form-item>
            <el-form-item label="邮箱" :label-width="formLabelWidth" prop="email">
                <el-input v-model="edit_form.email" autocomplete="off" />
            </el-form-item>
            <el-form-item label="角色" :label-width="formLabelWidth" prop="rold_id">
                <el-select v-model="edit_form.role_id" placeholder="请选择角色">
                    <el-option :label="r.name" :value="r.id" v-for="r in roles" :key="r.id" />
                </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="editDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="editUser">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>
    <!-- 删除用户 -->
    <el-dialog v-model="deleteDialogVisible" title="删除用户">
        <span>确定要删除账号:{{remove_user.name}},昵称:{{remove_user.nick_name}}用户吗？</span>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="deleteDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="deleteUser">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>

    <!-- 重置用户 -->
    <el-dialog v-model="restDialogVisible" title="删除用户">
        <span>确定重置此账号:{{rest_user.name}},昵称:{{rest_user.nick_name}}用户吗？</span>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="restDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="restUserPassword">
                    确定
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue'
import { Search } from '@element-plus/icons-vue' //引入搜索栏
import { CirclePlus } from '@element-plus/icons-vue' //引入增加用户按钮
import api from '../api/index.js'
import { onMounted,reactive,ref } from 'vue';

const user_data = reactive({
    tableData:[],
    total : 0,
    pageNum : 1,
    pageSize : 5,
    queryName : ''
})
//增加用户
const user_form = reactive({
    name : null,
    pwd : null,
    real_pwd : null,
    phone : null,
    email : null,
    nick_name : null,
    role_id : null,
})

//编辑用户
let edit_form = reactive({
    id: null,
    name : null,
    nick_name : null,
    phone : null,
    email : null,
    role_id:null,

})
//删除用户
let remove_user = reactive({
    id : null,
    name:null,
    nick_name:null
})

//重置用户
let rest_user = reactive({
    id : null,
    name:null,
    nick_name:null
})

let pageSizes = ref([1,2,5,10]) //设置分页数据
const small = ref(false)
const background = ref(false)
const disabled = ref(false)
const formLabelWidth = '80px'  //用户弹出大小
const addDialogVisible = ref(false)
const addFormRef = ref(null) //获取表单实例
const editFormRef = ref(null) //获取编辑表单实例
const editDialogVisible = ref(false)
let userID = ref(0) //获取用户id
const deleteDialogVisible = ref(false) //删除用户弹窗
const restDialogVisible = ref(false) //删除用户弹窗
let roles = ref([]) //获取角色列表

onMounted(() => {
    get_user_list()
    get_role_list()
})

// 定义验证确认密码的规则 必须在验证用户信息之前
const validatePass2 = (rule, value,callback) => {
    if (value === '') {
        callback(new Error('请输入确认密码'))
    } else if (value !== user_form.pwd) {
        callback(new Error("2次密码不匹配!"))
    } else {
        callback()
    }
}
//判断手机输入规则
const validatePhone = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请输入手机号'))
    } else if (!/^1[3456789]\d{9}$/.test(value)) {
        callback(new Error("手机号格式不正确!"))
    } else {
        callback()
    }
}
//判断邮箱输入规则 callback继续执行
const validateEmail = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请输入邮箱'))
    } else if (!/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/.test(value)) {
        callback(new Error("邮箱格式不正确!"))
    } else {
        callback()
    }
}
//验证用户信息
const user_rules = reactive({
    name: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
    ],
    pwd: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
    ],
    real_pwd: [
        { required: true, message: '请输入确认密码', trigger: 'blur' },
        { validator: validatePass2, trigger: 'blur' }   //validator指向对应的解析规则函数
    ],
    phone: [{ validator: validatePhone, trigger: 'blur' }],
    nick_name: [
        { required: true, message: '请输入昵称', trigger: 'blur' },
        { min: 3, max: 5, message: '长度在 1 到 5 个字符', trigger: 'blur' }
    ],
    email: [{ validator: validateEmail, trigger: 'blur' }],
})



//搜索用户列表
const searchUser = () => {
    get_user_list()
}
const get_user_list = () => {
    let params = {
        'pnum' : user_data.pageNum,
        'psize' : user_data.pageSize,
        'name':user_data.queryName
    }
    api.get_user_list({params}).then(res => {
        //更新用户列表数据
        user_data.tableData = res.data.data.data
        
        //更新分页总数
        user_data.total = res.data.data.total
    })
}

const handleSizeChange = (val) => {
    // 修改每页显示多少条数据
    user_data.pageSize = val
    // 重新获取用户列表数据
    get_user_list()
}
const handleCurrentChange = (val) => {
    //初始化页码
    user_data.pageNum = 1
    //修改显示第几页数据
    user_data.pageNum = val
    // 重新获取用户列表数据
    get_user_list()
}

//重置表单
const addFormRest = () => {
    // 清空表单
    addFormRef.value.resetFields()
    // 关闭对话框 因为通过ref方式获取,所以需要.value去重新赋值
    addDialogVisible.value = false
}

//新增用户
const addUser = (formRef) => {
    // 表单预验证
    formRef.validate((valid) => {
        if (valid) {
            console.log('验证通过，可以提交')
            // 发送请求
            api.add_user(user_form).then(res => {
                if (res.data.status === 200) {
                    ElMessage({
                        message: res.data.msg,
                        type: 'success'
                    })
                    // 关闭对话框 调用写好的就行了
                    addFormRest()
                    // 重新获取用户列表数据
                    get_user_list()
                } else {
                    ElMessage.warning(res.data.msg)
                }
        })
        } else {
            ElMessage.error('验证失败')
            return false
        }
    })
}

// 编辑用户
const handleEdit = (index,row) => {
    // 显示编辑对话框
    editDialogVisible.value = true
    // edit_form = row //把当前行的数据赋值给编辑表单 多用户同时操作时,会脏读
    // 从数据库获取当前用户的数据
    api.get_user_by_id(row.id).then(res => {
        // 把当前行的数据赋值给编辑表单
        // edit_form = res.data.data  会很慢
        edit_form.name = res.data.data.name
        edit_form.nick_name = res.data.data.nick_name
        edit_form.phone = res.data.data.phone
        edit_form.email = res.data.data.email
        edit_form.role_id = res.data.data.role_id
        // console.log(res.data.data)
    })
    userID.value = row.id   //每次打开页面进行修改
} 

// 修改用户
const editUser = (formRef) => {
    // 表单预验证
    api.edit_user(userID.value,edit_form).then(res => {
        if (res.data.status === 200) {
            ElMessage({
                message: res.data.msg,
                type: 'success'
            })
            // 关闭对话框 调用写好的就行了
            editDialogVisible.value = false
            // 重新获取用户列表数据
            get_user_list()
        } else {
            ElMessage.warning(res.data.msg)
        }
    })

}

//删除用户
const handleDelete = (index,row) => {
    remove_user.id = row.id
    remove_user.name = row.name
    remove_user.nick_name = row.nick_name

    deleteDialogVisible.value = true
}
//执行删除用户操作
const deleteUser = () => {
    api.delete_user(remove_user.id).then(res => {
        if (res.data.status === 200) {
            ElMessage({
                message: res.data.msg,
                type: 'success'
            })
            // 关闭对话框 调用写好的就行了
            deleteDialogVisible.value = false
            // 重新获取用户列表数据
            get_user_list()
        } else {
            ElMessage.warning(res.data.msg)
        }
    })
}

//重置用户
const handleRest = (index,row) => {
    rest_user.id = row.id
    rest_user.name = row.name
    rest_user.nick_name = row.nick_name

    restDialogVisible.value = true
}
//执行重置用户操作
const restUserPassword = () => {
    console.log(rest_user.id)
    api.reset_user_pwassword(rest_user.id).then(res => {
        if (res.data.status === 200) {
            ElMessage({
                message: res.data.msg,
                type: 'success'
            })
            // 关闭对话框 调用写好的就行了
            restDialogVisible.value = false
            // 重新获取用户列表数据
            get_user_list()
        } else {
            ElMessage.warning(res.data.msg)
        }
    })
}
//获取角色列表
const get_role_list = () => {
    api.get_roles().then(res => {
        roles.value = res.data.data
    })
}
// //分配角色
// const handleRole = (index,row) => {
//     role_user.id = row.id
//     role_user.name = row.name
//     role_user.nick_name = row.nick_name
//     role_user.role_id = row.role_id

//     roleDialogVisible.value = true
    
// }
</script>


<style scoped>
    .box-card{
        margin-top: 20px;
    }
    .table{
        margin-top: 20px;
    }
</style>