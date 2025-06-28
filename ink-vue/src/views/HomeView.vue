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

    <!-- 全网热点区域 -->
    <div class="hot-topics-section">
      <h2 class="section-title">全网热点</h2>
      <div class="hot-list">
        <div class="hot-item" v-for="(hot, i) in hotTopics" :key="i">
          <span class="hot-rank">{{ i+1 }}</span>
          <span class="hot-title">{{ hot.title }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

// 热点话题数据
const hotTopics = [
  { title: '直击两会民生热点' },
  { title: '女子校门口被撞身亡' },
  { title: '俄国防部称将增加西部军区兵力' },
  { title: '哈尔滨工程大学超话被封' },
  { title: '特朗普再被起诉' },
  { title: '微信支付重大更新' },
  { title: '油价调价窗口今日开启' },
  { title: '科学家发现新型超导材料' }
]
</script>

<style scoped>
.home-container {
  padding: 2rem;
}

.ink-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

/* 热点话题样式 */
.hot-topics-section {
  margin-top: 3rem;
}

.section-title {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 1rem;
  padding-left: 0.5rem;
  border-left: 3px solid var(--primary-color);
}

.hot-list {
  background-color: var(--bg-color);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.hot-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-bottom: 1px solid var(--border-color);
  transition: background-color 0.2s;
}

.hot-item:last-child {
  border-bottom: none;
}

.hot-item:hover {
  background-color: var(--hover-color);
}

.hot-rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.hot-rank:nth-child(-n+3) {
  background-color: #ff4d4f;
}

.hot-rank:nth-child(n+4):nth-child(-n+10) {
  background-color: #fa8c16;
}

.hot-title {
  flex: 1;
  font-size: 14px;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

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