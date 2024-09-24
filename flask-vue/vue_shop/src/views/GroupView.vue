<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Hmoe</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>分类列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row>
            <el-button type="primary" icon="CirclePlus" @click="addCateDialog">添加分类</el-button>
        </el-row>
        <el-row>
            <el-table :data="tableData.data" style="width: 100%; margin-bottom: 20px" row-key="id" border
                >
                <el-table-column prop="id" label="ID" sortable />
                <el-table-column prop="name" label="分类名称" sortable />
                <el-table-column prop="level" label="分类等级" sortable>
                    <template #default="scope">
                        <el-tag v-if="scope.row.level == 1" type="success">一级</el-tag>
                        <el-tag v-else-if="scope.row.level == 2" type="warning">二级</el-tag>
                        <el-tag v-else-if="scope.row.level == 3" type="">三级</el-tag>

                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <el-button type="primary" size="small" :icon="Edit">编辑</el-button>
                    <el-button type="danger" size="small" :icon="Delete">删除</el-button>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
    <!-- 添加分类 -->
    <el-dialog v-model="addDialogVisible" title="添加分类" width="30%">
        <el-form :model="addForm" :rules="addRules" ref="addFormRef" label-width="100px">
            <el-form-item label="分类节点" prop="pid">
                <el-cascader v-model="value" :options="options.data" :props="props" @change="handleChange" separator=" > "
                    clearable/>
            </el-form-item>
            <el-form-item label="分类名称" prop="name">
                <el-input v-model="addForm.name"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addCate">确定</el-button>
                <el-button @click="addDialogVisible = false">取消</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue'
import { onMounted, reactive, ref } from 'vue';
import api from '../api/index.js'
import { Edit,Delete } from '@element-plus/icons-vue'

let addDialogVisible = ref(false)
const addForm = reactive({
    name:'',
    pid:0,
    level:1,
})

const tableData = reactive({  
    data:[]
})

const value = ref([])
const options = reactive({
    data:[]
})
const props = {
    expandTrigger: 'hover',
    label: 'name',
    value: 'id',
    checkStrictly:true,  
}


onMounted(() => {
    get_catagory()
    get_options()
})
const get_catagory = () => {
    api.get_category(3).then(res => {
        tableData.data = res.data.data
        console.log(res.data)
    })
}
//添加分类
const addCateDialog = () => {
    addDialogVisible.value = true
}
//添加分类规则
const addRules = reactive({
    name: [
        { required: true, message: '请输入分类名称', trigger: 'blur' },
    ],
})

//级联选择器
const handleChange = (value) => {
    if (value){
        if(value.length == 1){
            addForm.pid = value[0]
            addForm.level = 2
        }else if (value.length == 2) {
            addForm.pid = value[1]
            addForm.level = 3
        }
    }else{
        addForm.pid = 0
        addForm.level = 1
    }
}
const get_options = () => {
    api.get_category(2).then(res => {
        options.data = res.data.data
    })

}

//添加分类
const addCate = () => {
    api.add_category(addForm).then(res => {
        console.log(res.data)
        addDialogVisible.value = false
        get_catagory()
        get_options()
    })
}

</script>

<style scoped> 
    .box-card {
        margin-top: 20px;
    }
</style>