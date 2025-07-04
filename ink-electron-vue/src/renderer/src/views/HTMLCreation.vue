<template>
  <div class="html-creation-container">
    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧预览区 -->
      <div class="display-section">
        <div
          class="display-content"
          style="
            display: flex;
            justify-content: center;
            align-items: center;
            height: 420px;
            max-width: 700px;
            margin: 0 auto;
            background: var(--bg-color);
            border-radius: 8px;
            box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.04);
            overflow: hidden;
          "
        >
          <!-- 限定内容区域大小，内容自适应缩放 -->
          <HtmlSectionPager :sections="htmlSections" />
        </div>
      </div>

      <!-- 右侧表单区 -->
      <div class="form-section">
        <div class="form-content">
          <div class="mode-toggle">
            <button :class="{ active: creationMode === 'custom' }" @click="creationMode = 'custom'">
              自定义主题
            </button>
            <button
              :class="{ active: creationMode === 'hotspot' }"
              @click="creationMode = 'hotspot'"
            >
              今日热点
            </button>
          </div>

          <form @submit.prevent="handleGenerateHtml">
            <div v-if="creationMode === 'custom'" class="form-group">
              <label for="theme">主题</label>
              <input
                id="theme"
                v-model="formData.theme"
                type="text"
                required
                placeholder="输入主题"
              />
            </div>
            <div v-else class="form-group">
              <label>热点分析</label>
              <button
                type="button"
                class="secondary-btn"
                :disabled="isAnalyzingHotspots"
                @click="handleAnalyzeHotspots"
              >
                {{ isAnalyzingHotspots ? '分析中...' : '分析今日热点' }}
              </button>
            </div>

            <div class="form-group">
              <label for="style">风格</label>
              <select id="style" v-model="formData.style" required class="form-select">
                <option value="">请选择风格</option>
                <option v-for="option in styleOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
                <option value="custom">自定义</option>
              </select>
              <input
                v-if="formData.style === 'custom'"
                v-model="formData.customStyle"
                placeholder="请输入自定义风格"
                class="form-custom-input"
              />
            </div>
            <div class="form-group">
              <label for="audience">受众</label>
              <select id="audience" v-model="formData.audience" required class="form-select">
                <option value="">请选择受众</option>
                <option v-for="option in audienceOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
                <option value="custom">自定义</option>
              </select>
              <input
                v-if="formData.audience === 'custom'"
                v-model="formData.customAudience"
                placeholder="请输入自定义受众"
                class="form-custom-input"
              />
            </div>
            <div class="form-group">
              <label for="numSections">生成数量</label>
              <input
                id="numSections"
                v-model.number="formData.numSections"
                type="number"
                min="1"
                max="20"
                required
                style="width: 100px"
              />
            </div>

            <!-- 模型选择 -->
            <div class="form-group">
              <label for="model">AI模型</label>
              <select
                id="model"
                v-model="selectedModel"
                class="form-select"
                @change="handleModelChange(selectedModel)"
              >
                <option value="">默认模型</option>
                <option
                  v-for="option in modelsStore.modelOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }} ({{ option.provider }})
                </option>
              </select>
              <div v-if="modelsStore.isLoading" class="model-loading">正在加载模型列表...</div>
              <div v-if="modelsStore.error" class="model-error">{{ modelsStore.error }}</div>
            </div>

            <button
              type="submit"
              class="generate-btn"
              :disabled="isGenerating || (creationMode === 'hotspot' && !hotspotAnalysisResult)"
            >
              <template v-if="isGenerating">生成中...</template>
              <template v-else>生成HTML</template>
            </button>

            <div v-if="showPreviewButton" class="preview-btn-container">
              <button type="button" class="preview-btn" @click="handlePreviewClick">
                生成预览
              </button>
            </div>
          </form>
        </div>

        <!-- 进度信息区 -->
        <div v-if="currentStage || isGenerating" class="progress-info">
          <div class="progress-stage">{{ currentStage || '准备中...' }}</div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: generationProgress + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 预览与编辑区域 -->
    <div v-if="showPreview" class="preview-layout">
      <!-- 左侧预览 -->
      <div class="preview-section-left">
        <h2 class="preview-title">图文预览</h2>

        <!-- 加载中状态 -->
        <div v-if="isLoadingPreview" class="preview-loading">正在生成预览图片...</div>

        <!-- 错误信息 -->
        <div v-if="previewError" class="preview-error">
          {{ previewError }}
        </div>

        <!-- 使用轮播组件 -->
        <div v-if="previewImages.length > 0" class="carousel-wrapper">
          <ImageCarousel
            :images="previewImages"
            :title="formData.theme"
            :description="editableDescription"
          />
        </div>

        <!-- 无图片提示 -->
        <div v-else-if="!isLoadingPreview && !previewError" class="no-images">暂无预览图片</div>
      </div>

      <!-- 右侧编辑区 - 美化版 -->
      <div class="edit-section-right">
        <div class="editor-card">
          <h2 class="editor-title">编辑发布信息</h2>

          <div class="form-group">
            <label for="preview-theme"> <span class="label-icon">📝</span>标题 </label>
            <input
              id="preview-theme"
              v-model="formData.theme"
              type="text"
              placeholder="输入吸引人的标题"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="preview-description"> <span class="label-icon">📄</span>内容描述 </label>
            <textarea
              id="preview-description"
              v-model="editableDescription"
              rows="8"
              placeholder="输入详细的内容描述..."
              class="form-textarea"
            ></textarea>
            <div class="textarea-counter">{{ editableDescription.length }}/1000 字</div>
          </div>

          <div class="form-group">
            <label for="preview-topics"> <span class="label-icon">#️⃣</span>话题标签 </label>
            <div class="tags-input-container">
              <input
                id="preview-topics"
                v-model="topicTags"
                type="text"
                placeholder="用逗号分隔多个标签，如：种草,分享,日常"
                class="form-input"
              />
              <div class="tags-preview" v-if="parsedTags.length > 0">
                <span v-for="(tag, index) in parsedTags" :key="index" class="tag-pill">
                  #{{ tag }}
                </span>
              </div>
            </div>
          </div>

          <button
            type="button"
            class="publish-btn"
            :disabled="isPublishing"
            @click="handleAutoPublish"
          >
            <span class="btn-icon">🚀</span>
            {{ isPublishing ? '发布中...' : '一键发布到小红书' }}
          </button>

          <div
            v-if="publishMessage"
            :class="['publish-message', publishSuccess ? 'success' : 'error']"
          >
            <span class="message-icon">{{ publishSuccess ? '✅' : '❌' }}</span>
            {{ publishMessage }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useHtmlStore } from '../store/htmlStore'
