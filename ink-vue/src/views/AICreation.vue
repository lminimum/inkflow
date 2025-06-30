<template>
  <div class="ai-creation-container">
    <!-- 顶部导航 -->
    <div class="top-nav">
      <div class="nav-tabs">
        <div class="tab active">AI创作</div>
        <div class="tab">AI改写</div>
      </div>
      <div class="toolbar">
        <button class="toolbar-btn"><SaveOutlined /> 保存</button>
        <button class="toolbar-btn"><ExportOutlined /> 导出</button>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 左侧展示界面 -->
      <div class="display-section">
        <div class="display-header">
          <h2>{{ generatedTitle || "生成内容预览" }}</h2>
          <div class="display-actions">
            <button class="action-btn" @click="copyContent">
              <CopyOutlined /> 复制
            </button>
            <button class="action-btn" @click="editContent">
              <EditOutlined /> 编辑
            </button>
          </div>
        </div>
        <div
          class="display-content markdown-content"
          v-if="generatedContent"
          v-html="generatedContent"
        ></div>
        <p v-else class="empty-hint">AI生成的内容将显示在这里...</p>
      </div>

      <!-- 右侧AI对话区 -->
      <div class="chat-section">
        <div class="chat-header">
          <h3>AI助手</h3>
          <div class="model-selector">
            <select v-model="selectedModel" class="model-select">
              <option
                v-for="model in modelsStore.modelOptions"
                :key="model.value"
                :value="model.value"
              >
                {{ model.label }}
              </option>
            </select>
          </div>
          <button class="clear-btn" @click="clearChat">
            <ClearOutlined />
          </button>
        </div>
        <div class="chat-messages">
          <div
            :class="[
              'message',
              msg.role === 'user' ? 'user-message' : 'ai-message',
            ]"
            v-for="(msg, index) in messages"
            :key="index"
          >
            <div class="message-avatar">
              <component
                :is="msg.role === 'user' ? UserOutlined : RobotOutlined"
              />
            </div>
            <div
              class="message-content markdown-content"
              v-html="parseMarkdown(msg.content)"
            ></div>
          </div>
          <div class="typing-indicator" v-if="isGenerating">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
          </div>
        </div>
        <div class="chat-input">
          <textarea
            v-model="userInput"
            placeholder="请输入您的创作需求或问题..."
            @keydown.enter.prevent="handleGenerate"
          ></textarea>
          <button
            class="send-btn"
            @click="handleGenerate"
            :disabled="!userInput.trim() || isGenerating"
          >
            <SendOutlined />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useModelsStore } from "../store/modelsStore";
import type { Message } from "../types";
import { generateContent } from "../api/generate";
import { marked } from "marked";
import {
  UserOutlined,
  RobotOutlined,
  SendOutlined,
  SaveOutlined,
  ExportOutlined,
  CopyOutlined,
  EditOutlined,
  ClearOutlined,
} from "@ant-design/icons-vue";

// Markdown解析函数
const parseMarkdown = (content: string) => {
  return marked.parse(content);
};

// 生成内容状态
const generatedTitle = ref("");
const generatedContent = ref("");
const isGenerating = ref(false);

// 对话状态
const modelsStore = useModelsStore();
const selectedModel = ref("");

onMounted(() => {
  modelsStore.loadModels().then(() => {
    // 设置默认模型
    if (modelsStore.modelOptions.length > 0) {
      selectedModel.value = modelsStore.modelOptions[0].value;
    }
  });
});

const messages = ref<Message[]>([
  {
    role: "assistant",
    content:
      "您好！我可以帮您创作内容。请告诉我您的主题或需求，我会生成相应的文本并可以根据您的反馈进行修改。",
  },
]);
const userInput = ref("");

const handleGenerate = async () => {
  if (!userInput.value.trim()) return;

  // 添加用户消息
  messages.value.push({ role: "user", content: userInput.value });
  isGenerating.value = true;

  try {
    // 查找选中模型的提供商
    const selectedOption = modelsStore.modelOptions.find(
      (option) => option.value === selectedModel.value
    );
    const provider = selectedOption?.provider || "deepseek";

    const response = await generateContent(
      [{ role: "user", content: userInput.value }],
      selectedModel.value,
      provider
    );
    // 使用marked解析Markdown内容
    generatedContent.value = await marked.parse(response.content);
    if (response.content) {
      messages.value.push({ role: "assistant", content: response.content });
    }
    userInput.value = ""; // 清空输入
  } catch (error) {
    console.error("生成内容失败:", error);
    messages.value.push({
      role: "assistant",
      content: "抱歉，生成内容时出错，请稍后再试。",
    });
  } finally {
    isGenerating.value = false;
  }
};

