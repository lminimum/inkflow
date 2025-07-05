<template>
  <div class="model-list-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else class="model-grid">
      <div v-for="serviceGroup in models" :key="serviceGroup.service" class="service-section">
        <h2>{{ serviceGroup.service }}</h2>
        <div class="model-grid">
          <div v-for="model in serviceGroup.models" :key="model" class="model-card">
            <h3>{{ model }}</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchModels } from '../api/models'
const models = ref<Array<{ service: string; models: string[] }>>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await fetchModels()
    models.value = Object.entries(response).map(([service, modelNames]) => ({
      service,
      models: modelNames
    }))
  } catch (err) {
    error.value = '获取模型列表失败，请稍后重试'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.model-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading,
.error {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

.error {
  color: #ff4d4f;
}

.model-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.model-card {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px;
  transition: transform 0.2s;
}

.model-card:hover {
  transform: translateY(-4px);
}

.model-card h3 {
  margin: 0 0 10px 0;
  color: var(--text-primary);
  font-size: 18px;
}

.model-card p {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
}
</style>
