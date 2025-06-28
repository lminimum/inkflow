<template>
  <nav class="sidebar">
    <!-- 导航图标区域 -->
    <template v-for="item in topItems" :key="item.to || JSON.stringify(item)">
      <div 
        class="menu-item" 
        :class="{ 'active': currentRoute === item.to }"
        @click="handleClick(item)"
        title="{{ item.to === '/' ? '首页' : 'AI创作' }}"
      >
        <component :is="item.icon" :style="{fontSize: '24px'}"/>
      </div>
    </template>

    <!-- 底部功能按钮 -->
    <div class="bottom-section">
      <div v-if="showThemeSwitch" class="menu-item" @click="$emit('toggle-theme')">
        <component :is="isDark ? BulbOutlined : BulbFilled" :style="{fontSize: '24px'}"/>
      </div>
      <div 
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { BulbFilled, BulbOutlined } from '@ant-design/icons-vue';

export interface NavigationItem {
  to?: string;
  icon?: any;
  handler?: () => void;
}

defineProps<{
  isDark: boolean;
  topItems?: NavigationItem[];
  addButton?: NavigationItem;
  showThemeSwitch?: boolean;
}>();

// Define emits properly
const emit = defineEmits(['itemClick', 'toggle-theme']);

const route = useRoute();
const currentRoute = computed(() => route.path);

const handleClick = (item: NavigationItem) => {
  if (item.to) {
    emit('itemClick', item);
  }
  item.handler?.();
};
</script>

<style scoped>
.sidebar {
  width: 60px;
  height: 100vh;
  background: var(--bg-color);
  padding: 20px 0;
  border-right: 1px solid var(--border-color);
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