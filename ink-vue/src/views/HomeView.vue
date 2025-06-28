<template>
  <div class="home-container">
    <h1 class="ink-title">墨韵创作中心</h1>
    <div class="card-container">
      <div class="nav-card" @click="router.push('/ai-creation')">
        <i class="icon-brush"></i>
        <h3>AI创作空间</h3>
      </div>
      <div class="nav-card" @click="router.push('/add')">
        <i class="icon-add"></i>
        <h3>内容管理</h3>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped>
.home-container {
  padding: 2rem;
}
.ink-title {
  font-family: 'Ma Shan Zheng', cursive;
  color: var(--ink-black);
  text-align: center;
  margin-bottom: 3rem;
  border-bottom: 2px solid var(--ink-accent);
  padding-bottom: 1rem;
}
</style>