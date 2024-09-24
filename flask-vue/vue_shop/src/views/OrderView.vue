<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Hmoe</el-breadcrumb-item>
        <el-breadcrumb-item>订单管理</el-breadcrumb-item>
        <el-breadcrumb-item>订单列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-row :gutter="12">
            <el-col :span="8">
                <el-input style="max-width: 600px" placeholder="输入需要搜索的订单" clearable>
                    <template #append>
                        <el-button :icon="Search" @click="searchUser" />
                    </template>
                </el-input>
            </el-col>
        </el-row>

        <el-row>
            <el-table :data="orderTable.data" stripe >
                <el-table-column type="index" label="ID" width="50"/>
                <el-table-column prop="user" label="订单用户" width="150"/>
                <el-table-column prop="price" label="订单价格" width="120" />
                <el-table-column prop="number" label="订单数量" width="100" />
                <el-table-column prop="pay_status" label="是否支付" width="100">
                    <template #default="scope">
                        <el-tag v-if="scope.row.pay_status === 0" type="danger">未支付</el-tag>
                        <el-tag v-else type="success">已支付</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="is_send" label="是否发货" width="100">
                    <template #default="scope">
                        <el-tag v-if="scope.row.is_send === 0" type="danger">未发货</el-tag>
                        <el-tag v-else type="success">已发货</el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <!-- scope.$index, scope.row前行的数值和当前行的索引当 -->
                        <el-button size="small" type="primary" @click="showExpress(scope.row.id)">
                            查看物流
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-row>
    </el-card>
    <!-- 显示物流信息 -->
    <el-dialog v-model="expressDialogVisible" title="物流信息" width="50%">
        <el-timeline>
            <!-- :timestamp设置时间 -->
            <el-timeline-item v-for="(item, index) in expressInfo.data" :key="index" :timestamp="item.update_time">
                {{ item.content }}
            </el-timeline-item>
        </el-timeline>
    </el-dialog>
</template>

<script setup>
import { ArrowRight, Search } from '@element-plus/icons-vue'
import { reactive,onMounted,ref } from 'vue'
import api from '../api/index.js'

onMounted(() => {
    get_order_list()
})

const orderTable = reactive({
    data: [],
})

//定义物流信息弹窗是否显示
let expressDialogVisible = ref(false)
//定义物流信息
let expressInfo = reactive({
    data: [],
})


//获取订单信息
const get_order_list = () => {
    api.get_orders_list().then(res => {
        orderTable.data = res.data.data
        console.log(res.data.data)
    })
}

// 查看物流
const showExpress = (id) => {
    expressDialogVisible.value =true
    api.get_express(id).then(res=>{
        expressInfo.data = res.data.data
        console.log(expressInfo.data)
    })
}
</script>

<style scoped>
.box-card {
    margin-top: 20px;
}
</style>