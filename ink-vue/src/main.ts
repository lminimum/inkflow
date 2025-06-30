import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import router from './router'
import App from './App.vue'
import * as AntdIcons from '@ant-design/icons-vue'
import Antd from 'ant-design-vue'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia).use(router).use(Antd)

// 全局注册Ant Design图标
Object.keys(AntdIcons).forEach(key => {
  app.component(key, AntdIcons[key as keyof typeof AntdIcons])
})
app.mount('#app')
