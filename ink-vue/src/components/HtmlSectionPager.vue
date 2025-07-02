<template>
  <div class="pager-container" ref="pagerContainer" v-if="props.sections && props.sections.length">
    <button class="pager-btn" :disabled="currentIndex === 0" @click="prev">
      &#8592;
    </button>
    <div class="pager-content">
      <div class="iframe-container" ref="containerRef">
        <div class="iframe-scaler" ref="scalerRef">
          <iframe
            :srcdoc="currentSection"
            class="html-iframe"
            frameborder="0"
            scrolling="no"
            ref="iframeRef"
          ></iframe>
        </div>
      </div>
      <div class="pager-indicator">
        {{ currentIndex + 1 }} / {{ props.sections ? props.sections.length : 0 }}
      </div>
    </div>
    <button
      class="pager-btn"
      :disabled="!props.sections || currentIndex === (props.sections.length - 1)"
      @click="next"
    >
      &#8594;
    </button>
  </div>
  <p v-else class="empty-hint">生成的HTML将显示在这里...</p>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from "vue";
const pagerContainer = ref<HTMLElement | null>(null);
// import testHtml from "../../../ink-backend/tests/test_outputs/generated_html.html?raw";
const props = defineProps<{ sections?: string[] }>();
const currentIndex = ref(0);
const currentSection = ref("");
const iframeRef = ref<HTMLIFrameElement | null>(null);
const scalerRef = ref<HTMLDivElement | null>(null);
const containerRef = ref<HTMLDivElement | null>(null);

watch(
  [() => props.sections, currentIndex],
  () => {
    if (props.sections && props.sections.length > 0) {
      currentSection.value = props.sections[currentIndex.value];
    } else {
      currentSection.value = "";
    }
  },
  { immediate: true }
);

watch(
  () => props.sections?.length ?? 0,
  (len) => {
    if (currentIndex.value >= len) currentIndex.value = len > 0 ? len - 1 : 0;
  }
);

const prev = () => {
  if (currentIndex.value > 0) currentIndex.value--;
};
const next = () => {
  if (props.sections && currentIndex.value < props.sections.length - 1) currentIndex.value++;
};

// 让iframe高度自适应内容，并同步缩放后高度到外层容器
const scale = 0.643;
const setIframeHeight = () => {
  if (iframeRef.value && scalerRef.value && containerRef.value) {
    try {
      const iframe = iframeRef.value;
      const doc = iframe.contentDocument || iframe.contentWindow?.document;
      if (doc) {
        const rawHeight = doc.body.scrollHeight;
        iframe.style.height = rawHeight + "px";
        scalerRef.value.style.height = rawHeight + "px";
        containerRef.value.style.height = rawHeight * scale + "px";
      }
    } catch (e) {
      // 跨域等异常忽略
    }
  }
};

watch([currentSection, () => props.sections], async () => {
  await nextTick();
  setTimeout(setIframeHeight, 100); // 等待渲染
});

onMounted(() => {
  setTimeout(setIframeHeight, 200);
});
</script>

<script lang="ts">
export default {};
</script>

<style scoped>
/* 让按钮和内容不被挤压，始终可见 */
.pager-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  width: 100vw;
  max-width: 100%;
  min-height: 300px;
  box-sizing: border-box;
  padding: 2rem 0;
  background: #f8f8f8;
  overflow-x: auto;
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
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
  max-width: 100%;
  height: 100%;
  min-height: 0;
  box-sizing: border-box;
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
  margin-top: 2rem;
  font-style: italic;
}
.iframe-container {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  height: auto;
  width: auto;
  overflow: visible;
  display: block;
}

.iframe-scaler {
  width: 450px;
  /* 450/700 ≈ 0.643 */
  transform: scale(0.643);
  transform-origin: top left;
  margin: 0 auto;
  overflow: visible;
  height: auto;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.html-iframe {
  width: 700px;
  min-height: 0;
  border: none;
  display: block;
  overflow: hidden;
  height: auto;
}
</style>
