import { createRouter, createWebHistory } from 'vue-router'
import ModelList from '../views/ModelList.vue'

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@renderer/views/HomeView.vue'),
      meta: { title: '主页' }
    },
    {
      path: '/ai-creation',
      component: () => import('@renderer/views/AICreation.vue'),
      meta: { title: 'AI创作' }
    },
    {
      path: '/html-creation',
      component: () => import('@renderer/views/HTMLCreation.vue'),
      meta: { title: '图文生成' }
    },
    {
      path: '/add',
      component: () => import('@renderer/views/AddView.vue'),
      meta: { title: '添加' }
    },
    {
      path: '/models',
      name: 'ModelList',
      component: ModelList,
      meta: { title: '模型列表' }
    },
    {
      path: '/html-to-image',
      name: 'HtmlToImageTool',
      component: () => import('@renderer/views/HtmlToImageTool.vue'),
      meta: { title: 'HTML转图片工具' }
    }
  ]
})
