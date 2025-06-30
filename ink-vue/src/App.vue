<template>
  <div class="layout-container">
    <SidebarMenu
      :is-dark="isDark"
      :top-items="topNavItems"
      @item-click="handleNavClick"
      :on-setting-click="showThemeSettings"
    />
    <div class="main-content">
      <router-view />
    </div>
    <ThemeSettings
      :open="themeSettingsOpen"
      @close="handleThemeSettingsClose"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import SidebarMenu from "@/components/SidebarMenu.vue";
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

// 导航项配置
const topNavItems = [
  { to: "/", icon: HomeOutlined },
  { to: "/ai-creation", icon: EditOutlined },
  { to: "/models", icon: DatabaseOutlined },
];

const router = useRouter();
const themeSettingsOpen = ref(false);

const handleNavClick = (item: { to?: string; handler?: () => void }) => {
  if (item.to) {
    router.push(item.to);
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

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
}

.main-content {
  margin-left: 60px;
  padding: 20px;
  flex: 1;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}
</style>
