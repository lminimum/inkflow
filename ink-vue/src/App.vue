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
        :active-tab="activeTab"
        @tab-change="switchTab"
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
  SettingOutlined,
  HomeOutlined,
  EditOutlined,
  DatabaseOutlined,
} from "@ant-design/icons-vue";
import ThemeSettings from "@/components/ThemeSettings.vue";
const isDark = ref(false);
const showThemeSettings = () => {
  themeSettingsOpen.value = true;
};

// Tab配置
const tabs = [
  { label: "主页", value: "home" },
  { label: "模型", value: "models" },
];

// Tab状态管理
const activeTab = ref("creation");
const switchTab = (tab: string) => {
  activeTab.value = tab;
  // 根据tab切换更新路由
  if (tab === "creation") {
    router.push("/ai-creation");
  } else if (tab === "rewrite") {
    router.push("/ai-rewrite");
  }
};

// 定义不同tab对应的导航项
const creationNavItems = [
  { to: "/", icon: HomeOutlined },
  { to: "/ai-creation", icon: EditOutlined },
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
  border: 1px solid var(--border-color);
  border-radius: 10px;
  flex: 1;
  overflow-y: auto;
}

.header {
  display: flex;
  align-items: center;
  position: fixed;
  width: 100%;
  padding: 0 24px;
  height: 60px;
  background-color: var(--bg-color);
  border-bottom: 1px solid var(--border-color);
}
.content-container {
  margin-top: 2.5rem;
}
</style>