import { useModelsStore } from '../store/modelsStore'
import HtmlSectionPager from '../components/HtmlSectionPager.vue'
import ImageCarousel from '../components/ImageCarousel.vue'
import {
  generateTitle,
  generateCss,
  generateContent,
  splitContentIntoSections,
  generateSectionHtml,
  type HTMLGenerateParams,
  type ContentRequestParams,
  type SectionsRequestParams,
  type SectionHTMLRequestParams
} from '../api/htmlGenerate'
import { htmlToImage, type HtmlToImageParams } from '../api/htmlToImage'
import { analyzeHotspots } from '../api/hotspot'
import { publishToXHS } from '../api/xhsPublish'
import type { FormData } from '../store/htmlStore'

// 表单数据
const formData = ref<FormData>({
  theme: '',
  style: '',
  audience: '',
  numSections: 1,
  customStyle: '',
  customAudience: ''
})

// 模型选择相关
const modelsStore = useModelsStore()
const selectedModel = ref('')
const selectedProvider = ref('')

const creationMode = ref('custom') // 'custom' or 'hotspot'
const isAnalyzingHotspots = ref(false)
const hotspotAnalysisResult = ref('')

const handleAnalyzeHotspots = async (): Promise<void> => {
  isAnalyzingHotspots.value = true
  hotspotAnalysisResult.value = ''
  try {
    const response = await analyzeHotspots()
    hotspotAnalysisResult.value = response.report
  } catch (err) {
    alert('热点分析失败，请稍后重试。')
    console.error('Failed to analyze hotspots:', err)
  } finally {
    isAnalyzingHotspots.value = false
  }
}

const styleOptions = ref([
  { value: '杂志封面风', label: '杂志封面风' },
  { value: '极简信息图风', label: '极简信息图风' },
  { value: '可爱手绘涂鸦风', label: '可爱手绘涂鸦风' },
  { value: '拼贴手帐风', label: '拼贴手帐风' },
  { value: '复古胶片风', label: '复古胶片风' },
  { value: '高饱和大字报风', label: '高饱和大字报风' },
  { value: 'modern', label: '现代' },
  { value: 'minimalist', label: '简约' },
  { value: 'retro', label: '复古' },
  { value: 'professional', label: '专业' },
  { value: 'creative', label: '创意' }
])

