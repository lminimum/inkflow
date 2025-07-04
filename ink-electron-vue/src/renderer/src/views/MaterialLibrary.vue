<template>
  <div class="p-4 h-full overflow-y-auto">
    <h1 class="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-200">热点素材库</h1>
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-gray-500">加载中...</div>
    </div>
    <div v-else-if="error" class="text-center text-red-500 p-4 bg-red-100 rounded-md">
      {{ error }}
    </div>
    <div v-else class="space-y-6">
      <div
        v-for="(group, source) in groupedHotspots"
        :key="source"
        class="bg-white dark:bg-gray-800 shadow-md rounded-lg p-4"
      >
        <h2 class="text-xl font-semibold mb-3 text-gray-700 dark:text-gray-300">{{ source }}</h2>
        <ul class="space-y-2">
          <li
            v-for="(item, index) in group"
            :key="index"
            class="border-b border-gray-200 dark:border-gray-700 last:border-b-0 py-2"
          >
            <a
              :href="item.url"
              target="_blank"
              rel="noopener noreferrer"
              class="text-blue-600 dark:text-blue-400 hover:underline"
            >
              {{ item.title }}
            </a>
            <span v-if="item.hot_score" class="ml-3 text-sm text-gray-500 dark:text-gray-400"
              >热度: {{ item.hot_score }}</span
            >
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useHotspotStore } from '../store/hotspotStore'
import { storeToRefs } from 'pinia'

const hotspotStore = useHotspotStore()
const { groupedHotspots, loading, error } = storeToRefs(hotspotStore)

onMounted(() => {
  hotspotStore.fetchHotspots()
})
</script>

<style scoped>
/* You can add specific styles here if needed */
</style>