// 复制内容到剪贴板
const copyContent = () => {
  if (!generatedContent.value) return;
  navigator.clipboard.writeText(generatedContent.value);
  alert("内容已复制到剪贴板");
};

// 清空对话
const clearChat = () => {
  messages.value = [
    {
      role: "assistant",
      content:
        "您好！我可以帮您创作内容。请告诉我您的主题或需求，我会生成相应的文本并可以根据您的反馈进行修改。",
    },
  ];
};

// 编辑内容
const editContent = () => {
  // 可以在这里实现编辑功能
  alert("编辑功能待实现");
};

// 字数统计功能
const titleInput = ref("");
const contentInput = ref("");
const titleCount = ref(0);
const contentCount = ref(0);

// 监听输入变化更新字数统计
const updateTitleCount = () => (titleCount.value = titleInput.value.length);
const updateContentCount = () =>
  (contentCount.value = contentInput.value.length);

// 选项卡切换功能
const activeTab = ref(0);
const switchTab = (index: number) => (activeTab.value = index);
</script>

<style scoped>
.ai-creation-container {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

/* 顶部导航 */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.nav-tabs {
  display: flex;
  gap: 0.5rem;
}

.tab {
  padding: 0.5rem 1.5rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px 4px 0 0;
  cursor: pointer;
  color: var(--text-primary);
}

.tab.active {
  background: var(--primary-light);
  color: var(--primary-color);
  border-bottom-color: transparent;
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

/* 主题切换按钮 */
.theme-toggle {
  margin-left: 1rem;
}

/* 主内容区 */
.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  flex: 1;
  overflow: hidden;
}

/* 左侧展示区 */
.display-section {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
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
  background: var(--bg-color);
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

.display-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background: var(--bg-color);
  line-height: 1.6;
  color: var(--text-primary);
}

.empty-hint {
  color: var(--text-secondary);
  text-align: center;
  margin-top: 2rem;
  font-style: italic;
}

/* 右侧对话区 */
.chat-section {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--bg-color);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-color);
}

.clear-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-secondary);
}

/* 模型选择器样式 */
.model-selector {
  margin-left: 1rem;
}

.model-select {
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
  color: var(--text-primary);
}

/* 聊天消息样式 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: var(--bg-color);
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  max-width: 90%;
}

.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-message .message-avatar {
  background-color: var(--primary-light);
}

.message-content {
  padding: 0.8rem 1rem;
  border-radius: 8px;
  background-color: var(--hover-color);
  line-height: 1.5;
  color: var(--text-primary);
}

.user-message .message-content {
  background-color: var(--primary-color);
  color: white;
}

/* 打字指示器 */
.typing-indicator {
  display: flex;
  gap: 0.3rem;
  padding: 0.8rem;
}

.dot {
  width: 0.6rem;
  height: 0.6rem;
  border-radius: 50%;
  background: var(--text-secondary);
  animation: typing 1.4s infinite both;
}

.dot:nth-child(1) {
  animation-delay: 0s;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  60%,
  100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}

/* 输入区样式 */
.chat-input {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  background-color: var(--bg-color);
}

.chat-input textarea {
  flex: 1;
  border: 1px solid var(--border-color);
  border-radius: 5px;
  resize: none;
  min-height: 4rem;
  max-height: 10rem;
  font-size: 1rem;
  padding: 0.8rem;
  background-color: var(--bg-color);
  color: var(--text-primary);
}

/* 发送按钮样式 */
.send-btn {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: var(--primary-color);
  color: var(--text-primary);
  border: none;
  cursor: pointer;
}
.send-btn:disabled {
  background-color: var(--border-color);
  cursor: not-allowed;
}

/* Markdown内容样式 */
.markdown-content {
  line-height: 1.6;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin: 1.5rem 0 1rem;
  color: var(--text-primary);
}

  .main-content {
    grid-template-columns: 1fr;
.markdown-content p {
  margin-bottom: 1rem;
}

.markdown-content ul,
.markdown-content ol {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}

.markdown-content ul {
  list-style-type: disc;
}

.markdown-content ol {
  list-style-type: decimal;
}

.markdown-content strong {
  font-weight: bold;
}

.markdown-content em {
  font-style: italic;
}

.markdown-content a {
  color: var(--primary-color);
  text-decoration: underline;
}

.markdown-content img {
  max-width: 100%;
  border-radius: 4px;
  margin: 1rem 0;
}

.markdown-content code {
  background-color: var(--bg-secondary);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: monospace;
}

.markdown-content pre {
  background-color: var(--bg-secondary);
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.markdown-content blockquote {
  border-left: 4px solid var(--border-color);
  padding-left: 1rem;
  margin-left: 0;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}
</style>
