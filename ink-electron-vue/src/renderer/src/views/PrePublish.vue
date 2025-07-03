<template>
  <div class="prepublish-container">
    <div class="main-content">
      <div class="display-section">
        <div class="display-header">
          <h2>预发布 - HTML转图片</h2>
          <div class="display-actions">
            <button class="action-btn" :disabled="loading" @click="handleConvert">
              {{ loading ? '生成中...' : '生成图片' }}
            </button>
          </div>
        </div>
        <div
          class="display-content"
          style="display: flex; flex-direction: column; align-items: center; min-height: 420px"
        >
          <div class="theme-edit">
            <label>主题文案：</label>
            <input v-model="themeText" placeholder="请输入主题文案" class="theme-input" />
          </div>
          <div v-if="imgUrl" class="img-preview-wrapper">
            <h3>图片预览</h3>
            <img :src="imgUrl" alt="预览图片" class="preview-img" />
          </div>
          <div v-if="errorMsg" class="prepublish-error">{{ errorMsg }}</div>
        </div>
      </div>
      <div class="form-section">
        <div class="form-header">
          <h3>HTML转图片参数</h3>
        </div>
        <div class="form-content">
          <div class="form-group">
            <label>HTML文件路径</label>
            <input v-model="htmlPath" placeholder="请输入HTML文件路径" />
          </div>
          <div class="form-group">
            <label>图片输出路径（可选）</label>
            <input v-model="outputPath" placeholder="可选，留空则自动生成" />
          </div>
          <div class="form-group">
            <label>宽度</label>
            <input v-model.number="width" type="number" min="100" max="2000" />
          </div>
          <div class="form-group">
            <label>高度</label>
            <input v-model.number="height" type="number" min="100" max="2000" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { htmlToImage } from '../api/htmlToImage'

const route = useRoute()
const htmlPath = ref('')
const outputPath = ref('')
const width = ref(375)
const height = ref(667)
const themeText = ref('')
const imgUrl = ref('')
const errorMsg = ref('')
const loading = ref(false)

// 获取API基础URL
const getApiBaseUrl = (): string => {
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000'
}

const handleConvert = async (): Promise<void> => {
  if (!htmlPath.value) {
    errorMsg.value = '请填写HTML文件路径'
    return
  }
  errorMsg.value = ''
  loading.value = true
  imgUrl.value = ''
  try {
    const res = await htmlToImage({
      html_path: htmlPath.value,
      output_path: outputPath.value || undefined,
      width: width.value,
      height: height.value
    })
    if (res.success) {
      if (res.image_url) {
        // 使用返回的图片URL
        imgUrl.value = getApiBaseUrl() + res.image_url
      } else if (res.output_path) {
        // 兼容旧版API，使用文件路径
        imgUrl.value = 'file://' + res.output_path
      } else {
        errorMsg.value = '生成成功但未返回图片URL'
      }
    } else {
      errorMsg.value = res.msg || '生成失败'
    }
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // 自动填充参数并自动生成
  if (route.query.html_path) {
    htmlPath.value = String(route.query.html_path)
  }
  if (route.query.theme) {
    themeText.value = String(route.query.theme)
  }
  if (htmlPath.value) {
    handleConvert()
  }
})
</script>

<style scoped>
.prepublish-container {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 108px);
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
  color: var(--text-primary);
}
.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  flex: 1;
  overflow: hidden;
}
.display-section {
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--bg-color);
}
.display-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}
.display-actions {
  display: flex;
  gap: 0.5rem;
}
.action-btn,
.prepublish-btn {
  padding: 0.6rem 1.2rem;
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}
.action-btn:disabled,
.prepublish-btn:disabled {
  background: var(--border-color);
  color: #aaa;
  cursor: not-allowed;
}
.display-content {
  flex: 1;
  padding: 1.5rem;
  overflow: visible;
  background: var(--bg-color);
  color: var(--text-primary);
  min-height: 300px;
  white-space: nowrap;
}
.theme-edit {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.theme-input {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--card-bg);
  color: var(--text-primary);
  width: 300px;
}
.img-preview-wrapper {
  margin-top: 1rem;
  background: var(--bg-color);
  border-radius: 8px;
  padding: 1rem;
  box-shadow: var(--card-shadow);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.preview-img {
  max-width: 100%;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: #fff;
}
.prepublish-error {
  color: #c3073f;
  margin-top: 1rem;
}
.form-section {
  border-left: 1px solid var(--border-color);
  overflow: hidden;
  background-color: var(--bg-color);
}
.form-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}
.form-content {
  padding: 1.5rem;
}
.form-group {
  margin-bottom: 1.5rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
.form-group input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--card-bg);
  color: var(--text-primary);
}
</style>
