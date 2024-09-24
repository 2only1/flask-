<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Hmoe</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>添加商品</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-alert title="下面输入要《添加商品》的信息" type="info" center show-icon />
        <!-- 字符串默认-0会变整型 保证steps和tabs传入的数据为统一类型-->
        <el-steps :active="active - 0" finish-status="success" align-center>
            <el-step title="基本信息" />
            <el-step title="商品静态属性" />
            <el-step title="商品动态属性" />
            <el-step title="商品图片" />
            <el-step title="商品内容" />
            <el-step title="完成" />
        </el-steps>
        <el-tabs tab-position="left " class="el-tabs" v-model="active" :before-leave="beforeLeave">
            <el-form :model="addForm" ref="addFormRef" label-width="80px" :rules="addFormRules">
                <!-- :表示传入为整型 -->
                <el-tab-pane label="基本信息" :name="0">
                    <el-form-item label="商品名称" prop="name">
                        <el-input v-model="addForm.name" placeholder="请输入商品名称" />
                    </el-form-item>
                    <el-form-item label="商品价格" prop="price">
                        <el-input v-model="addForm.price" placeholder="请输入商品价格" />
                    </el-form-item>
                    <el-form-item label="商品库存" prop="number">
                        <el-input v-model="addForm.num" placeholder="请输入商品库存" />
                    </el-form-item>
                    <el-form-item label="商品权重" prop="weight">
                        <el-input v-model="addForm.weight" placeholder="请输入商品权重" />
                    </el-form-item>
                    <el-form-item label="商品分类">
                        <el-cascader :options="options.data" :props="props" separator=" > " clearable
                            v-model="options.selectID" @change="changeSelect" style="width: 300px;" />
                    </el-form-item>
                </el-tab-pane>
                <el-tab-pane label="商品静态属性" :name="1">
                    <el-form-item :label="s.name" v-for="s in attrData.static" :key="s.id">
                        <el-input v-model="s.val" />
                    </el-form-item>
                </el-tab-pane>
                <el-tab-pane label="商品动态属性" :name="2">
                    <el-form-item :label="d.name" v-for="d in attrData.dynamic" :key="d.id">
                        <el-checkbox-group v-model="d.val">
                            <el-checkbox :label="v" name="type" v-for="(v, i) in d.val " :key="i" border />
                        </el-checkbox-group>
                    </el-form-item>
                </el-tab-pane>
                <el-tab-pane label="商品图片" :name="3">
                    <!-- action上传服务器地址 -->
                    <el-upload v-model:file-list="fileList" :action="base.baseUrl + base.upload_img" list-type="picture"
                        :on-success="handleSuccess" :on-remove="handleRemove" :on-preview="handlePreview">
                        <el-button type="primary">上传图片</el-button>
                    </el-upload>
                </el-tab-pane>
                <el-tab-pane label="商品内容" :name="4">
                    <EditorComponent @onDataEvent="getDataHandler" />
                    <el-button type="primary" @click="addProduct">添加商品</el-button>
                </el-tab-pane>
            </el-form>
        </el-tabs>
    </el-card>
    <el-dialog title="图片预览" v-model="dialogVisible" width="50%" >
        <img :src="preImageSrc" class="pre-image" />
    </el-dialog>
</template>

<script setup>

import { ArrowRight, } from '@element-plus/icons-vue'
import { ref, reactive, onMounted } from 'vue'
import api from '../api/index'
import base from '../api/base';
import EditorComponent from '@/components/EditorComponent.vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const active = ref(0)
const addForm = reactive({
    name: '',
    price: '',
    num: '',
    weight: '',
    cid_one: null,
    cid_two: '',
    cid_three: '',
    pics: [],
    introduce : '',
    attr_static:[],
    attr_dynamic:[]
})

//创建级联显示器
const options = reactive({
    data: [],
    selectID: null
})
const props = {
    expandTrigger: 'hover',
    label: 'name',
    value: 'id',
}

const addFormRef = ref(null)

const attrData = reactive({
    static: [],
    dynamic: []
})

