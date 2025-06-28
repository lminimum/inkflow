import { createRouter, createWebHistory } from 'vue-router';


export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { title: '墨韵主页' }
    },
    { 
      path: '/ai-creation',
      component: () => import('@/views/AICreation.vue'),
      meta: { title: 'AI创作' }
    },
    {
      path: '/add',
      component: () => import('@/views/AddView.vue'),
      meta: { title: '添加' }
    }
  ]
});
