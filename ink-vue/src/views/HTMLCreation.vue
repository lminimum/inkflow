<template>
  <div class="html-creation-container">
    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧预览区 -->
      <div class="display-section">
        <div class="display-header">
          <h2>HTML预览</h2>
          <div class="display-actions">
            <button class="action-btn" @click="copyHtml">
              <CopyOutlined /> 复制HTML
            </button>
            <button class="action-btn" @click="previewInNewTab">
              <EyeOutlined /> 新窗口预览
            </button>
            <button class="action-btn"><ExportOutlined /> 导出</button>
          </div>
        </div>
        <div
          class="display-content"
          v-if="generatedHtml"
          v-html="generatedHtml"
        ></div>
        <p v-else class="empty-hint">生成的HTML将显示在这里...</p>
      </div>

      <!-- 右侧表单区 -->
      <div class="form-section">
        <div class="form-header">
          <h3>HTML生成参数</h3>
        </div>
        <div class="form-content">
          <form @submit.prevent="handleGenerateHtml">
            <div class="form-group">
              <label for="theme">主题</label>
              <input
                type="text"
                id="theme"
                v-model="formData.theme"
                required
                placeholder="输入主题"
              />
            </div>
            <div class="form-group">
              <label for="style">风格</label>
              <select
                id="style"
                v-model="formData.style"
                required
                class="form-select"
              >
                <option value="">请选择风格</option>
                <option
                  v-for="option in styleOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="audience">受众</label>
              <select
                id="audience"
                v-model="formData.audience"
                required
                class="form-select"
              >
                <option value="">请选择受众</option>
                <option
                  v-for="option in audienceOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </div>
            <button type="submit" class="generate-btn" :disabled="isGenerating">
              <template v-if="isGenerating">生成中...</template>
              <template v-else>生成HTML</template>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
// import { generateHtml } from "../api/htmlGenerate"; // 移除旧的导入
import { 
  generateTitle, 
  generateCss, 
  generateContent, 
  splitContentIntoSections, 
  generateSectionHtml, 
  // buildFinalHtml, // 移除未使用的导入
  type HTMLGenerateParams, // 导入需要的类型
  type ContentRequestParams,
  type SectionsRequestParams,
  type SectionHTMLRequestParams,
  // type BuildRequestParams // 移除未使用的导入
} from "../api/htmlGenerate"; // 导入所有需要的接口和类型
import {
  ExportOutlined,
  CopyOutlined,
  EyeOutlined,
} from "@ant-design/icons-vue";

// 表单数据
const formData = ref({
  theme: "",
  style: "",
  audience: "",
});

const styleOptions = ref([
  { value: "modern", label: "现代" },
  { value: "minimalist", label: "简约" },
  { value: "retro", label: "复古" },
  { value: "professional", label: "专业" },
  { value: "creative", label: "创意" },
]);

const audienceOptions = ref([
  { value: "children", label: "儿童" },
  { value: "teenagers", label: "青少年" },
  { value: "adults", label: "成人" },
  { value: "professionals", label: "专业人士" },
]);

// 生成状态
const generatedHtml = ref("");
const isGenerating = ref(false);

