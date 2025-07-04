<template>
  <div class="material-container">
    <!-- Left Panel: Hotspot List -->
    <div class="hotspot-list-panel">
      <div v-if="loading" class="loading-placeholder">加载中...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      <div v-else class="hotspot-groups">
        <div v-for="(group, source) in groupedHotspots" :key="source" class="hotspot-group">
          <h2 class="source-title">{{ source }}</h2>
          <ul>
            <li
              v-for="item in group"
              :key="item.title"
              class="hotspot-item"
              :class="{ active: selectedHotspot?.title === item.title }"
            >
              {{ item.title }}
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Right Panel: Analysis Result -->
    <div class="analysis-panel">
      <div v.if="!analysisStarted" class="placeholder">
        <p>请从左侧选择一个热点进行分析</p>
      </div>
      <div v-if="analyzing" class="loading-placeholder">正在分析中，请稍候...</div>
      <div v-else-if="analysisError" class="error-message">
        {{ analysisError }}
      </div>
      <div v-else-if="analysisResult" class="analysis-result">
        <h2 class="result-title">热点分析结果</h2>
        <pre class="result-content">{{ analysisResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useHotspotStore } from '../store/hotspotStore'
import { storeToRefs } from 'pinia'
// import { analyzeHotspots } from '../api/hotspot'
import type { HotspotItem } from '../api/hotspot'

const hotspotStore = useHotspotStore()
const { groupedHotspots, loading, error } = storeToRefs(hotspotStore)

const selectedHotspot = ref<HotspotItem | null>(null)
const analyzing = ref(false)
// const analysisStarted = ref(false)
const analysisResult = ref('')
const analysisError = ref<string | null>(null)

// const analyzeHotspot = async (hotspot: HotspotItem): Promise<void> => {
//   selectedHotspot.value = hotspot
//   analyzing.value = true
//   analysisStarted.value = true
//   analysisResult.value = ''
//   analysisError.value = null

//   try {
//     // API目前分析所有热点，我们可以在此基础上进行扩展
//     // 为了模拟针对性分析，我们仅传递选中的热点标题
//     const response = await analyzeHotspots({
//       // 传递一些上下文，尽管后端当前可能未使用
//     })
//     analysisResult.value = response.report
//   } catch (err) {
//     console.error('Failed to analyze hotspot:', err)
//     analysisError.value = '分析失败，请稍后再试。'
//   } finally {
//     analyzing.value = false
//   }
// }

onMounted(() => {
  hotspotStore.fetchHotspots()
})
</script>

<style scoped>
.material-container {
  display: flex;
  height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.hotspot-list-panel {
  width: 300px;
  border-right: 1px solid var(--border-color);
  padding: 1.5rem;
  overflow-y: auto;
  background-color: var(--card-bg);
}

.panel-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.source-title {
  font-size: 1.1rem;
  font-weight: 500;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.hotspot-item {
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 0.9rem;
}

.hotspot-item:hover {
  background-color: var(--hover-color);
}

.hotspot-item.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
  font-weight: 600;
}

.analysis-panel {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.placeholder,
.loading-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: var(--text-secondary);
}

.error-message {
  color: var(--rank-color);
  text-align: center;
  padding: 1rem;
}

.analysis-result {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.result-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

.result-content {
  background-color: var(--card-bg);
  padding: 1.5rem;
  border-radius: 8px;
  white-space: pre-wrap; /* Allows text to wrap */
  word-wrap: break-word;
  line-height: 1.6;
}
</style>
