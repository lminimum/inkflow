<template>
  <div style="background-color: var(--card-bg)">
    <div v-if="isElectron" class="custom-titlebar">
      <div class="window-title"></div>
      <div class="window-controls-fixed">
        <MinusOutlined class="window-btn" @click="minimize" />
        <BorderOutlined class="window-btn" style="font-size: 14px" @click="maximize" />
        <CloseOutlined class="window-btn" @click="close" />
      </div>
    </div>
    <div class="layout-container">
      <SidebarMenu
        :is-dark="isDark"
        :top-items="topNavItems"
        :on-setting-click="showThemeSettings"
        @item-click="handleNavClick"
      />
      <div class="main-container">
        <!-- 全局Tab组件 -->
        <GlobalTabs :tabs="tabs" :model-value="activeTab" @update:model-value="switchTab" />
        <div class="main-content">
          <div class="header">
            <span style="font-size: larger">
              {{ route.meta.title }}
            </span>
          </div>
          <div class="content-container">
            <router-view />
          </div>
        </div>
      </div>
      <ThemeSettings :open="themeSettingsOpen" @close="handleThemeSettingsClose" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import SidebarMenu from '@renderer/components/SidebarMenu.vue'
import GlobalTabs from '@renderer/components/GlobalTabs.vue'
import {
  HomeOutlined,
  EditOutlined,
  DatabaseOutlined,
  BuildOutlined,
  MinusOutlined,
  FileImageOutlined,
  CloseOutlined,
  BookOutlined
} from '@ant-design/icons-vue'
import ThemeSettings from '@renderer/components/ThemeSettings.vue'

declare global {
  interface Window {
    electronAPI?: {
      minimize: () => void
      maximize: () => void
      close: () => void
    }
  }
}

const isDark = ref(false)
const showThemeSettings = (): void => {
  themeSettingsOpen.value = true
}

// 自定义窗口控制
const minimize = (): void => window.electronAPI?.minimize()
const maximize = (): void => window.electronAPI?.maximize()
const close = (): void => window.electronAPI?.close()

// Tab配置
const tabs = [
  { label: '主页', key: 'home', route: '/' },
  { label: '工具', key: 'tools', route: '/html-to-image' },
  { label: '设置', key: 'settings', route: '/models' }
]

// Tab状态管理
const activeTab = ref('home')
const switchTab = (tab: string): void => {
  activeTab.value = tab
  if (tab === 'home') {
    router.push('/')
  } else if (tab === 'tools') {
    router.push('/html-to-image')
  } else if (tab === 'settings') {
    router.push('/models')
  }
}

// 定义不同tab对应的导航项
const homeNavItems = [
  { to: '/', icon: HomeOutlined },
  { to: '/ai-creation', icon: EditOutlined },
  { to: '/html-creation', icon: BuildOutlined }
]

const toolsNavItems = [
  { to: '/html-to-image', icon: FileImageOutlined },
  { to: '/material-library', icon: BookOutlined }
]

const settingsNavItems = [{ to: '/models', icon: DatabaseOutlined }]

// 动态导航项
const topNavItems = computed(() => {
  if (activeTab.value === 'home') return homeNavItems
  if (activeTab.value === 'tools') return toolsNavItems
  return settingsNavItems
})

const router = useRouter()
const route = useRoute()
const themeSettingsOpen = ref(false)

const handleNavClick = (item: { to?: string; handler?: () => void }): void => {
  if (item.to) {
    router.push(item.to)
    // 根据路由更新activeTab
    if (item.to === '/' || item.to === '/ai-creation' || item.to === '/html-creation') {
      activeTab.value = 'home'
    } else if (item.to === '/html-to-image' || item.to === '/material-library') {
      activeTab.value = 'tools'
    } else if (item.to === '/models') {
      activeTab.value = 'settings'
    }
  }
  item.handler?.()
}

const handleThemeSettingsClose = (): void => {
  themeSettingsOpen.value = false
}

const isElectron = typeof window !== 'undefined' && !!window.electronAPI
</script>

<style scoped>
.custom-titlebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  -webkit-app-region: drag;
  z-index: 10000;
  user-select: none;
}
/* .window-title {
  font-size: 16px;
  padding-left: 16px;
  font-weight: bold;
} */
.window-controls-fixed {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 100%;
  margin-right: 12px;
  -webkit-app-region: no-drag;
}
.window-btn {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-color);
  font-size: 18px;
  border-radius: 4px;
  cursor: pointer;
  transition:
    background 0.2s,
    color 0.2s;
}
.window-btn:hover {
  background: var(--primary-color);
  color: var(--text-color);
}
.layout-container {
  display: flex;
  height: 100vh;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 60px;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
}

.main-content {
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  flex: 1;
  overflow-y: auto;
  box-shadow:
    3px 3px 8px rgba(0, 0, 0, 0.1),
    0 0 0 rgba(0, 0, 0, 0);
}

.header {
  display: flex;
  align-items: center;
  position: fixed;
  width: calc(100% - 64px);
  padding: 0 24px;
  height: 60px;
  background-color: var(--bg-color);
  border-radius: 10px 10px 0 0;
  border-bottom: 1.5px solid var(--border-color);
  z-index: 10;
}

.content-container {
  margin-top: 2.5rem;
}
</style>