//获取商品分类数据
onMounted(() => {
    get_category()
})
//定义级联的change事件
const changeSelect = (value) => {
    if (options.selectID) {
        if (options.selectID.length == 3) {
            //更新表单ID
            addForm.cid_one = options.selectID[0]
            addForm.cid_two = options.selectID[1]
            addForm.cid_three = options.selectID[2]
        }
    }
    //测试表单数据
    // console.log(addForm)
    // console.log(options.selectID)

}
const get_category = () => {
    api.get_category(3).then(res => {
        options.data = res.data.data
    })
}

//定义图片预览地址
let preImageSrc = ref('')

//定义表单验证规则
const addFormRules = reactive(
    {
        name: [
            { required: true, message: '请输入商品名称', trigger: 'blur' },
            { min: 2, max: 15, message: '长度在 2 到 15 个字符', trigger: 'blur' },
        ],
        price: [
            { required: true, message: '请输入商品价格', trigger: 'blur' },
            //transform将输入内容强制转换为数字
            { type: 'number', message: '商品价格必须为数字值', trigger: 'blur', transform: (value) => Number(value) },
        ],
        num: [
            { required: true, message: '请输入商品库存', trigger: 'blur' },
            { type: 'number', message: '商品价格必须为数字值', trigger: 'blur', transform: (value) => Number(value) },
        ],
        weight: [
            { required: true, message: '请输入商品权重', trigger: 'blur' },
            { type: 'number', message: '商品价格必须为数字值', trigger: 'blur', transform: (value) => Number(value) },
        ],
    }
)

//定义切换标签时的钩子函数
const beforeLeave = (tab, event) => {
    //判断是否选择了前3及分类
    if (options.selectID) {
        if (options.selectID.length == 3) {
            //获取静态属性
            getAttr(options.selectID[2], 'static')
            getAttr(options.selectID[2], 'dynamic')
            return true
        }
    }
    //如果未选择则提示
    ElMessage.error('请选择商品分类')
    return false
}

//获取属性
const getAttr = (s_key, s_type) => {
    // console.log(s_key,s_type)
    if (s_type === 'static') {
        api.get_attr_by_category(s_key, s_type).then(res => {
            attrData.static = res.data.data
        })
    } else if (s_type === 'dynamic') {
        api.get_attr_by_category(s_key, s_type).then(res => {
            //遍历每个动态属性的值
            res.data.data.forEach(item => {
                //将动态值转换数组
                item.val = item.val ? item.val.split(',') : []
                // console.log(item.val)
            });
            attrData.dynamic = res.data.data

        })
    }
}

//定义一个上传图片功能
const fileList = ref([
])
//图片上传成功提示
const handleSuccess = (response, file, fileList) => {
    if (response.status == 200) {
        ElMessage({
            type: 'success',
            message: '上传图片成功'
        })
        //将上传成功的图片地址添加到表单中
        addForm.pics.push(response.data.path)

    } else {
        ElMessage.error('上传失败')
    }
}

//定义删除图片功能
const handleRemove = (uploadFile, uploadFiles) => {
    //删除图片地址
    let removePath = uploadFile.response.data.path
    // 获取要删除的图片的索引
    let index = addForm.pics.indexOf(removePath)
    //删除addForm中的图片,要删除的索引,要删除的个数
    addForm.pics.splice(index, 1)
}

//定义图片预览功能
const dialogVisible = ref(false)
//定义预览事件
const handlePreview = (uploadFile) => {
    // 显示预览框
    dialogVisible.value = true
    // 修改预览图片的地址
    preImageSrc.value = uploadFile.response.data.url
}

//定义富文本编辑器
const getDataHandler = (data) => {
    addForm.introduce = data
}

//定义提交表单数据
const addProduct = () => {
    addForm.attr_dynamic = attrData.dynamic
    addForm.attr_static = attrData.static
    //提交表单
    api.add_product(addForm).then(res => {
        if (res.data.status == 200) {
            ElMessage({
                type: 'success',
                message:  '添加商品成功'
            })
            //跳转到商品列表
            router.push('/product_list')
        } else {
            ElMessage({
                type: 'error',
                message: '商品添加失败'
            })
            }
    })
}
</script>

<style scoped>
.box-card {
    margin-top: 20px;
}

.el-tabs {
    margin-top: 20px;
}

.pre-image{
    width: 100%;
}
</style>