// 生成HTML (测试模式)
const handleGenerateHtml = async () => {
  // 表单验证
  if (
    !formData.value.theme ||
    !formData.value.style ||
    !formData.value.audience
  ) {
    alert("请填写所有必填字段");
    return;
  }

  isGenerating.value = true;
  generatedHtml.value = ""; // 清空之前的生成内容

  try {
    // 1. 调用生成标题接口
    console.log("开始测试生成标题接口...");
    const titleParams: HTMLGenerateParams = formData.value;
    const titleResponse = await generateTitle(titleParams);
    
    // 检查 titleResponse 和 title 属性是否存在
    if (!titleResponse || !titleResponse.title) {
      throw new Error("测试失败: 从后端获取标题失败或标题为空。");
    }
    const title = titleResponse.title;
    console.log("测试成功: 标题生成接口返回标题:", title);

    // 2. 调用生成CSS接口
    console.log("开始测试生成CSS接口...");
    const cssParams: HTMLGenerateParams = formData.value;
    const cssResponse = await generateCss(cssParams);
    
    // 检查 cssResponse 和 css_style 属性是否存在
     if (!cssResponse || !cssResponse.css_style) {
      throw new Error("测试失败: 从后端获取CSS失败或CSS为空。\n" + JSON.stringify(cssResponse));
    }
    const css_style = cssResponse.css_style;
    console.log("测试成功: CSS生成接口返回CSS样式:\n", css_style);

    // 3. 调用生成内容接口
    console.log("开始测试生成内容接口...");
    const contentParams: ContentRequestParams = {
      title: title,
      ...formData.value, // theme, style, audience
    };
    const contentResponse = await generateContent(contentParams);
    
    // 检查 contentResponse 和 content 属性是否存在
    if (!contentResponse || !contentResponse.content) {
      throw new Error("测试失败: 从后端获取内容失败或内容为空。\n" + JSON.stringify(contentResponse));
    }
    const content = contentResponse.content;
    console.log("测试成功: 内容生成接口返回内容");

    // 4. 调用内容分割接口
    console.log("开始测试内容分割接口...\n内容长度:", content.length);
    const sectionsParams: SectionsRequestParams = {
      content: content,
      num_sections: 5, // 暂时固定分割成5段，后续可以考虑用户输入或动态计算
    };
    const sectionsResponse = await splitContentIntoSections(sectionsParams);
    
    // 检查 sectionsResponse 和 sections 属性是否存在且为数组
    if (!sectionsResponse || !Array.isArray(sectionsResponse.sections) || sectionsResponse.sections.length === 0) {
       throw new Error("测试失败: 从后端分割内容失败或内容片段为空。\n" + JSON.stringify(sectionsResponse));
    }
    const textSections = sectionsResponse.sections;
    console.log("测试成功: 内容分割接口返回", textSections.length, "段内容片段");

    // 5. 遍历内容片段，调用生成单个内容区块HTML接口
    console.log("开始测试生成单个内容区块HTML接口...");
    const htmlSections: string[] = [];
    for (const section of textSections) {
      const sectionHtmlParams: SectionHTMLRequestParams = {
        title: title,
        description: section,
        css_style: css_style,
      };
      const sectionHtmlResponse = await generateSectionHtml(sectionHtmlParams);
      
      // 检查 sectionHtmlResponse 和 html 属性是否存在
      if (!sectionHtmlResponse || !sectionHtmlResponse.html) {
         console.warn("测试警告: 生成一个内容区块HTML失败或HTML为空，跳过此段。\n" + JSON.stringify(sectionHtmlResponse));
         continue; // 跳过当前片段，继续处理下一段
      }
      htmlSections.push(sectionHtmlResponse.html);
      console.log("测试成功: 生成一个内容区块HTML");
    }
    
    if (htmlSections.length === 0) {
        throw new Error("测试失败: 所有内容区块HTML生成失败或为空。");
    }
    console.log("测试成功: 所有内容区块HTML生成完成");

    // 测试模式下，不调用 buildFinalHtml
    console.log("所有API接口测试通过！请检查控制台输出确认返回数据。");
    alert("所有API接口测试通过！请检查控制台输出确认返回数据。");

  } catch (error: any) {
    console.error("API接口测试失败:", error);
    alert(`API接口测试失败: ${error.message || error}`); // 改进错误提示
  } finally {
    isGenerating.value = false;
  }
};

// 复制HTML到剪贴板
const copyHtml = () => {
  if (!generatedHtml.value) return;
  navigator.clipboard.writeText(generatedHtml.value);
  alert("HTML内容已复制到剪贴板");
};

// 在新窗口预览
const previewInNewTab = () => {
  if (!generatedHtml.value) return;
  const newWindow = window.open("", "_blank");
  if (newWindow) {
    newWindow.document.write(generatedHtml.value);
    newWindow.document.close();
  }
};
</script>

<style scoped>
.html-creation-container {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  height: calc(100vh - 108px);
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
  overflow-y: auto;
  background: white;
  color: black;
  min-height: 300px;
}

.empty-hint {
  color: var(--text-secondary);
  text-align: center;
  margin-top: 2rem;
  font-style: italic;
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
</style>
