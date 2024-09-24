<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Hmoe</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>商品列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row :gutter="12">
            <el-col :span="8">
                <!-- @clear清空后执行函数, clearable清楚搜索栏-->
                <el-input placeholder="请输入内容" v-model="productTable.searchKey" clearable @clear="getProductlist()">
                    <template #append>
                        <el-button icon="Search" @click="getProductlist()"></el-button>
                    </template>
                </el-input>
            </el-col>
            <el-col :span="4">
                <el-button type="primary" @click="AddProduct">添加商品</el-button>
            </el-col>
        </el-row>
        <el-row>
            <el-table :data="productTable.data" style="width: 100%">
                <el-table-column type="index" />
                <!--  show-overflow-tooltip是隐藏内容 -->
                <el-table-column prop="name" label="商品名称"  show-overflow-tooltip/>
                <el-table-column prop="price" label="商品价格"  width="150px"/>
                <el-table-column prop="number" label="商品数量" width="150px"/>
                <el-table-column prop="state" label="商品状态"  width="150px"/>
                <el-table-column label="操作" >
                    <template #default="scope">
                        <el-button type="primary" size="small">编辑</el-button>
                        <el-button type="danger" size="small" @click="removeProduct(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
</template>

<script setup>
import { ArrowRight,Search } from '@element-plus/icons-vue'
import { ref,onMounted,reactive } from 'vue'
import api from '../api/index'
import { useRouter } from 'vue-router'


const productTable = ref({
    data : [],
    searchKey : null
})
const router = useRouter()
onMounted(() => {
    getProductlist()
})

//响应所有数据
const getProductlist = (name) => {
    api.get_product_list(productTable.value.searchKey).then(res => {
        // console.log(res.data.data)
        // console.log(productTable)
        //响应数据保存
        productTable.value.data = res.data.data
    })
}

//删除对应数据
const removeProduct = (row) => {
    // console.log(id)
    ElMessageBox.confirm(
        '是否要删除' + row.name + '该商品？',
        '删除商品',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        // 调用删除商品接口
        api.delete_product_list(row.id).then(res => {
            if (res.data.status == 200) {
                ElMessage({
                    type: 'success',
                    message: res.data.msg,
                })
                // 删除成功后重新获取商品列表
                getProductlist()
            } else {
                ElMessage({
                    type: 'info',
                    message: res.data.msg,
                })
            }

        })
    }).catch(() => {
            ElMessage({
                type: 'info',
                message: '已取消删除',
            })
        })
}
const AddProduct = () => {
    router.push('/add_product')
}
</script>

<style scoped>

.box-card {
        margin-top: 20px;
    }

</style>