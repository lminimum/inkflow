<template>
  <div class="html-creation-container">
    <!-- 顶部导航 -->
    <div class="top-nav">
      <div class="toolbar">
        <button class="toolbar-btn"><SaveOutlined /> 保存</button>
        <button class="toolbar-btn"><ExportOutlined /> 导出</button>
      </div>
    </div>

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
              <input
                type="text"
                id="style"
                v-model="formData.style"
                required
                placeholder="输入风格"
              />
            </div>
            <div class="form-group">
              <label for="audience">受众</label>
              <input
                type="text"
                id="audience"
                v-model="formData.audience"
                required
                placeholder="输入受众"
              />
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
  SaveOutlined,
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

// 生成状态
const generatedHtml = ref("");
const isGenerating = ref(false);

// 生成HTML
const handleGenerateHtml = async () => {
  isGenerating.value = true;
  try {
    const response = await generateHtml(formData.value);
    generatedHtml.value = response;
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
  height: calc(100vh - 60px);
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

display-section {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--bg-color);
}

display-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

display-actions {
  display: flex;
  gap: 0.5rem;
}

action-btn {
  padding: 0.6rem 1.2rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
}

display-content {
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
  border: 1px solid var(--border-color);
  border-radius: 8px;
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
  background-color: var(--bg-color);
  color: var(--text-primary);
}

generate-btn {
  width: 100%;
  padding: 0.8rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

generate-btn:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
}
</style>
