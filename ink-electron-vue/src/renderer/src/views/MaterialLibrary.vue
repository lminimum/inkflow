<template>
  <div class="material-container">
    <!-- 左侧热点列表面板 -->
    <div class="hotspot-list-panel">
      <div class="panel-header">
        <h2 class="panel-title">热点素材库</h2>
        <button class="refresh-btn" @click="refreshHotspots" :disabled="loading">
          <ReloadOutlined :spin="loading" />
        </button>
      </div>

      <div v-if="loading" class="loading-container">
        <LoadingOutlined class="loading-icon" spin />
        <span>正在加载热点数据...</span>
      </div>

      <div v-else-if="error" class="error-container">
        <WarningOutlined class="error-icon" />
        <span>{{ error }}</span>
        <button class="retry-btn" @click="refreshHotspots">重试</button>
      </div>

      <div v-else class="hotspot-groups">
        <div v-for="(group, source) in groupedHotspots" :key="source" class="hotspot-group">
          <div class="source-header">
            <h3 class="source-title">{{ getSourceDisplayName(source) }}</h3>
            <span class="item-count">{{ group.length }}条</span>
          </div>

          <ul class="hotspot-list">
            <li
              v-for="item in group"
              :key="item.title"
              class="hotspot-item"
              :class="{ active: selectedHotspot?.title === item.title }"
              @click="selectHotspot(item)"
            >
              <div class="hotspot-content">
                <div class="hotspot-title">{{ item.title }}</div>
                <div class="hotspot-meta" v-if="item.hot_score">
                  <FireOutlined class="hot-icon" />
                  <span class="hot-score">{{ formatHotScore(item.hot_score) }}</span>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 右侧内容展示面板 -->
    <div class="content-panel">
      <div v-if="!selectedHotspot" class="empty-state">
        <CompassOutlined class="empty-icon" />
        <p class="empty-text">请从左侧选择一个热点进行浏览</p>
      </div>

      <div v-else class="iframe-container">
        <div class="iframe-header">
          <h2 class="iframe-title">{{ selectedHotspot.title }}</h2>
          <div class="iframe-actions">
            <button class="action-btn" @click="openInNewWindow" title="在新窗口打开">
              <ExportOutlined />
            </button>
            <button class="action-btn" @click="refreshIframe" title="刷新">
              <ReloadOutlined />
            </button>
          </div>
        </div>

        <div class="iframe-wrapper">
          <div v-if="isIframeLoading" class="iframe-loading">
            <LoadingOutlined class="loading-icon" spin />
            <span>正在加载页面...</span>
          </div>

          <div v-if="iframeError" class="iframe-error">
            <WarningOutlined class="error-icon" />
            <p>页面加载失败</p>
            <button class="retry-btn" @click="refreshIframe">重试</button>
          </div>

          <iframe
            v-if="selectedHotspot.url"
            :src="selectedHotspot.url"
            frameborder="0"
            ref="iframeRef"
            sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            class="content-iframe"
            @load="handleIframeLoad"
            @error="handleIframeError"
            :style="{
              transform: `scale(${iframeScale})`,
              transformOrigin: 'top left',
              width: `${100 / iframeScale}%`,
              height: `${100 / iframeScale}%`
            }"
          ></iframe>
          <div v-else class="no-url-message">
            <WarningOutlined class="warning-icon" />
            <p>该热点没有可访问的URL</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Chrome第三方Cookie警告提示 -->
    <div class="cookie-notice" v-if="selectedHotspot">
      <p>部分网站可能需要启用第三方Cookie才能正常显示</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useHotspotStore } from '../store/hotspotStore'
import { storeToRefs } from 'pinia'
import type { HotspotItem } from '../api/hotspot'
import {
  ReloadOutlined,
  LoadingOutlined,
  WarningOutlined,
  FireOutlined,
  CompassOutlined,
  ExportOutlined
} from '@ant-design/icons-vue'

const hotspotStore = useHotspotStore()
const { groupedHotspots, loading, error } = storeToRefs(hotspotStore)

const selectedHotspot = ref<HotspotItem | null>(null)
const iframeRef = ref<HTMLIFrameElement | null>(null)
const isIframeLoading = ref(false)
const iframeError = ref(false)
const iframeScale = ref(1)

// 添加被动事件监听器支持
const addPassiveSupport = (): void => {
  // 创建一个样式元素
  const style = document.createElement('style')
  style.textContent = `
    /* 添加CSS来防止触摸事件引起的滚动问题 */
    .content-iframe {
      touch-action: manipulation;
    }
    
    /* 确保iframe容器可以正常滚动 */
    .iframe-wrapper {
      touch-action: pan-y;
    }
    
    /* 确保热点列表可以正常滚动 */
    .hotspot-groups {
      touch-action: pan-y;
    }
  `
  document.head.appendChild(style)

  // 添加被动事件监听器
  document.addEventListener('touchstart', () => {}, { passive: true })
  document.addEventListener('touchmove', () => {}, { passive: true })
  document.addEventListener('wheel', () => {}, { passive: true })
}

