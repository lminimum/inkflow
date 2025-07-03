<template>
  <div class="tab-container">
    <div
      v-for="tab in tabs"
      :key="tab.key"
      :class="['tab-item', { active: activeKey === tab.key }]"
      @click="handleTabClick(tab.key)"
    >
      {{ tab.label }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps<{
  modelValue: string
  tabs: Array<{
    key: string
    label: string
    route: string
  }>
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const router = useRouter()
const route = useRoute()
const activeKey = ref(props.modelValue)

// 同步路由变化到Tab
watch(
  () => route.path,
  (newPath) => {
    const matchedTab = props.tabs.find((tab) => tab.route === newPath)
    if (matchedTab) {
      activeKey.value = matchedTab.key
    }
  },
  { immediate: true }
)

// 同步Tab变化到路由和父组件
const handleTabClick = (key: string): void => {
  activeKey.value = key
  emit('update:modelValue', key)
  const matchedTab = props.tabs.find((tab) => tab.key === key)
  if (matchedTab && route.path !== matchedTab.route) {
    // 原代码使用了未导入的 useRouter，需要先导入 useRouter 并使用它来进行路由跳转
    // 这里需要补充导入 useRouter，以下为修正后的代码
    router.push(matchedTab.route)
  }
}

// 同步props变化到本地状态
watch(
  () => props.modelValue,
  (newValue) => {
    activeKey.value = newValue
  }
)
</script>

<style scoped>
.tab-container {
  display: flex;
  margin-top: 30px;
  -webkit-app-region: drag;
}

.tab-item {
  padding: 0 24px 8px 24px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  background-color: var(--card-bg);
  color: var(--text-primary);
  transition: all 0.3s ease;
  font-size: medium;
  -webkit-app-region: no-drag;
}

.tab-item:hover {
  color: var(--primary-color);
}
</style>