const audienceOptions = ref([
  { value: 'children', label: '儿童' },
  { value: 'teenagers', label: '青少年' },
  { value: 'adults', label: '成人' },
  { value: 'professionals', label: '专业人士' }
])

// 生成状态
const isGenerating = ref(false)
const htmlStore = useHtmlStore()
const { htmlSections, sectionDescriptions: storeSectionDescriptions } = storeToRefs(htmlStore)

// 用于存储完整的HTML，用于复制和预览
const fullGeneratedHtml = ref('')

// 进度信息相关
const currentStage = ref('')
const generationProgress = ref(0)
const showPreviewButton = ref(false)
const showPreview = ref(false)
const sectionDescriptions = ref<string[]>([])

// 图片预览相关
const previewImages = ref<Array<{ url: string }>>([])
const isLoadingPreview = ref(false)
const previewError = ref('')
const editableDescription = ref('')

// 添加发布相关状态变量
const isPublishing = ref(false)
const publishMessage = ref('')
const publishSuccess = ref(false)
const topicTags = ref('')

// 计算属性：解析话题标签
const parsedTags = computed(() => {
  if (!topicTags.value) return []
  return topicTags.value
    .split(',')
    .map((tag) => tag.trim())
    .filter((tag) => tag)
})

// 获取API基础URL
const getApiBaseUrl = (): string => {
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000'
}

// 生成HTML
const handleGenerateHtml = async (): Promise<void> => {
  const theme = creationMode.value === 'custom' ? formData.value.theme : hotspotAnalysisResult.value
  // 表单验证
  if (!theme || !formData.value.style || !formData.value.audience) {
    alert('请确保主题、风格和受众都已提供。')
    return
  }

  // 处理自定义风格/受众
  let style = formData.value.style === 'custom' ? formData.value.customStyle : formData.value.style
  let audience =
    formData.value.audience === 'custom' ? formData.value.customAudience : formData.value.audience

  isGenerating.value = true
  showPreviewButton.value = false
  showPreview.value = false
  htmlStore.clearHtml()
  fullGeneratedHtml.value = ''
  sectionDescriptions.value = []
  generationProgress.value = 0
  currentStage.value = '正在生成标题'

  try {
    // 准备AI模型参数
    const aiParams = selectedModel.value
      ? {
          model: selectedModel.value,
          service: selectedProvider.value
        }
      : undefined

    // 1. 调用生成标题接口
    const titleParams: HTMLGenerateParams = {
      theme: theme,
      style,
      audience,
      ...(aiParams && { model: aiParams.model, service: aiParams.service })
    }
    const titleResponse = await generateTitle(titleParams)
    if (!titleResponse || !titleResponse.title) {
      throw new Error('从后端获取标题失败或标题为空。')
    }
    const title = titleResponse.title
    generationProgress.value = 20
    currentStage.value = '正在生成CSS'

    // 2. 调用生成CSS接口
    const cssParams: HTMLGenerateParams = {
      theme: theme,
      style,
      audience,
      ...(aiParams && { model: aiParams.model, service: aiParams.service })
    }
    const cssResponse = await generateCss(cssParams)
    if (!cssResponse || !cssResponse.css_style) {
      throw new Error('从后端获取CSS失败或CSS为空。')
    }
    const css_style = cssResponse.css_style
    generationProgress.value = 40
    currentStage.value = '正在生成内容'

    // 3. 调用生成内容接口
    const contentParams: ContentRequestParams = {
      title: title,
      theme: theme,
      style,
      audience,
      ...(aiParams && { model: aiParams.model, service: aiParams.service })
    }
    const contentResponse = await generateContent(contentParams)
    if (!contentResponse || !contentResponse.content) {
      throw new Error('从后端获取内容失败或内容为空。')
    }
    const content = contentResponse.content
    generationProgress.value = 60
    currentStage.value = '正在分割内容'

    // 4. 调用内容分割接口
    const sectionsParams: SectionsRequestParams = {
      content: content,
      num_sections: formData.value.numSections
    }
    const sectionsResponse = await splitContentIntoSections(sectionsParams)
    if (
      !sectionsResponse ||
      !Array.isArray(sectionsResponse.sections) ||
      sectionsResponse.sections.length === 0
    ) {
      throw new Error('从后端分割内容失败或内容片段为空。')
    }
    const textSections = sectionsResponse.sections
    sectionDescriptions.value = [...textSections]
    htmlStore.saveSectionDescriptions(textSections)
    generationProgress.value = 70
    currentStage.value = '正在生成内容区块HTML'

    // 5. 遍历内容片段，调用生成单个内容区块HTML接口
    let sectionHtmlArr: string[] = []
    let progressStep = 30 / textSections.length

    for (let i = 0; i < textSections.length; i++) {
      const section = textSections[i]
      const sectionHtmlParams: SectionHTMLRequestParams = {
        title: title,
        description: section,
        style: style,
        css_style: css_style
      }
      try {
        const sectionHtmlResponse = await generateSectionHtml(sectionHtmlParams)
        if (sectionHtmlResponse && sectionHtmlResponse.html) {
          // 存储 html、file_path 和 html_url
          htmlStore.addHtmlSection({
            html: sectionHtmlResponse.html,
            file_path: sectionHtmlResponse.file_path,
            html_url: sectionHtmlResponse.html_url,
            section_id: sectionHtmlResponse.section_id
          })
          sectionHtmlArr.push('已生成')
        } else {
          sectionHtmlArr.push('生成失败')
        }
        generationProgress.value = 70 + (i + 1) * progressStep
      } catch (err) {
        sectionHtmlArr.push('生成失败' + err)
      }
    }

    if (htmlStore.htmlSections.length === 0) {
      throw new Error('所有内容区块HTML生成失败或为空。')
    }

    generationProgress.value = 100
    currentStage.value = '生成完成'

    setTimeout(() => {
      isGenerating.value = false
      currentStage.value = ''
      showPreviewButton.value = true
      // 保存表单数据到 store
      htmlStore.saveFormData(formData.value)
    }, 1000)
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error)
    alert(`生成失败: ${message}`)
    isGenerating.value = false
    currentStage.value = ''
  }
}

