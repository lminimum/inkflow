<template>
  <div class="layout-container">
    <SidebarMenu
      :is-dark="isDark"
      :top-items="topNavItems"
      @item-click="handleNavClick"
      :on-setting-click="showThemeSettings"
    />
    <div class="main-container">
      <!-- 全局Tab组件 -->
      <GlobalTabs
        :tabs="tabs"
        :modelValue="activeTab"
        @update:modelValue="switchTab"
      />
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
    <ThemeSettings
      :open="themeSettingsOpen"
      @close="handleThemeSettingsClose"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import SidebarMenu from "@/components/SidebarMenu.vue";
import GlobalTabs from "@/components/GlobalTabs.vue";
import {
  HomeOutlined,
  EditOutlined,
  DatabaseOutlined,
  CodeOutlined,
} from "@ant-design/icons-vue";
import ThemeSettings from "@/components/ThemeSettings.vue";
const isDark = ref(false);
const showThemeSettings = () => {
  themeSettingsOpen.value = true;
};

// Tab配置
const tabs = [
  { label: "主页", key: "home", route: "/" },
  { label: "模型", key: "models", route: "/models" },
];

// Tab状态管理
const activeTab = ref("creation");
const switchTab = (tab: string) => {
  activeTab.value = tab;
  router.push("/ai-creation");
};

// 定义不同tab对应的导航项
const creationNavItems = [
  { to: "/", icon: HomeOutlined },
  { to: "/ai-creation", icon: EditOutlined },
  { to: "/html-creation", icon: CodeOutlined },
  { to: "/models", icon: DatabaseOutlined },
];

const rewriteNavItems = [
  { to: "/", icon: HomeOutlined },
  { to: "/ai-rewrite", icon: EditOutlined },
  { to: "/models", icon: DatabaseOutlined },
];

// 动态导航项
const topNavItems = computed(() => {
  return activeTab.value === "creation" ? creationNavItems : rewriteNavItems;
});

const router = useRouter();
const route = useRoute();
const themeSettingsOpen = ref(false);

const handleNavClick = (item: { to?: string; handler?: () => void }) => {
  if (item.to) {
    router.push(item.to);
    // 根据路由更新activeTab
    if (item.to === "/ai-creation") {
      activeTab.value = "creation";
    } else if (item.to === "/ai-rewrite") {
      activeTab.value = "rewrite";
    }
  }
  item.handler?.();
};

const handleThemeSettingsClose = () => {
  themeSettingsOpen.value = false;
};
</script>

<style scoped>
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
  box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.1), 0 0 0 rgba(0, 0, 0, 0);
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
