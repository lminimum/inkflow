<template>
  <div class="model-list-container">
    <h1>可用AI模型列表</h1>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div class="model-grid" v-else>
      <div class="model-card" v-for="model in models" :key="model.id">
        <h3>{{ model.id }}</h3>
        <p>拥有者: {{ model.owned_by }}</p>
        <p>创建时间: {{ new Date(model.created * 1000).toLocaleString() }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchModels } from "../api/models";
import type { Model } from "../types";

const models = ref<Model[]>([]);
const loading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    const response = await fetchModels();
    models.value = response.data;
  } catch (err) {
    error.value = "获取模型列表失败，请稍后重试";
    console.error(err);
  } finally {
    loading.value = false;
  }
});
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
  background: #fff;
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
  color: #1890ff;
  font-size: 18px;
}

.model-card p {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
}
</style>
