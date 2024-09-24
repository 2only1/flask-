<template>
    <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">Hmoe</el-breadcrumb-item>
        <el-breadcrumb-item>商品管理</el-breadcrumb-item>
        <el-breadcrumb-item>属性列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card class="box-card">
        <el-alert title="分类属性可以选择最后一级" type="warning" class="alert"></el-alert>
        <div>
            <span class="attr_title">选择分类</span>
            <el-cascader :options="options.data" :props="props" separator=" > " clearable class="cascader"
                v-model="options.selectID" @change="changeSelect" />
        </div>
        <div>
            <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
                <el-tab-pane label="静态属性" name="static">
                    <el-button type="primary" size="small" @click="addDialogVisible = true"
                        :disabled="isButtonVisible">添加属性</el-button>
                    <el-table :data="attrData.static">
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="属性名称" width="180" prop="name"></el-table-column>
                        <el-table-column label="属性值" width="180" prop="name"></el-table-column>
                        <el-table-column label="操作">
                            <template #default="scope">
                                <el-button type="primary" size="small">编辑</el-button>
                                <el-button type="danger" size="small">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane label="动态属性" name="dynamic">
                    <el-button type="primary" size="small" @click="addDialogVisible=true"
                        :disabled="isButtonVisible">添加属性</el-button>
                    <el-table :data="attrData.dynamic" row-key="id">
                        <el-table-column type="expand">
                            <template #default="scope">
                                <el-tag v-for="(item,i) in scope.row.val" class="e-tag" closable @close="closeTag(scope.row.id, scope.row.val,i)">{{ item }}</el-tag>
                                <TagComponents @addTagEvent="getTagValue" :row="scope.row" />
                            </template>
                        </el-table-column>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="属性名称" width="180" prop="name"></el-table-column>
                        <el-table-column label="操作">
                            <template #default="scope">
                                <el-button type="primary" size="small">编辑</el-button>
                                <el-button type="danger" size="small">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>
        </div>
    </el-card>
    <el-dialog :title="dialogTitile" width="30%" v-model="addDialogVisible" :before-close="addDialogClose">
        <el-form :model="addForm" label-width="80px" :rules="addRules" ref="addRef">
            <el-form-item label="属性名称" prop="name">
                <el-input v-model="addForm.name"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addAttr">确定</el-button>
                <el-button @click="addDialogVisible=false">取消</el-button>
            </el-form-item>
        </el-form>
    </el-dialog>
</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue'
import api from '@/api/index.js'
import { onMounted,reactive,ref,computed,nextTick } from 'vue'
import TagComponents from '@/components/TagComponents.vue'; //将其他vue引入可以在html中直接使用
import { ElMessage } from 'element-plus';
const options = reactive({
    data:[],
    selectID:null
})
const props = {
    expandTrigger: 'hover',
    label: 'name',
    value: 'id',
}
const attrData = reactive({
    static:[],
    dynamic:[]
})
const activeName = ref('static')

const addForm = reactive({
    name:'',
})
const flag = reactive({
    static:false,   //f表示不可获取，t表示可获取
    dynamic:false
})
const addDialogVisible = ref(false)
const dialogTitile = ref('添加属性')


let isButtonVisible = computed(() => {
    // computed:通过函数判断是否赋值
    if (options.selectID && options.selectID.length == 3) {
        return false
    }
    return true
})

const addRules = {
    name: [
        { required: true, message: '请输入属性名称', trigger: 'blur' },
    ],
}
const addRef = ref(null)
onMounted(() => {
    get_category()
})
const get_category = () => {
    api.get_category(3).then(res => {
        options.data = res.data.data
    })
}
const handleClick = (tab, event) => {
    //   console.log(tab.props.name)
    //   console.log(options.selectID)
    if (tab.props.name == 'static') {
        dialogTitile.value = '添加静态属性'
    } else if (tab.props.name == 'dynamic') {
        dialogTitile.value = '添加动态属性'
    }
    //根据flag表示判断是否获取属性数据
    if (options.selectID) {
        if (options.selectID.length == 3) {
            let selectkey = options.selectID[2]
            let _type = tab.props.name
            //根据flag表示判断是否获取属性数据
            if(_type=='static' && !flag.static) return
            if(_type=='dynamic' && !flag.dynamic) return
            get_attr(selectkey,_type)
            
        }
    }
}
//级联选择器
const changeSelect = (value) => {
    if (value) {
        if (value.length == 3) {
            let selectkey = value[2]
            let _type = activeName.value
            //设置静态属性重新获取
            flag.static = true
            //设置动态属性重新获取
            flag.dynamic = true
            get_attr(selectkey,_type)
        }
    }else {
        attrData.static = []
        attrData.dynamic = []
    }
    
}
//获取属性
const get_attr = (s_key,s_type) => {
    // console.log(s_key,s_type)
    if (s_type === 'static') {
        api.get_attr_by_category(s_key,s_type).then(res => {
            attrData.static = res.data.data
            //设置静态属性不在获取
            flag.static = false
        })
    } else if (s_type === 'dynamic') {
        api.get_attr_by_category(s_key,s_type).then(res => {
            //遍历每个动态属性的值
            res.data.data.forEach(item => {
                //将动态值转换数组
                item.val = item.val?item.val.split(','):[]
            });
            attrData.dynamic = res.data.data
            //设置动态属性不在获取
            flag.dynamic = false

        })
    }
}

const addDialogClose = () => {
    addRef.value.resetFields()
    addDialogVisible.value = false
}
//增加商品分类属性
const addAttr = () => {
    console.log(addForm.value)
    let params = {
        "name":addForm.name,
        "_type":activeName.value,
        "cid":options.selectID[2],
    }
    api.add_attr(params).then(res => {
        get_attr(options.selectID[2],activeName.value)
        addDialogClose()
    })
}

//收集增加动态属性input值的数据
const getTagValue = (val) => {
    // console.log(tag.inputvalue)  //属性值
    // console.log(tag.row.id)  //属性id
    // 将新输入的输增加到原来的数组中
    val.row.val.push(val.inputvalue)
    // 封装接口所需数据
    let params = {
        '_type':activeName.value,
        'val':val.row.val.join(",")
    }
    //发送请求
    api.add_attr_value(val.row.id,params,).then(res => {
        ElMessage({
            type: 'success',
            message: res.data.message,
        })
    })
}

//关闭tag修改数据
const closeTag = (id,taglist,i) => {
    // console.log(id,taglist,i)
    //删除数组中指定索引的值
    taglist.splice(i,1)
    //封装接口所需数据
    //封装接口所需数据
    let params = {
        'val':taglist.join(",")
    }
    //发送请求
    //发送请求
    api.update_attr_value(id,params,).then(res => {
        ElMessage({
            type: 'success',    
            message: res.data.message,
        })
    })
}
</script>

<style scoped>
    .box-card {
        margin-top: 20px;
    }
    .attr_title {
        margin-right: 20px;
    }
    .alert {
        margin-bottom: 20px;
    }
    .demo-tabs > .el-tabs__content {
        padding: 32px;
        color: #6b778c;
        font-size: 32px;
        font-weight: 600;
    }
    .e-tag {
        margin: 10px;
    }
</style>