//vue3写法
import * as components from "@element-plus/icons-vue";
export default {
    install: (app) => {
        for (const key in components) {
            const componentConfig = components[key];
            app.component(componentConfig.name, componentConfig);
        }
    },
};

// main.ts

// 如果您正在使用CDN引入，请删除下面一行。
// import * as ElementPlusIconsVue from '@element-plus/icons-vue';


// const app = createApp(app)
// for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
// app.component(key, component)
// }

// export default app;
