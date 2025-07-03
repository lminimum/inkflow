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
        <img
          src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfYAAAA8CAYAAACU75jaAAAFiElEQVR4Xu3dMU7rTBSG4SyBJbAElsAS2AEsgR3ADqClgoqGAhASFRKChgohQQEVVBQ00FAgGv/68utwD+faDr44iefofaQRTuyMc5O583k8TjIaAQCAPKqqWqNQKBQKhZKjjCoAAJAGwQ4AQCIEOwAAiRDsAAAkQrADAJAIwQ4AQCIEOwAAiRDsAAAkQrADAJAIwQ4AQCIEOwAAiRDsAAAkQrADAJAIwQ4AQCIEOwAAiRDsAAAkQrADAJAIwQ4AQCIEOwAAiRDsAAAkQrADAJAIwQ4AmIqnp6dqd3e32t7erjY3N8d/Dw8Pq5ubm7hpJ5+fn9X9/X11e3s7tfLy8hJ3W4zig90aTh+NBQDwf7+6sLBQjUajanFxsTo/P4+bNNK26+vrX49vKqp3bW1tvK8uHh4eqv39/erg4KA6Pj6eWtE+Li8v4+6LUGywK8SXl5drG0vXhhKpDl9nEx19+sYPABlodO37QN2eRP1uXZ/8k/LTgH9/fx8HrkbU0/b6+jo+eJjFvvrWnFoD5o8mVZaWlr41qN+Ee2zQKlFdAybYAWQR+8FJwe4HOb7oPvWVCm4rut207d7eXqz6G4WsRtOifnhlZWVcX9/Fnsf19fXX/kryd2oVQC+8NQR/ikhvtI22tU1XerxvyLbs6UyBNUr9tf0R7ABKoylM9V0q6jPf3t7G93cJ9rit9b+TTt9r39aX+6KDhCYK9rOzs/GyBnTxsX0W5YE/kChJccGuhmcvfF0D0Hy7rY8NyxptEwvpjY2Nb/V4dr/9J7CGSbADKE0MVuszY1i3BbvvK+vm4zUY0jZN10LZwYXVodtNfLDHKdO+i/4dPtifn5/9Uxm04oJdL7Z/4SM/6vbBb42v6TS9NWQL6KZgV6Pb2tr6uk2wAyhVH8Eu6i/9iF9/9Zi6U+7WX2q99cU2val62swz2E9OToqZby8u2JuC2xwdHX2t13yO0VyM3R/ncXyd1rCbgj0i2AEMnfpKmz/2Id1XsHsa/DQFeizqN9tG6NG8g33SgcdQtKfWQNkbGkffWvZvtsLc6A2xOfE4YrfQ9wcCBDuALGJomb6D3U+VWvEX0OlvXehPmiY18w72nZ0d/3QGqz21BkpHeP4NUGNROFtw20UVPtibNJ2iJ9gBlEYBqX4sBmUMLdN3sIv1neqPtRyfi21jwdxlFDzvYLfXZ+jaU2vAfMOwYuFsjdWPwJtYHbpgziPYAZQknrH0U5UxtMw0gl00+PIDJV0wp7r9hXNa3+U0vMwz2LX88fHhn85gtadWAfTixyst7VRP3Ry8F+fj42ct/Tp9k1Idgh3AEKgv9MGkvsnE0DLTCnajfjkGcDw72sUsg13PnY+7zZBG0yrxYxO2zr8xbfy2k0pTcBPsAIZgiMGuTxDFfat0HakbBe3p6el4Wf133Xx9H2V1dfWv/ZWkyGD3YeqP/PypKM2ze1qnOXeNvm3OR8GvBltX/FX0ut00+ifYAQzBEINdNM3p6+oypx7ph1n0lbKz+IEWfX2tRutXV1dx1eAVGey+AStQLbD9N8LFUz2+AcePu9Vhjh1ASTRg8SNYf42R/5Y231f5APf9ZrxA+TdhLBbuv61HFLT2Ay1anlaxH5lRwJemPbUGLH5bkW+0dafgfQOuWx8R7ABKo2DWwCf2cXa/SrxKfdL9sa5/1Vc98vj4WF1cXIzn26dRVPfd3d3452FL1J5aBVDAK7Q1l1PXOD1tq21+wj42Ekf+0U+3AwBgFooPdgAA8AfBDgBAIgQ7AACJEOwAACRCsAMAkAjBDgBAIgQ7AACJEOwAACRCsAMAkAjBDgBAIgQ7AACJEOwAACRCsAMAkAjBDgBAIgQ7AACJEOwAACRCsAMAkAjBDgBAIgQ7AACJEOwAACTyH9o48UXhkTTjAAAAAElFTkSuQmCC"
          alt="status bar"
          class="status-bar"
        />
        <!-- 导航栏 -->
        <div class="phone-nav">
          <div class="nav-back">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M15.41 7.41L14 6L8 12L14 18L15.41 16.59L10.83 12L15.41 7.41Z"
                fill="currentColor"
              />
            </svg>
          </div>
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
          <div class="nav-actions">
            <button class="follow-btn">关注</button>
            <svg
              class="share-icon"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M18 16.08C17.24 16.08 16.56 16.38 16.04 16.85L8.91 12.7C8.96 12.47 9 12.24 9 12C9 11.76 8.96 11.53 8.91 11.3L16.04 7.15C16.56 7.62 17.24 7.92 18 7.92C19.66 7.92 21 6.58 21 4.92C21 3.26 19.66 1.92 18 1.92C16.34 1.92 15 3.26 15 4.92C15 5.16 15.04 5.39 15.09 5.62L7.96 9.77C7.44 9.3 6.76 9 6 9C4.34 9 3 10.34 3 12C3 13.66 4.34 15 6 15C6.76 15 7.44 14.7 7.96 14.23L15.09 18.38C15.04 18.61 15 18.84 15 19.08C15 20.74 16.34 22.08 18 22.08C19.66 22.08 21 20.74 21 19.08C21 17.42 19.66 16.08 18 16.08Z"
                fill="currentColor"
              />
            </svg>
          </div>
        </div>

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
                <rect x="1" y="1" width="24" height="24" rx="12" fill="black" fill-opacity="0.16" />
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

          <!-- 轮播指示点 -->
          <div v-if="images.length > 1" class="carousel-dots">
            <span
              v-for="(_, index) in images"
              :key="index"
              class="dot"
              :class="{ active: currentIndex === index }"
              @click="goToImage(index)"
            ></span>
          </div>
        </div>

        <!-- 内容信息区域 -->
        <div class="note-body">
          <div class="content-info">
            <h3 class="content-title">{{ title }}</h3>
            <p class="content-description">{{ description }}</p>
          </div>

          <!-- 底部信息 -->
          <div class="post-info">
            <span class="post-time">编辑于 刚刚</span>
          </div>

          <!-- 评论区 -->
          <div class="comment-section">
            <div class="wasteland">
              <svg
                width="48"
                height="48"
                viewBox="0 0 48 48"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle cx="24" cy="24" r="24" fill="#F0F0F0" />
                <path
                  d="M26 20C26 21.1046 25.1046 22 24 22C22.8954 22 22 21.1046 22 20C22 18.8954 22.8954 18 24 18C25.1046 18 26 18.8954 26 20Z"
                  fill="#CCCCCC"
                />
                <path
                  d="M30 20C30 21.1046 29.1046 22 28 22C26.8954 22 26 21.1046 26 20C26 18.8954 26.8954 18 28 18C29.1046 18 30 18.8954 30 20Z"
                  fill="#CCCCCC"
                />
                <path
                  d="M20 20C20 21.1046 19.1046 22 18 22C16.8954 22 16 21.1046 16 20C16 18.8954 16.8954 18 18 18C19.1046 18 20 18.8954 20 20Z"
                  fill="#CCCCCC"
                />
                <path
                  d="M16 30C16 28 19 27 24 27C29 27 32 28 32 30"
                  stroke="#CCCCCC"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
              <p>这是一片荒草地，分享笔记</p>
            </div>
          </div>
        </div>

        <!-- 底部操作栏 -->
        <div class="action-bar">
          <div class="action-item input">
            <span class="action-icon">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z"
                  fill="currentColor"
                />
              </svg>
            </span>
            <span class="action-text">说点什么...</span>
          </div>
          <div class="action-buttons">
            <div class="action-item">
              <span class="action-icon">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M16.5 3C14.76 3 13.09 3.81 12 5.09C10.91 3.81 9.24 3 7.5 3C4.42 3 2 5.42 2 8.5C2 12.28 5.4 15.36 10.55 20.03L12 21.35L13.45 20.03C18.6 15.36 22 12.28 22 8.5C22 5.42 19.58 3 16.5 3Z"
                    stroke="currentColor"
                    stroke-width="1.5"
                    fill="none"
                  />
                </svg>
              </span>
              <span class="action-text">点赞</span>
            </div>
            <div class="action-item">
              <span class="action-icon">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12 17.27L18.18 21L16.54 13.97L22 9.24L14.81 8.63L12 2L9.19 8.63L2 9.24L7.46 13.97L5.82 21L12 17.27Z"
                    stroke="currentColor"
                    stroke-width="1.5"
                    fill="none"
                  />
                </svg>
              </span>
              <span class="action-text">收藏</span>
            </div>
            <div class="action-item">
              <span class="action-icon">
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M20 2H4C2.9 2 2 2.9 2 4V16C2 17.1 2.9 18 4 18H18L22 22V4C22 2.9 21.1 2 20 2Z"
                    stroke="currentColor"
                    stroke-width="1.5"
                    fill="none"
                  />
                </svg>
              </span>
              <span class="action-text">评论</span>
            </div>
          </div>
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