// 处理预览按钮点击
const handlePreviewClick = async (): Promise<void> => {
  if (htmlSections.value.length === 0) {
    return
  }

  await generatePreview()
}

// 提取预览生成逻辑为单独函数
const generatePreview = async (): Promise<void> => {
  isLoadingPreview.value = true
  previewError.value = ''
  previewImages.value = []
  showPreview.value = true
  editableDescription.value =
    storeSectionDescriptions.value.length > 0 ? storeSectionDescriptions.value[0] : '暂无描述'

  try {
    // 为每个HTML部分生成图片
    for (const section of htmlSections.value) {
      if (!section.file_path && !section.html_url) continue

      // 修复路径问题：尝试不同的路径格式
      let htmlPath = ''

      if (section.html_url) {
        // 如果是相对路径，不要添加前缀
        if (section.html_url.startsWith('/')) {
          // 去掉开头的斜杠，因为后端可能期望相对路径
          htmlPath = section.html_url.substring(1)
        } else {
          htmlPath = section.html_url
        }
      } else if (section.file_path) {
        htmlPath = section.file_path
      }

      if (!htmlPath) continue

      // 调用HTML转图片接口
      const params: HtmlToImageParams = {
        html_path: htmlPath,
        width: 750
      }

      console.log('发送HTML转图片请求，路径:', htmlPath)
      const result = await htmlToImage(params)

      if (result.success && (result.image_url || result.output_path)) {
        // 构建图片URL
        const imageUrl = result.image_url
          ? getApiBaseUrl() + result.image_url
          : result.output_path
            ? 'file://' + result.output_path
            : ''

        if (imageUrl) {
          // 只需要 url 属性，适配 ImageCarousel 组件
          previewImages.value.push({ url: imageUrl })
        }
      } else {
        console.error('HTML转图片失败:', result.msg || '未知错误')
      }
    }

    if (previewImages.value.length === 0) {
      previewError.value = '生成预览图片失败'
    }
  } catch (error) {
    console.error('预览生成错误:', error)
    previewError.value = error instanceof Error ? error.message : String(error)
  } finally {
    isLoadingPreview.value = false
  }
}

// 监听showPreviewButton变化，当为true且之前已经预览过时自动预览
watch(showPreviewButton, (newVal) => {
  if (newVal && htmlStore.htmlSections.length > 0 && htmlStore.hasGeneratedContent) {
    generatePreview()
  }
})

