<template>
  <div class="image-carousel-container">
    <div class="view-switcher">
      <button :class="{ active: viewMode === 'note' }" @click="viewMode = 'note'">笔记预览</button>
      <button :class="{ active: viewMode === 'cover' }" @click="viewMode = 'cover'">
        封面预览
      </button>
    </div>

    <!-- 笔记预览 -->
    <div v-if="viewMode === 'note'" class="note-preview-wrapper">
      <div class="phone-frame">
        <div class="phone-top">
          <img src="../../public/Image/data_image_png;base….png" alt="phone-top" />
        </div>
        <div class="phone-nav">
          <img
            class="nav-bg-image"
            src="../../public/Image/data_image_png;base… (2).png"
            alt="nav background"
          />
          <div class="nav-user">
            <div class="avatar-icon-wrapper">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"
                  fill="currentColor"
                />
              </svg>
            </div>
            <span class="top-nickname">用户名</span>
          </div>
        </div>

        <div class="note-scrollable-content">
          <!-- 轮播图主体 -->
          <div class="carousel-main">
            <!-- 轮播图片区域 -->
            <div ref="carouselContent" class="carousel-content">
              <div
                v-for="(image, index) in images"
                :key="index"
                class="carousel-item"
                :class="{ active: currentIndex === index }"
                :style="{ transform: `translateX(${100 * (index - currentIndex)}%)` }"
              >
                <div class="image-container">
                  <img :src="image.url" :alt="title || '预览图片'" class="carousel-image" />
                </div>
              </div>
            </div>

            <!-- 页码指示器 -->
            <div v-if="images.length > 1" class="carousel-indicator">
              <span class="page-number">{{ currentIndex + 1 }}/{{ images.length }}</span>
            </div>

            <!-- 轮播控制按钮 -->
            <div v-if="images.length > 1" class="carousel-controls">
              <button
                class="control-btn prev"
                :class="{ btnDisabled: currentIndex === 0 }"
                :disabled="currentIndex === 0"
                @click="prevImage"
              >
                <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
                  <rect
                    x="1"
                    y="1"
                    width="24"
                    height="24"
                    rx="12"
                    fill="black"
                    fill-opacity="0.16"
                  />
                  <rect
                    x="0.83"
                    y="0.83"
                    width="24.33"
                    height="24.33"
                    rx="12.17"
                    stroke="black"
                    stroke-opacity="0.1"
                    stroke-width="0.33"
                  />
                  <path
                    d="M14.51 8.13c.19.2.2.51.02.71l-3.64 4.06c-.05.05-.05.13 0 .18l3.64 4.06c.18.2.17.52-.02.71a.48.48 0 0 1-.7-.02L9.8 13.34a.48.48 0 0 1 0-.69l4.03-4.5c.18-.2.49-.21.68-.02Z"
                    fill="white"
                  />
                </svg>
              </button>
              <button
                class="control-btn next"
                :class="{ btnDisabled: currentIndex === images.length - 1 }"
                :disabled="currentIndex === images.length - 1"
                @click="nextImage"
              >
                <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
                  <rect
                    width="24"
                    height="24"
                    rx="12"
                    transform="matrix(-1 0 0 1 25 1)"
                    fill="black"
                    fill-opacity="0.16"
                  />
                  <rect
                    x=".17"
                    y="-.17"
                    width="24.33"
                    height="24.33"
                    rx="12.17"
                    transform="matrix(-1 0 0 1 25.33 1)"
                    stroke="black"
                    stroke-opacity=".1"
                    stroke-width=".33"
                  />
                  <path
                    d="M11.49 8.13c-.2.2-.2.51 0 .71l3.64 4.06c.05.05.05.13 0 .18l-3.64 4.06c-.18.2-.17.52.02.71.19.2.5.19.68-.02l4.03-4.5a.48.48 0 0 0 0-.69l-4.03-4.5c-.18-.2-.49-.21-.68-.02Z"
                    fill="white"
                  />
                </svg>
              </button>
            </div>
          </div>

          <!-- 内容信息区域 -->
          <div class="content-info">
            <h3 class="content-title">{{ title }}</h3>
            <p class="content-description">{{ description }}</p>
          </div>

          <!-- 底部信息 -->
          <div class="post-info">
            <span class="post-time">编辑于 刚刚</span>
          </div>
          <div class="phone-bottom">
            <img src="../../public/Image/data_image_png;base… (1).png" alt="phone-bottom" />
          </div>
        </div>
        <!-- 底部操作栏 -->
        <div class="action-bar">
          <img src="../../public/Image/footer.6b103b36.png" />
        </div>
      </div>
    </div>

    <!-- 封面预览 -->
    <div v-if="viewMode === 'cover'" class="cover-preview-wrapper">
      <div class="cover-preview-frame">
        <img
          src="https://fe-static.xhscdn.com/formula-static/ugc/public/resource/image/topbar.592e462a.png"
          alt="top bar"
          class="cover-bar"
        />
        <div class="cover-content-wrapper">
          <div class="cover-content">
            <div class="column">
              <div v-for="(note, index) in column1" :key="`col1-${index}`" class="note-card">
                <img :src="note.cover" :alt="note.title" class="note-cover-image" />
                <div class="note-card-info">
                  <p class="note-card-title">{{ note.title }}</p>
                  <div class="note-card-user">
                    <div class="avatar-icon-wrapper small">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                          d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"
                          fill="currentColor"
                        />
                      </svg>
                    </div>
                    <span class="note-card-name">{{ note.user }}</span>
                    <span class="note-card-likes">♡ {{ note.likes }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="column">
              <div v-for="(note, index) in column2" :key="`col2-${index}`" class="note-card">
                <img :src="note.cover" :alt="note.title" class="note-cover-image" />
                <div class="note-card-info">
                  <p class="note-card-title">{{ note.title }}</p>
                  <div class="note-card-user">
                    <div class="avatar-icon-wrapper small">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                          d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"
                          fill="currentColor"
                        />
                      </svg>
                    </div>
                    <span class="note-card-name">{{ note.user }}</span>
                    <span class="note-card-likes">♡ {{ note.likes }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <img
          src="https://fe-static.xhscdn.com/formula-static/ugc/public/resource/image/homebar.5e8b4e25.png"
          alt="home bar"
          class="cover-bar"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'

interface ImageItem {
  url: string
}

interface Props {
  images: ImageItem[]
  title?: string
  description?: string
  autoplay?: boolean
  interval?: number
}

const props = withDefaults(defineProps<Props>(), {
  title: '默认标题',
  description: '',
  autoplay: false,
  interval: 3000
})

const viewMode = ref('note')
const currentIndex = ref(0)
const autoplayTimer = ref<number | null>(null)

const allNotes = computed(() => {
  if (!props.images || props.images.length === 0) {
    return []
  }
  return props.images.map((image, index) => ({
    title: `笔记标题 ${index + 1}`,
    user: '用户名',
    likes: Math.floor(Math.random() * 100),
    cover: image.url
  }))
})

const column1 = computed(() => allNotes.value.filter((_, i) => i % 2 === 0))
const column2 = computed(() => allNotes.value.filter((_, i) => i % 2 !== 0))

// 切换到下一张图片
const nextImage = (): void => {
  if (currentIndex.value < props.images.length - 1) {
    currentIndex.value++
  }
}

// 切换到上一张图片
const prevImage = (): void => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

// 启动自动播放
const startAutoplay = (): void => {
  if (props.autoplay && props.images.length > 1) {
    autoplayTimer.value = window.setInterval(() => {
      if (currentIndex.value < props.images.length - 1) {
        currentIndex.value++
      } else {
        currentIndex.value = 0
      }
    }, props.interval)
  }
}

// 停止自动播放
const stopAutoplay = (): void => {
  if (autoplayTimer.value) {
    clearInterval(autoplayTimer.value)
    autoplayTimer.value = null
  }
}

// 监听图片数组变化
watch(
  () => props.images,
  (newImages) => {
    if (newImages.length > 0) {
      currentIndex.value = 0
      if (props.autoplay) {
        stopAutoplay()
        startAutoplay()
      }
    }
  },
  { deep: true }
)

// 组件挂载时启动自动播放
onMounted(() => {
  if (props.autoplay) {
    startAutoplay()
  }
})

// 组件卸载时清除定时器
onUnmounted(() => {
  stopAutoplay()
})
</script>

<style scoped>
.image-carousel-container {
  width: 100%;
  margin: 0;
  font-family:
    'PingFang SC',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    sans-serif;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  height: calc(100vh - 150px);
  padding: 0 24px;
  box-sizing: border-box;
}

.view-switcher {
  display: flex;
  gap: 10px;
  background-color: #f0f0f0;
  padding: 4px;
  border-radius: 8px;
}

.view-switcher button {
  padding: 6px 12px;
  border: none;
  background-color: transparent;
  color: #666;
  font-size: 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.view-switcher button.active {
  background-color: white;
  color: #333;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.note-preview-wrapper,
.cover-preview-wrapper {
  width: auto;
  height: 100%;
  max-width: 100%;
  aspect-ratio: 375 / 750;
  margin: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.phone-frame,
.cover-preview-frame {
  width: 100%;
  height: 100%;
  background-color: white;
  display: flex;
  flex-direction: column;
}

.note-scrollable-content {
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* Note Preview Specific Styles */
.phone-top,
.phone-bottom {
  flex-shrink: 0;
  align-items: center;
  padding: 10px 15px;
  background-color: white;
}
.phone-top img,
.phone-bottom img,
.action-bar img {
  width: 100%;
  display: block;
}

.phone-nav {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
}

.nav-bg-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.nav-user {
  position: relative;
  z-index: 2;
  margin-left: 30px;
  margin-top: 3px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar-icon-wrapper {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
}
.avatar-icon-wrapper.small {
  width: 20px;
  height: 20px;
}
.avatar-icon-wrapper svg {
  width: 70%;
  height: 70%;
}

.top-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

.top-nickname {
  font-size: 10px;
  font-weight: 500;
  color: #333;
}

.follow-btn {
  padding: 4px 12px;
  background-color: #ff2442;
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
}

.carousel-main {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  background-color: #fff;
}

.carousel-content,
.carousel-item,
.image-container,
.carousel-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.carousel-content {
  display: flex;
}

.carousel-item {
  transition: transform 0.3s ease-in-out;
  flex-shrink: 0;
}

.carousel-image {
  object-fit: contain;
  width: 100%;
  height: 100%;
}

.carousel-controls {
  position: absolute;
  top: 50%;
  left: 10px;
  right: 10px;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  z-index: 10;
}

.control-btn {
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
}

.control-btn.btnDisabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.carousel-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.3);
  color: white;
  padding: 3px 8px;
  border-radius: 10px;
  font-size: 12px;
  z-index: 10;
}

.carousel-dots {
  position: absolute;
  bottom: 10px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 8px;
  z-index: 10;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.2s;
}

.dot.active {
  background-color: #ff2442;
  width: 16px;
  border-radius: 4px;
}

.content-info {
  padding: 15px;
  flex-shrink: 0;
}

.content-title {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
}

.content-description {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.65);
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-info {
  padding: 0 15px 10px;
  flex-shrink: 0;
}

.post-time {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
}

.action-bar {
  display: flex;
  padding: 0;
  border-top: none;
  flex-shrink: 0;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.65);
}

.action-item.input {
  flex-grow: 1;
  background-color: #f0f0f0;
  padding: 6px 10px;
  border-radius: 16px;
}

.action-icon {
  font-size: 14px;
}

/* Cover Preview Specific Styles */
.cover-bar {
  width: 100%;
  display: block;
  flex-shrink: 0;
}

.cover-content-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #f7f7f7;
}

.cover-content {
  display: flex;
  padding: 8px;
  gap: 8px;
}

.column {
  width: 50%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.note-card {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  break-inside: avoid;
  max-height: 40vh;
}

.note-cover-image {
  width: 100%;
  display: block;
}

.note-card-info {
  padding: 8px;
}

.note-card-title {
  font-size: 14px;
  color: #333;
  margin: 0 0 8px;
  font-weight: 500;
}

.note-card-user {
  display: flex;
  align-items: center;
  gap: 6px;
}

.note-card-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.note-card-name {
  font-size: 12px;
  color: #666;
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-card-likes {
  font-size: 12px;
  color: #999;
}
</style>
