<script setup lang="ts">
import { ref } from 'vue'
import SidebarMenu from '@/components/SidebarMenu.vue'
import { HomeOutlined, EditOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'

// 导航项配置 - 移除label属性
const topNavItems = [
  { to: '/', icon: HomeOutlined },
  { to: '/ai-creation', icon: EditOutlined },
  { to: '/add', icon: PlusOutlined },
]

const router = useRouter()
const isDark = ref(false)

const handleNavClick = (item: { to?: string; handler?: () => void }) => {
  if (item.to) {
    router.push(item.to)
  }
  item.handler?.()
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
}
</script>

<template>
  <div class="layout-container">
    <SidebarMenu 
      :is-dark="isDark"
      :top-items="topNavItems"
      :show-theme-switch="true"
      @toggle-theme="toggleTheme"
      @item-click="handleNavClick"
    />
    <div class="main-content">
      <router-view/>
    </div>
  </div>
</template>

<style scoped>
.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  min-height: 100vh;
}
</style>
