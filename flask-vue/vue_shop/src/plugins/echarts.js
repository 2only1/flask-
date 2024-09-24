
// //单表引用方式
// import * as echarts from 'echarts'
// export default {
//     // echarts 作为全局变量使用
//     install: app => {
//         app.config.globalProperties.$echarts = (element) => {
//             // element设置在哪个元素上渲染图表
//             let myChart =
//                 echarts.init(document.getElementById(element))
//             const option = {
//                 //加载图表的样式与数据
//                 xAxis: {
//                     type: 'category',
//                     data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
//                 },
//                 yAxis: {
//                     type: 'value'
//                 },
//                 series: [
//                     {
//                         data: [150, 230, 224, 218, 135, 147, 260],
//                         type: 'line'
//                     }
//                 ]
//             }
//             // 渲染图表
//             myChart.setOption(option)
//         }
//     }
// }

//多表引用方式
import * as echarts from 'echarts';
export default {
    // echarts 作为全局变量使用
    install: app => {
        app.config.globalProperties.$echarts = (element,option) => {
            // element设置在哪个元素上渲染图表
            let myChart =
                echarts.init(document.getElementById(element))
            
            // 渲染图表
            myChart.setOption(option)
        }
    }
}
