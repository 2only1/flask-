<template>
    <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue" class="input-tag" size="small"
        @blur="handleInputConfirm" />
    <el-button v-else class="button-new-tag ml-1" size="small" @click="showInput">+ 添加值</el-button>
</template>

<script setup>
import { ref, nextTick } from 'vue'
const inputValue = ref('')
const inputVisible = ref(false)
const InputRef = ref(null)


const emit = defineEmits(['addTagEvent'])  //定义事件]
const props= defineProps({
    row: {
        type: Object, //传递的数据类型
        default: () => Object  //默认值
    }
})//定义接收父级组件的值

//点击后显示输入框
const showInput = () => {
    inputVisible.value = true
    nextTick(() => {
        InputRef.value.input.focus() //获取焦点
    })
}
//输入框失去焦点后
const handleInputConfirm = () => {
    //触发事件
    emit('addTagEvent', {'inputvalue':inputValue.value,'row':props.row})
    inputVisible.value = false
    inputValue.value = ''
}

</script>

<style scoped>
.input-tag {
    width: 100px;
    margin-right: 10px;
}
</style>