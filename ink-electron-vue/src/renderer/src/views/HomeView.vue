<template>
  <div class="home-container">
    <div class="stats-card-container">
      <div class="nav-card">
        <i class="icon-file-text"></i>
        <h3>总作品数</h3>
        <p class="stat-value">{{ totalWorks }}</p>
      </div>
      <div class="nav-card">
        <i class="icon-eye"></i>
        <h3>总访问量</h3>
        <p class="stat-value">{{ totalVisits }}</p>
      </div>
      <div class="nav-card">
        <i class="icon-money"></i>
        <h3>总收入</h3>
        <p class="stat-value">{{ totalIncome }}</p>
      </div>
    </div>

    <h2 class="section-title">功能区域</h2>
    <div class="card-container">
      <div class="nav-card card-color-1" @click="router.push('/ai-creation')">
        <EditOutlined />
        <h3 style="color: #333">AI创作</h3>
      </div>
      <div class="nav-card card-color-2" @click="router.push('/html-creation')">
        <BuildOutlined />
        <h3 style="color: #333">图文生成</h3>
      </div>
      <div class="nav-card card-color-3" @click="router.push('/data-analysis')">
        <BarChartOutlined />
        <h3 style="color: #333">数据分析</h3>
      </div>
      <div class="nav-card card-color-4" @click="router.push('/material')">
        <DatabaseOutlined />
        <h3 style="color: #333">素材库</h3>
      </div>
      <div class="nav-card card-color-5" @click="router.push('/settings')">
        <SettingOutlined />
        <h3 style="color: #333">系统设置</h3>
      </div>
      <div class="nav-card card-color-6" @click="router.push('/help')">
        <QuestionCircleOutlined />
        <h3 style="color: #333">帮助中心</h3>
      </div>
    </div>

    <div class="rankings-container">
      <!-- 全网热点 -->
      <div class="ranking-card">
        <div class="hot-topics-section">
          <h2 class="section-title">全网热点</h2>
          <div class="hot-list">
            <div v-for="(hot, i) in hotTopics" :key="i" class="hot-item">
              <span class="hot-rank">{{ i + 1 }}</span>
              <span class="hot-title">{{ hot.title }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 实时爆文 -->
      <div class="ranking-card">
        <div class="realtime-section">
          <h2 class="section-title">实时爆文</h2>
          <div class="realtime-list">
            <div v-for="(article, i) in realtimeArticles" :key="i" class="realtime-item">
              <span class="realtime-rank">{{ i + 1 }}</span>
              <div class="realtime-content">
                <h3 class="realtime-title">{{ article.title }}</h3>
                <p class="realtime-views">{{ article.views }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 粉丝量排行榜 -->
      <div class="ranking-card">
        <div class="fans-ranking-section">
          <h2 class="section-title">粉丝量排行榜</h2>
          <div class="ranking-list">
            <div v-for="(author, i) in authorRanking" :key="i" class="ranking-item">
              <span class="rank-number">{{ i + 1 }}</span>
              <div class="author-info">
                <div class="author-avatar">{{ author.name.charAt(0) }}</div>
                <div class="author-details">
                  <h3 class="author-name">{{ author.name }}</h3>
                  <p class="author-stats">{{ author.fans }}粉丝 · {{ author.likes }}获赞</p>
                </div>
              </div>
              <!-- 移除奖励金额显示 -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
import {
  EditOutlined,
  BuildOutlined,
  BarChartOutlined,
  DatabaseOutlined,
  SettingOutlined,
  QuestionCircleOutlined
} from '@ant-design/icons-vue'
// 热点话题数据
// 实时爆文数据
const realtimeArticles = [
  { title: '国常会最新部署：释放三大政策信号', views: '235.6万观看' },
  { title: '突发！美联储宣布加息25个基点', views: '189.3万观看' },
  { title: '苹果新品发布会全程回顾', views: '156.7万观看' },
  { title: '高考志愿填报十大误区', views: '128.9万观看' },
  { title: '多地出现极端高温天气', views: '102.4万观看' }
]

// 粉丝量排行榜数据（按粉丝数降序排列）
// 统计数据
const totalWorks = '128 篇'
const totalVisits = '3.2 万'
const totalIncome = '¥15,680'

// 作者排行榜数据（按粉丝数降序排列）
const authorRanking = [
  { name: '数码科技迷', fans: '124.7万', likes: '896.5万' },
  { name: '旅行摄影日记', fans: '98.3万', likes: '654.2万' },
  { name: '美食烹饪大师', fans: '76.5万', likes: '432.1万' },
  { name: '职场成长指南', fans: '62.8万', likes: '321.7万' },
  { name: '健康养生专家', fans: '54.2万', likes: '289.3万' }
]

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
  padding: 1.5rem;
  max-width: 1400px;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
  color: var(--text-primary);
  overflow: hidden;
}

.rankings-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 400fr));
  gap: 1rem;
  margin-top: 1.5rem;
  align-items: stretch;
  flex: 1;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.hot-topics-section,
