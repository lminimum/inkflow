import { createRouter, createWebHistory } from 'vue-router'
import ModelList from '../views/ModelList.vue'
import HtmlToImageTool from '../views/HtmlToImageTool.vue'
import MaterialLibrary from '../views/MaterialLibrary.vue'
import CookieManager from '../views/CookieManager.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { title: '主页' }
    },
    {
      path: '/models',
      name: 'models',
      component: ModelList,
      meta: { title: '模型列表' }
    },
    {
      path: '/ai-creation',
      name: 'ai-creation',
      component: () => import('../views/AICreation.vue'),
      meta: { title: 'AI创作' }
    },
    {
      path: '/html-creation',
      name: 'html-creation',
      component: () => import('../views/HTMLCreation.vue'),
      meta: { title: 'HTML生成' }
    },
    {
      path: '/html-to-image',
      name: 'html-to-image',
      component: HtmlToImageTool,
      meta: { title: '图文生成工具' }
    },
    {
      path: '/material-library',
      name: 'material-library',
      component: MaterialLibrary,
      meta: { title: '热点素材库' }
    },
    {
      path: '/cookies',
      name: 'cookies',
      component: CookieManager,
      meta: { title: '账号管理' }
    }
  ]
})

export default router
