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
import { generateHtml } from "../api/htmlGenerate";
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

// 生成HTML
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
  try {
    const response = await generateHtml(formData.value);
    generatedHtml.value = response.html; // 提取html属性
  } catch (error: any) {
    console.error("生成HTML失败:", error);
    alert(`生成失败: ${error.message}`);
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
