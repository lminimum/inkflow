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
      <!-- 左侧输入区 -->
      <div class="input-section">
        <div class="input-group">
          <label>请输入文章标题（2~30个字）</label>
          <input type="text" placeholder="请输入文章标题" class="title-input" />
          <span class="char-count">0/30</span>
        </div>

        <div class="input-group">
          <label>请输入创作主题、观点</label>
          <textarea
            placeholder="请输入创作主题、观点..."
            class="content-input"
          ></textarea>
          <span class="char-count">0/500</span>
        </div>
      </div>

      <!-- 右侧设置区 -->
      <div class="settings-section">
        <div class="model-selector">
          <label>模型选择</label>
          <select class="model-select">
            <option>DeepSeek-R1</option>
            <option>其他模型1</option>
            <option>其他模型2</option>
          </select>
        </div>

        <div class="setting-group">
          <label>风格</label>
          <select class="style-select">
            <option>不限定类型</option>
            <option>正式</option>
            <option>轻松</option>
            <option>专业</option>
          </select>
        </div>

        <div class="setting-group">
          <label>用词</label>
          <select class="wording-select">
            <option>不限定风格</option>
            <option>通俗</option>
            <option>华丽</option>
            <option>简洁</option>
          </select>
        </div>

        <div class="setting-group">
          <label>字数</label>
          <select class="word-count-select">
            <option>1000字以内</option>
            <option>1000-2000字</option>
            <option>2000-3000字</option>
            <option>3000字以上</option>
          </select>
        </div>

        <button class="generate-btn">开始创作</button>
      </div>
    </div>

    <!-- 底部操作栏 -->
    <div class="bottom-actions">
      <button class="action-btn">实时全文</button>
      <button class="action-btn">存草稿</button>
      <button class="action-btn">预览</button>
      <button class="primary-btn">生成原创内容</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

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
const switchTab = (index) => (activeTab.value = index);
</script>

<style scoped>
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
