<template>
  <div class="ai-creation-container">
    <!-- 顶部导航 -->
    <div class="top-nav">
      <div class="nav-tabs">
        <div class="tab active">AI创作</div>
        <div class="tab">AI改写</div>
      </div>
      <div class="toolbar">
        <button class="toolbar-btn"><i class="icon-save"></i> 保存</button>
        <button class="toolbar-btn"><i class="icon-export"></i> 导出</button>
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
              <i class="icon-copy"></i> 复制
            </button>
            <button class="action-btn" @click="editContent">
              <i class="icon-edit"></i> 编辑
            </button>
          </div>
        </div>
        <div
          class="display-content"
          v-if="generatedContent"
          v-html="generatedContent"
        ></div>
        <p v-else class="empty-hint">AI生成的内容将显示在这里...</p>
        >
      </div>

      <!-- 右侧AI对话区 -->
      <div class="chat-section">
        <div class="chat-header">
          <h3>AI助手</h3>
          <button class="clear-btn" @click="clearChat">
            <i class="icon-clear"></i>
          </button>
        </div>
        <div class="chat-messages">
          <div
            class="message ai-message"
            v-for="(msg, index) in messages"
            :key="index"
          >
            <div class="message-avatar"><i class="icon-ai"></i></div>
            <div class="message-content">{{ msg.content }}</div>
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
            <i class="icon-send"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { generateContent } from "../api/generate";

// 生成内容状态
const generatedTitle = ref("");
const generatedContent = ref("");
const isGenerating = ref(false);

// 对话状态
const messages = ref([
  {
    content:
      "您好！我可以帮您创作内容。请告诉我您的主题或需求，我会生成相应的文本并可以根据您的反馈进行修改。",
  },
]);
const userInput = ref("");

const handleGenerate = async () => {
  isGenerating.value = true;
  const response = await generateContent(userInput.value);
  // 更新生成内容和AI回复
  generatedContent.value = response.content;
  // if (response.title) generatedTitle.value = response.title;
  // if (response.content) generatedContent.value = response.content;
  // 假设实际属性名可能需要根据 GenerateResponse 类型调整，这里假设正确属性名为 aiResponse
  if (response.content) {
    messages.value.push({ content: response.content });
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
  height: 100vh;
  display: flex;
  flex-direction: column;
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
.display-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background: white;
  line-height: 1.6;
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
.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: var(--bg-color);
}
.message {
  display: flex;
  gap: 0.8rem;
  max-width: 85%;
}
.ai-message {
  align-self: flex-start;
}
.user-message {
  align-self: flex-end;
  flex-direction: row-reverse;
}
.message-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.user-message .message-avatar {
  background: var(--secondary-color);
}
.message-content {
  padding: 0.8rem 1.2rem;
  border-radius: 18px;
  background: white;
  border: 1px solid var(--border-color);
}
.user-message .message-content {
  background: var(--primary-light);
  color: var(--primary-color);
  border-color: var(--primary-color);
}
.chat-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid var(--border-color);
}
.chat-input textarea {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  resize: none;
  min-height: 4rem;
  max-height: 10rem;
}
.send-btn {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: var(--primary-color);
  color: white;
  border: none;
  cursor: pointer;
  align-self: flex-end;
}
.send-btn:disabled {
  background: var(--border-color);
  cursor: not-allowed;
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

/* 响应式调整 */
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}
.ai-creation-container {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
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
}

/* 主内容区 */
.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

/* 输入区样式 */
.input-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
label {
  font-size: 0.9rem;
  color: var(--text-secondary);
}
.title-input {
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
}
.content-input {
  min-height: 200px;
  padding: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  resize: vertical;
}
.char-count {
  align-self: flex-end;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

/* 设置区样式 */
.settings-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
}
.setting-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
select {
  padding: 0.6rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: white;
}
.generate-btn {
  padding: 0.8rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

/* 底部操作栏 */
.bottom-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}
.action-btn {
  padding: 0.6rem 1.2rem;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
}
.primary-btn {
  padding: 0.6rem 1.2rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  .bottom-actions {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
