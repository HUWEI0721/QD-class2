import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

import App from './App.vue'
import router from './router'

// 简单的调试信息
console.log('🚀 应用启动')
console.log('环境变量 VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)
console.log('所有环境变量:', import.meta.env)

const app = createApp(App)

// 注册所有图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
})

// 直接挂载应用，认证状态会在路由守卫中初始化
app.mount('#app')