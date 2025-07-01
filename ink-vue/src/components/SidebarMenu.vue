<template>
  <nav class="sidebar">
    <!-- 网站图标 -->
    <div class="logo-container">
      <img src="/icons8-墨-32.png" alt="网站图标" class="logo" />
    </div>

    <!-- 导航图标区域 -->
    <template v-for="item in topItems" :key="item.to || JSON.stringify(item)">
      <div
        class="menu-item"
        :class="{ active: currentRoute === item.to }"
        @click="handleClick(item)"
        title="{{ item.to === '/' ? '首页' : 'AI创作' }}"
      >
        <component :is="item.icon" :style="{ fontSize: '24px' }" />
      </div>
    </template>

    <!-- 底部功能按钮 -->
    <div class="bottom-section">
      <div class="menu-item" @click="handleSettingClick">
        <component :is="SettingOutlined" :style="{ fontSize: '24px' }" />
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { SettingOutlined } from "@ant-design/icons-vue";

export interface NavigationItem {
  to?: string;
  icon?: any;
  handler?: () => void;
}

const props = defineProps<{
  isDark: boolean;
  topItems?: NavigationItem[];
  addButton?: NavigationItem;
  onSettingClick?: () => void;
}>();

// Define emits properly
const emit = defineEmits(["itemClick"]);

const route = useRoute();
const currentRoute = computed(() => route.path);

const handleClick = (item: NavigationItem) => {
  if (item.to) {
    emit("itemClick", item);
  }
  item.handler?.();
};

const handleSettingClick = () => {
  props.onSettingClick?.();
};
</script>

<style scoped>
.logo-container {
  padding: 10px 0;
}

.logo {
  width: 32px;
  height: 32px;
}

.sidebar {
  width: 60px;
  height: 100vh;
  background: var(--bg-color);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.menu-item {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  color: var(--text-primary);
}

.menu-item.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
}

.menu-item:hover:not(.active) {
  background-color: var(--hover-color);
}

.bottom-section {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.add-btn {
  background-color: var(--primary-color);
  color: white;
}

.add-btn:hover {
  background-color: var(--primary-hover);
}
</style>