const handleAutoPublish = async (): Promise<void> => {
  if (!formData.value.theme || !editableDescription.value || previewImages.value.length === 0) {
    alert('主题、描述和预览图片不能为空')
    return
  }

  try {
    // 显示加载状态
    isPublishing.value = true
    publishMessage.value = ''
    currentStage.value = '正在发布到小红书...'

    // 准备要发布的图片
    const imageUrls = previewImages.value.map((img) => img.url)

    // 处理话题标签
    const topics = topicTags.value
      ? topicTags.value
          .split(',')
          .map((tag) => tag.trim())
          .filter((tag) => tag)
      : []

    // 调用发布接口
    const result = await publishToXHS({
      title: formData.value.theme,
      content: editableDescription.value,
      topics: topics,
      images: imageUrls
    })

    // 处理结果
    if (result.success) {
      publishSuccess.value = true
      publishMessage.value = '发布成功！笔记已提交到小红书。'
      console.log('发布成功:', result)
    } else {
      publishSuccess.value = false
      publishMessage.value = `发布失败: ${result.message}`
      console.error('发布失败:', result)
    }
  } catch (error) {
    publishSuccess.value = false
    publishMessage.value = `发布过程出错: ${error instanceof Error ? error.message : String(error)}`
    console.error('发布过程出错:', error)
  } finally {
    // 清除加载状态
    isPublishing.value = false
    currentStage.value = ''
  }
}

// 页面初始化时恢复内容和加载模型
onMounted(() => {
  // 加载模型列表
  modelsStore.loadModels()

  // 检查 store 中是否已有内容，如果有则自动预览
  if (htmlStore.htmlSections.length > 0) {
    showPreviewButton.value = true
    // 恢复表单数据
    formData.value = { ...htmlStore.formData }

    // 如果之前已经生成过内容，自动显示预览
    if (htmlStore.hasGeneratedContent) {
      setTimeout(() => {
        generatePreview()
      }, 500)
    }
  } else {
    htmlStore.clearAll()
    fullGeneratedHtml.value = ''
  }
})

// 监听模型选择变化
const handleModelChange = (model: string): void => {
  selectedModel.value = model
  // 找到对应的提供商
  const selectedOption = modelsStore.modelOptions.find((option) => option.value === model)
  if (selectedOption) {
    selectedProvider.value = selectedOption.provider
  }
}
</script>

<style scoped>
.html-creation-container {
  padding: 1rem;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 108px);
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.toolbar {
  display: flex;
  gap: 1rem;
}

.toolbar-btn {
  padding: 0.4rem 0.8rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
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

.action-btn {
  padding: 0.6rem 1.2rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
  color: var(--text-primary);
}

.action-btn:hover,
.action-btn:active {
  color: var(--primary-color);
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

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  background-size: 1em;
}

.generate-btn {
  width: 100%;
  padding: 0.6rem 1.2rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
  color: var(--text-primary);
  font-size: 1rem;
}

.generate-btn:hover,
.generate-btn:active {
  color: var(--primary-color);
}

.generate-btn:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
}

.html-section-list {
  display: flex; /* 使用 flexbox 实现水平布局 */
  flex-direction: row; /* 子元素水平排列 */
  gap: 2rem;
  padding-bottom: 1rem; /* 避免滚动条遮挡内容 */
}

.html-section-item {
  flex: 0 0 auto; /* 不伸缩，不收缩，基于内容决定大小 */
  width: 80%; /* 或者一个固定宽度，根据需要调整 */
  max-width: 600px; /* 最大宽度限制 */
  border: 1px solid var(--border-color);
  border-radius: 8px;
  /* margin-bottom: 1rem; */ /* 移除底部 margin */
  padding: 1.5rem;
  background: var(--bg-color);
  color: var(--text-primary);
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.04);
  min-height: 200px;
  overflow-x: auto; /* 允许单个 section 内部滚动 */
}

.debug-info {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  margin: 1.5rem 0 0 0;
  padding: 1rem;
  font-size: 0.95rem;
  color: var(--text-primary);
  max-height: 350px;
  overflow: auto;
}

