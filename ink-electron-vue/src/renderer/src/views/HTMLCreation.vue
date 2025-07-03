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
          <form @submit.prevent="handleGenerateHtml">
            <div class="form-group">
              <label for="theme">主题</label>
              <input
                id="theme"
                v-model="formData.theme"
                type="text"
                required
                placeholder="输入主题"
              />
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
            <button type="submit" class="generate-btn" :disabled="isGenerating">
              <template v-if="isGenerating">生成中...</template>
              <template v-else>生成HTML</template>
            </button>
          </form>
        </div>
        <!-- 调试信息区 -->
        <div class="debug-info">
          <h4>生成信息</h4>
          <div v-if="currentStage" class="debug-stage">当前阶段：{{ currentStage }}</div>
          <div
            v-for="(item, idx) in debugResults.filter(
              (i) => i.label !== 'CSS' && i.label !== '区块HTML' && i.label !== '最终HTML'
            )"
            :key="idx"
            class="debug-result"
          >
            <div class="debug-label">{{ item.label }}：</div>
            <pre class="debug-value">{{ item.value }}</pre>
          </div>
          <div
            v-for="(item, idx) in debugResults.filter(
              (i) => i.label === '区块HTML' || i.label === '最终HTML'
            )"
            :key="'html-' + idx"
            class="debug-result"
          >
            <div class="debug-label">{{ item.label }}：</div>
            <pre class="debug-value">已生成</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { storeToRefs } from 'pinia'
import { useHtmlStore } from '../store/htmlStore'
import HtmlSectionPager from '../components/HtmlSectionPager.vue'
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

// 表单数据
const formData = ref({
  theme: '',
  style: '',
  audience: '',
  numSections: 1,
  customStyle: '',
  customAudience: ''
})

const styleOptions = ref([
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
const { htmlSections } = storeToRefs(htmlStore)

// 用于存储完整的HTML，用于复制和预览
const fullGeneratedHtml = ref('')

// 调试信息相关
const currentStage = ref('')
const debugResults = reactive<Array<{ label: string; value: string }>>([])

// 生成HTML
const handleGenerateHtml = async (): Promise<void> => {
  // 表单验证
  if (!formData.value.theme || !formData.value.style || !formData.value.audience) {
    alert('请填写所有必填字段')
    return
  }
  // 处理自定义风格/受众
  let style = formData.value.style === 'custom' ? formData.value.customStyle : formData.value.style
  let audience =
    formData.value.audience === 'custom' ? formData.value.customAudience : formData.value.audience

  isGenerating.value = true
  htmlStore.clearHtml()
  fullGeneratedHtml.value = ''
  debugResults.length = 0
  currentStage.value = '正在生成标题'
  try {
    // 1. 调用生成标题接口
    const titleParams: HTMLGenerateParams = {
      ...formData.value,
      style,
      audience
    }
    const titleResponse = await generateTitle(titleParams)
    if (!titleResponse || !titleResponse.title) {
      throw new Error('从后端获取标题失败或标题为空。')
    }
    const title = titleResponse.title
    debugResults.push({ label: '标题', value: title })
    currentStage.value = '正在生成CSS'

    // 2. 调用生成CSS接口
    const cssParams: HTMLGenerateParams = {
      ...formData.value,
      style,
      audience
    }
    const cssResponse = await generateCss(cssParams)
    if (!cssResponse || !cssResponse.css_style) {
      throw new Error('从后端获取CSS失败或CSS为空。')
    }
    const css_style = cssResponse.css_style
    currentStage.value = '正在生成内容'

    // 3. 调用生成内容接口
    const contentParams: ContentRequestParams = {
      title: title,
      theme: formData.value.theme,
      style,
      audience
    }
    const contentResponse = await generateContent(contentParams)
    if (!contentResponse || !contentResponse.content) {
      throw new Error('从后端获取内容失败或内容为空。')
    }
    const content = contentResponse.content
    debugResults.push({ label: '主内容', value: content })
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
    debugResults.push({ label: '分段内容', value: JSON.stringify(textSections, null, 2) })
    currentStage.value = '正在生成内容区块HTML'

    // 5. 遍历内容片段，调用生成单个内容区块HTML接口
    let sectionHtmlArr: string[] = []
    for (const section of textSections) {
      const sectionHtmlParams: SectionHTMLRequestParams = {
        title: title,
        description: section,
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
      } catch (err) {
        sectionHtmlArr.push('生成失败' + err)
      }
    }
    if (htmlStore.htmlSections.length === 0) {
      throw new Error('所有内容区块HTML生成失败或为空。')
    }
    debugResults.push({ label: '区块HTML', value: sectionHtmlArr.join('\n\n') })
    currentStage.value = '正在构建最终HTML'

    isGenerating.value = false
    debugResults.push({ label: '最终HTML', value: '已生成' })
    currentStage.value = ''
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error)
    alert(`生成失败: ${message}`)
    isGenerating.value = false
    currentStage.value = ''
  }
}

// 页面初始化时恢复内容 (如果需要)
onMounted(() => {
  // 目前不实现恢复功能，每次进入页面清空
  htmlStore.clearHtml()
  fullGeneratedHtml.value = ''
})
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
</style>