.realtime-section,
.fans-ranking-section {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.hot-list,
.realtime-list,
.ranking-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 450px;
}

.ranking-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.hot-list,
.realtime-list,
.ranking-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 400px;
}

.ranking-card {
  flex: 1;
  min-width: 0;
}

.left-section,
.right-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

@media (max-width: 768px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }
}

.ink-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  text-align: left;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.stats-card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 300px));
  gap: 0.8rem;
  margin-bottom: 1.5rem;
  width: 100%;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.8rem;
  margin-bottom: 1.5rem;
  width: 100%;
}

.nav-card .stat-value {
  font-size: 20px;
  font-weight: bold;
  margin-top: 5px;
  color: var(--text-primary);
}

.nav-card h3 {
  color: var(--text-primary);
}

.nav-card {
  padding: 1rem 0.8rem;
  font-size: 0.9rem;
  border-radius: 8px;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.nav-card.card-color-1 {
  background-color: #e6f7ff;
}
.nav-card.card-color-2 {
  background-color: #fff7e6;
}
.nav-card.card-color-3 {
  background-color: #f6ffed;
}
.nav-card.card-color-4 {
  background-color: #fff0f0;
}
.nav-card.card-color-5 {
  background-color: #f9f0ff;
}
.nav-card.card-color-6 {
  background-color: #e6fffb;
}

/* 热点话题样式 */
.hot-topics-section {
  margin-top: 0;
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

.hot-rank:nth-child(-n + 3) {
  background-color: #ff4d4f;
}

.hot-rank:nth-child(n + 4):nth-child(-n + 10) {
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

/* 创作攻略样式 */
.strategies-section {
  margin-top: 3rem;
}

.realtime-list {
  background-color: var(--bg-color);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--border-color);
}

.realtime-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-bottom: 1px solid var(--border-color);
}

.realtime-item:last-child {
  border-bottom: none;
}

.realtime-rank {
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
  background-color: #1890ff;
}

.realtime-content {
  flex: 1;
}

.realtime-title {
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.realtime-views {
  font-size: 12px;
  color: var(--text-secondary);
}

.ranking-section {
  margin-top: 3rem;
}

.ranking-list {
  background-color: var(--bg-color);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--border-color);
}

.ranking-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid var(--border-color);
}

.ranking-item:last-child {
  border-bottom: none;
}

.rank-number {
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
  background-color: var(--primary-color);
}

.author-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.author-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--primary-light);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 12px;
}

.author-details {
  line-height: 1.4;
}

.author-name {
  font-size: 14px;
  color: var(--text-primary);
}

.author-stats {
  font-size: 12px;
  color: var(--text-secondary);
}

.author-reward {
  font-size: 14px;
  font-weight: bold;
  color: #ff4d4f;
}

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