// 调整iframe缩放比例
const adjustIframeScale = (): void => {
  if (!iframeRef.value) return

  // 获取iframe容器宽度
  const containerWidth = iframeRef.value.parentElement?.clientWidth || 800

  // 设置一个标准宽度，大多数网站设计为960px或1024px宽
  const standardWidth = 1024

  // 计算缩放比例，但不超过1（不放大，只缩小）
  const scale = Math.min(containerWidth / standardWidth, 1)

  // 更新缩放比例
  iframeScale.value = scale
}

// 刷新热点数据
const refreshHotspots = (): void => {
  hotspotStore.fetchHotspots(true) // 传入true表示强制刷新
}

// 选择热点
const selectHotspot = (hotspot: HotspotItem): void => {
  selectedHotspot.value = hotspot
  isIframeLoading.value = true
  iframeError.value = false
}

// 在新窗口打开链接
const openInNewWindow = (): void => {
  if (selectedHotspot.value?.url) {
    window.open(selectedHotspot.value.url, '_blank')
  }
}

// 刷新iframe
const refreshIframe = (): void => {
  if (iframeRef.value && selectedHotspot.value?.url) {
    isIframeLoading.value = true
    iframeError.value = false
    iframeRef.value.src = selectedHotspot.value.url
  }
}

// iframe加载完成
const handleIframeLoad = (): void => {
  isIframeLoading.value = false

  // 调整iframe缩放
  adjustIframeScale()
}

// iframe加载错误
const handleIframeError = (): void => {
  isIframeLoading.value = false
  iframeError.value = true
}

// 格式化热度分数
const formatHotScore = (score: number | string | null): string => {
  if (score === null) return '未知'

  const num = Number(score)
  if (isNaN(num)) return String(score)

  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }

  return String(num)
}

// 获取来源的显示名称
const getSourceDisplayName = (source: string): string => {
  const sourceMap: Record<string, string> = {
    baidu: '百度热搜',
    weibo: '微博热搜',
    zhihu: '知乎热榜',
    toutiao: '今日头条',
    douyin: '抖音热点'
  }

  return sourceMap[source] || source
}

onMounted(() => {
  hotspotStore.fetchHotspots()
  addPassiveSupport()

  // 监听窗口大小变化，调整iframe缩放
  window.addEventListener('resize', adjustIframeScale)
})

// 组件卸载时移除事件监听器
onUnmounted(() => {
  window.removeEventListener('resize', adjustIframeScale)
})
</script>

<style scoped>
.material-container {
  display: flex;
  height: calc(100vh - 108px);
  background-color: var(--bg-color);
  color: var(--text-primary);
  overflow: hidden;
  position: relative;
}

/* 左侧热点列表面板样式 */
.hotspot-list-panel {
  width: 320px;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.panel-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.refresh-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 1.1rem;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.refresh-btn:hover {
  background-color: var(--hover-color);
  color: var(--primary-color);
}

.hotspot-groups {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.hotspot-group {
  margin-bottom: 1.5rem;
}

.source-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
}

.source-title {
  font-size: 1rem;
  font-weight: 500;
  margin: 0;
  color: var(--text-secondary);
}

.item-count {
  font-size: 0.8rem;
  color: var(--text-secondary);
  background-color: var(--hover-color);
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
}

.hotspot-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.hotspot-item {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 0.25rem;
}

.hotspot-item:hover {
  background-color: var(--hover-color);
}

.hotspot-item.active {
  background-color: var(--primary-light);
  border-left: 3px solid var(--primary-color);
}

.hotspot-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.hotspot-title {
  font-size: 0.9rem;
  line-height: 1.4;
  word-break: break-all;
}

.hotspot-meta {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.hot-icon {
  color: #ff4d4f;
  font-size: 0.8rem;
}

.hot-score {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

/* 右侧内容展示面板样式 */
.content-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
}

.iframe-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.iframe-title {
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 80%;
}

.iframe-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 1rem;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.action-btn:hover {
  background-color: var(--hover-color);
  color: var(--primary-color);
}

.iframe-wrapper {
  flex: 1;
  position: relative;
  height: calc(100vh - 160px); /* 减去头部和导航的高度 */
  overflow: hidden;
}

.content-iframe {
  width: 100%;
  height: 100%;
  border: none;
  background-color: white;
  display: block;
  /* 添加平滑过渡效果 */
  transition: transform 0.2s ease;
}

/* 加载和错误状态样式 */
.loading-container,
.error-container,
.empty-state,
.no-url-message {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 2rem;
  text-align: center;
  color: var(--text-secondary);
  gap: 1rem;
}

.loading-icon,
.error-icon,
.empty-icon,
.warning-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.loading-icon {
  color: var(--primary-color);
}

.error-icon,
.warning-icon {
  color: var(--rank-color);
}

.empty-icon {
  color: var(--text-secondary);
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-btn:hover {
  background-color: var(--primary-hover);
}

.iframe-loading,
.iframe-error {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 10;
}

.iframe-loading {
  color: var(--primary-color);
}

.iframe-error {
  color: var(--rank-color);
}

.iframe-loading .loading-icon,
.iframe-error .error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Chrome第三方Cookie警告提示 */
.cookie-notice {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px;
  text-align: center;
  font-size: 12px;
  z-index: 100;
}

.cookie-notice p {
  margin: 0;
}
</style>