.debug-stage {
  color: var(--primary-color);
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.debug-result {
  margin-bottom: 0.5rem;
}

.debug-label {
  font-weight: bold;
  color: var(--text-secondary);
}

.debug-value {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 0.5em;
  font-family: monospace;
  white-space: pre-wrap;
  word-break: break-all;
}

.form-custom-input {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.6rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

/* 进度信息区样式 */
.progress-info {
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  margin: 1.5rem;
  padding: 1rem;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.progress-stage {
  color: var(--primary-color);
  font-weight: bold;
  margin-bottom: 0.8rem;
  text-align: center;
}

.progress-bar {
  height: 8px;
  background-color: var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--primary-color);
  transition: width 0.3s ease;
}

/* 预览与编辑区域样式 */
.preview-layout {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.preview-title {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  color: var(--text-primary);
}

.edit-section-right .form-group {
  margin-bottom: 1.5rem;
}

.edit-section-right .form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.edit-section-right .form-input,
.edit-section-right .form-textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.edit-section-right .form-textarea {
  resize: vertical;
  min-height: 150px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.image-card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-container {
  height: 200px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-info {
  padding: 1rem;
}

.image-title {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
  color: #333;
}

.image-description {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.preview-btn-container {
  margin-top: 1rem;
  text-align: center;
}

.preview-btn {
  width: 100%;
  padding: 0.6rem 1.2rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}

.preview-btn:hover {
  background: var(--primary-color-dark, #0056b3);
}

.preview-loading {
  text-align: center;
  margin-bottom: 1rem;
}

.preview-error {
  text-align: center;
  color: red;
  margin-bottom: 1rem;
}

.no-images {
  text-align: center;
  margin-top: 1rem;
}

.carousel-wrapper {
  display: flex;
  justify-content: center;
  margin: 2rem auto;
  max-width: 375px;
}

.publish-btn {
  width: 100%;
  padding: 0.6rem 1.2rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
  margin-top: 1rem;
}

.publish-btn:hover {
  background: var(--primary-color-dark, #0056b3);
}

.mode-toggle {
  display: flex;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  overflow: hidden;
}

.mode-toggle button {
  flex: 1;
  padding: 0.6rem;
  border: none;
  background-color: transparent;
  cursor: pointer;
  color: var(--text-secondary);
  transition: all 0.2s;
}

.mode-toggle button.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
  font-weight: 500;
}

.secondary-btn {
  width: 100%;
  padding: 0.6rem 1.2rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
  color: var(--text-primary);
  font-size: 1rem;
}

.secondary-btn:hover {
  border-color: var(--primary-color);
}

.form-textarea.mt-2 {
  margin-top: 1rem;
}

.publish-message {
  margin-top: 1rem;
  padding: 0.8rem;
  border-radius: 4px;
  text-align: center;
}

.publish-message.success {
  background-color: #dff0d8;
  color: #3c763d;
  border: 1px solid #d6e9c6;
}

.publish-message.error {
  background-color: #f2dede;
  color: #a94442;
  border: 1px solid #ebccd1;
}

/* 美化编辑区域样式 */
.editor-card {
  background-color: var(--bg-color);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.editor-title {
  font-size: 1.6rem;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
  font-weight: 600;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 0.8rem;
}

.label-icon {
  margin-right: 0.5rem;
  font-size: 1.1rem;
}

.edit-section-right .form-group label {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.7rem;
}

.edit-section-right .form-input,
.edit-section-right .form-textarea {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--bg-color);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.2s ease;
}

.edit-section-right .form-input:focus,
.edit-section-right .form-textarea:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
  outline: none;
}

.edit-section-right .form-textarea {
  resize: vertical;
  min-height: 150px;
  line-height: 1.5;
}

.textarea-counter {
  text-align: right;
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-top: 0.3rem;
}

.tags-input-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tags-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tag-pill {
  display: inline-block;
  background: var(--primary-light);
  color: var(--primary-color);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.publish-btn {
  width: 100%;
  padding: 1rem 1.2rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1.5rem;
}

.btn-icon {
  margin-right: 0.6rem;
}

.publish-btn:hover {
  background: var(--primary-color-dark, #0056b3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.publish-btn:disabled {
  opacity: 0.7;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.publish-message {
  margin-top: 1.2rem;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease;
}

.message-icon {
  margin-right: 0.6rem;
  font-size: 1.2rem;
}

.publish-message.success {
  background-color: rgba(223, 240, 216, 0.6);
  color: #3c763d;
  border: 1px solid #d6e9c6;
}

.publish-message.error {
  background-color: rgba(242, 222, 222, 0.6);
  color: #a94442;
  border: 1px solid #ebccd1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .preview-layout {
    grid-template-columns: 1fr;
  }

  .edit-section-right {
    margin-top: 2rem;
  }
}

.model-loading {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.model-error {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #dc3545;
}
</style>
