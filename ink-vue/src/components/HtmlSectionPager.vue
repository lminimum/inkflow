<template>
  <div class="pager-container" v-if="sections.length">
    <button class="pager-btn" :disabled="currentIndex === 0" @click="prev">&#8592;</button>
    <div class="pager-content">
      <div class="html-section-item" v-html="sections[currentIndex]"></div>
      <div class="pager-indicator">{{ currentIndex + 1 }} / {{ sections.length }}</div>
    </div>
    <button class="pager-btn" :disabled="currentIndex === sections.length - 1" @click="next">&#8594;</button>
  </div>
  <p v-else class="empty-hint">生成的HTML将显示在这里...</p>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
const props = defineProps<{ sections: string[] }>();
const currentIndex = ref(0);

watch(
  () => props.sections.length,
  (len) => {
    if (currentIndex.value >= len) currentIndex.value = len > 0 ? len - 1 : 0;
  }
);

function prev() {
  if (currentIndex.value > 0) currentIndex.value--;
}
function next() {
  if (currentIndex.value < props.sections.length - 1) currentIndex.value++;
}
</script>

<style scoped>
.pager-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  width: 100%;
  min-height: 300px;
}
.pager-btn {
  font-size: 2rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--primary-color, #333);
  padding: 0 1rem;
}
.pager-btn:disabled {
  color: #ccc;
  cursor: not-allowed;
}
.pager-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.html-section-item {
  min-width: 400px;
  max-width: 700px;
  min-height: 200px;
  border: 1px solid var(--border-color, #eee);
  border-radius: 8px;
  background: #fff;
  color: #222;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.04);
  padding: 1.5rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}
.pager-indicator {
  text-align: center;
  color: #888;
  font-size: 1rem;
}
.empty-hint {
  color: var(--text-secondary);
  text-align: center;
  margin-top: 2rem;
  font-style: italic;
}
</style>