const dummyNotes = [
  {
    title: '示例笔记标题1',
    user: '用户名',
    likes: 12,
    cover: 'https://via.placeholder.com/300x400.png/f0f0f0/999999?text=Cover+1'
  },
  {
    title: '示例笔记标题2',
    user: '用户名',
    likes: 5,
    cover: 'https://via.placeholder.com/300x350.png/f0f0f0/999999?text=Cover+2'
  },
  {
    title: '示例笔记标题3',
    user: '用户名',
    likes: 33,
    cover: 'https://via.placeholder.com/300x450.png/f0f0f0/999999?text=Cover+3'
  }
]

const allNotes = computed(() => {
  if (props.images.length === 0) {
    return [...dummyNotes]
  }
  return [
    {
      title: props.title,
      user: '用户名',
      likes: 0,
      cover: props.images[0].url
    },
    ...dummyNotes
  ]
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

// 切换到指定图片
const goToImage = (index: number): void => {
  if (index >= 0 && index < props.images.length) {
    currentIndex.value = index
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
  height: calc(100vh - 108px);
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
  aspect-ratio: 375 / 812;
  margin: 0;
  overflow: hidden;
  border-radius: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.phone-frame,
.cover-preview-frame {
  width: 100%;
  height: 100%;
  background-color: white;
  display: flex;
  flex-direction: column;
}

.status-bar {
  width: 100%;
  display: block;
  flex-shrink: 0;
}

/* Note Preview Specific Styles */
.phone-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  background-color: white;
  flex-shrink: 0;
  color: #333;
}

.nav-back,
.nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-back {
  font-size: 24px;
  color: #333;
}

.nav-user {
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
  font-size: 14px;
  font-weight: 500;
}

.follow-btn {
  padding: 4px 12px;
  background-color: #fff;
  color: #ff2442;
  border: 1px solid #ff2442;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
}

.share-icon {
  font-size: 24px;
}

.carousel-main {
  position: relative;
  width: 100%;
  flex-grow: 1;
  background-color: #fff;
  overflow: hidden;
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

.note-body {
  padding: 15px;
  flex-shrink: 0;
  background-color: #fff;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.content-info {
  padding-bottom: 15px;
}

.content-title {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

.content-description {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.65);
}

.post-info {
  padding: 10px 0;
  border-top: 1px solid #f0f0f0;
  flex-shrink: 0;
}

.post-time {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
}

.comment-section {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
}

.wasteland {
  text-align: center;
  color: #ccc;
}
.wasteland p {
  margin-top: 10px;
  font-size: 12px;
}

.action-bar {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  border-top: 1px solid #f0f0f0;
  gap: 15px;
  flex-shrink: 0;
  background-color: #fff;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.85);
}

.action-item.input {
  flex-grow: 1;
  background-color: #f0f0f0;
  padding: 6px 10px;
  border-radius: 16px;
  color: #999;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 15px;
}

.action-icon {
  font-size: 20px;
  display: flex;
  align-items: center;
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
