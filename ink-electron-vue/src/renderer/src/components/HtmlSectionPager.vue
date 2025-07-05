<template>
  <div v-if="props.sections && props.sections.length" ref="pagerContainer" class="pager-container">
    <button class="pager-btn" :disabled="currentIndex === 0" @click="prev">&#8592;</button>
    <div class="pager-content">
      <div ref="containerRef" class="iframe-container">
        <div ref="scalerRef" class="iframe-scaler">
          <iframe
            ref="iframeRef"
            :srcdoc="currentSection"
            class="html-iframe"
            frameborder="0"
            scrolling="no"
          ></iframe>
        </div>
      </div>
      <div class="pager-indicator">
        {{ currentIndex + 1 }} / {{ props.sections ? props.sections.length : 0 }}
      </div>
    </div>
    <button
      class="pager-btn"
      :disabled="!props.sections || currentIndex === props.sections.length - 1"
      @click="next"
    >
      &#8594;
    </button>
  </div>
  <p v-else class="empty-hint">生成的HTML将显示在这里...</p>
</template>

<script setup lang="ts">
import { ref, watch, watchEffect, onMounted, nextTick } from 'vue'

interface HtmlSectionItem {
  html: string
  file_path?: string
}

const pagerContainer = ref<HTMLElement | null>(null)
// import testHtml from "../../../ink-backend/tests/test_outputs/generated_html.html?raw";
const props = defineProps<{ sections: HtmlSectionItem[] }>()
const currentIndex = ref(0)
const currentSection = ref('')
const iframeRef = ref<HTMLIFrameElement | null>(null)
const scalerRef = ref<HTMLDivElement | null>(null)
const containerRef = ref<HTMLDivElement | null>(null)

watchEffect(() => {
  if (props.sections && props.sections.length > 0) {
    currentSection.value = props.sections[currentIndex.value].html
  } else {
    currentSection.value = ''
  }
})

watch(
  () => props.sections?.length ?? 0,
  (len) => {
    if (currentIndex.value >= len) currentIndex.value = len > 0 ? len - 1 : 0
  }
)

const prev = (): void => {
  if (currentIndex.value > 0) currentIndex.value--
}
const next = (): void => {
  if (props.sections && currentIndex.value < props.sections.length - 1) currentIndex.value++
}

// 让iframe高度自适应内容，并同步缩放后高度到外层容器
const scale = 0.643
const setIframeHeight = (): void => {
  if (iframeRef.value && scalerRef.value && containerRef.value) {
    try {
      const iframe = iframeRef.value
      const doc = iframe.contentDocument || iframe.contentWindow?.document
      if (doc) {
        // 获取实际内容高度
        const rawHeight = Math.max(
          doc.body.scrollHeight,
          doc.documentElement.scrollHeight,
          doc.body.offsetHeight,
          doc.documentElement.offsetHeight
        )

        // 添加额外的空间以确保内容完全显示
        const adjustedHeight = rawHeight + 20

        // 设置iframe高度
        iframe.style.height = adjustedHeight + 'px'

        // 设置缩放容器高度
        scalerRef.value.style.height = adjustedHeight + 'px'

        // 设置外层容器高度，考虑缩放比例
        containerRef.value.style.height = adjustedHeight * scale + 'px'
      }
    } catch (e) {
      console.error('设置iframe高度时出错:', e)
    }
  }
}

watch([currentSection, () => props.sections], async () => {
  await nextTick()
  // 多次尝试设置高度，确保内容完全加载
  setTimeout(setIframeHeight, 100)
  setTimeout(setIframeHeight, 300)
  setTimeout(setIframeHeight, 500)
})

onMounted(() => {
  setTimeout(setIframeHeight, 200)
  setTimeout(setIframeHeight, 500)
})
</script>

<script lang="ts">
export default {}
</script>

<style scoped>
/* 让按钮和内容不被挤压，始终可见 */
.pager-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  width: 100%;
  max-width: 100%;
  min-height: 300px;
  box-sizing: border-box;
  padding: 1rem 0;
  background: var(--bg-color);
  position: relative;
}

.pager-btn {
  font-size: 2rem;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--primary-color, #333);
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
}

.pager-btn:first-child {
  left: -45px;
}

.pager-btn:last-child {
  right: -45px;
}

.pager-btn:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.pager-content {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
  max-width: 100%;
  height: 100%;
  min-height: 0;
  box-sizing: border-box;
  position: relative;
}

.iframe-container {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  height: auto;
  width: 100%;
  overflow: visible;
  display: block;
  margin: 0 auto;
}

.iframe-scaler {
  width: 450px;
  /* 450/700 ≈ 0.643 */
  transform: scale(0.643);
  transform-origin: top center;
  margin: 0 auto;
  overflow: visible;
  height: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.html-iframe {
  width: 700px;
  min-height: 200px;
  border: none;
  display: block;
  overflow: hidden;
  height: auto;
  background-color: white;
}

.html-section-item {
  min-width: 320px;
  max-width: 100%;
  height: 100%;
  border: 1px solid var(--border-color, #eee);
  border-radius: 8px;
  background: #fff;
  color: #222;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.04);
  /* padding: 1.5rem; 移除padding，交给container */
  margin-bottom: 1rem;
  overflow: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.pager-indicator {
  text-align: center;
  color: #888;
  font-size: 1rem;
}

.empty-hint {
  color: var(--text-secondary);
  text-align: center;
  margin-left: 3rem;
  margin-right: 3rem;
  margin-top: 2rem;
  font-style: italic;
}
</style>
