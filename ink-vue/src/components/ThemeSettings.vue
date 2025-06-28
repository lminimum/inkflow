<template>
  <a-drawer
    :width="300"
    title="主题设置"
    :open="open"
    placement="right"
    @close="onClose"
    style="background-color: var(--bg-color)"
  >
    <div class="theme-setting-item">
      <h4>主题模式</h4>
      <a-radio-group v-model:value="themeMode" @change="handleThemeModeChange">
        <a-radio value="light">浅色</a-radio>
        <a-radio value="dark">深色</a-radio>
      </a-radio-group>
    </div>

    <div class="theme-setting-item">
      <h4>主色调</h4>
      <a-color-picker
        v-model:value="primaryColor"
        @change="handlePrimaryColorChange"
        :style="{ width: '100%' }"
      />
    </div>

    <div class="theme-setting-item">
      <h4>悬停色</h4>
      <a-color-picker
        v-model:value="primaryHoverColor"
        @change="handlePrimaryHoverColorChange"
        :style="{ width: '100%' }"
      />
    </div>

    <template #extra>
      <a-button @click="resetDefault">重置默认</a-button>
      <a-button type="primary" @click="onClose" style="margin-left: 8px"
        >保存</a-button
      >
    </template>
  </a-drawer>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { message } from "ant-design-vue";

defineProps<{
  open: boolean;
  onClose: () => void;
}>();

// 主题状态
const themeMode = ref<"light" | "dark">("light");
const primaryColor = ref<string>("#1677ff");
const primaryHoverColor = ref<string>("#0050b3");

// 初始化主题设置
onMounted(() => {
  const savedTheme = localStorage.getItem("themeSettings");
  if (savedTheme) {
    const parsed = JSON.parse(savedTheme);
    themeMode.value = parsed.themeMode || "light";
    primaryColor.value = parsed.primaryColor || "#1677ff";
    primaryHoverColor.value = parsed.primaryHoverColor || "#0050b3";
    applyThemeSettings();
  }
});

// 应用主题设置到CSS变量
const applyThemeSettings = () => {
  // 设置颜色变量
  document.documentElement.style.setProperty(
    "--primary-color",
    primaryColor.value
  );
  document.documentElement.style.setProperty(
    "--primary-hover",
    primaryHoverColor.value
  );

  // 设置深色/浅色模式
  document.documentElement.setAttribute("data-theme", themeMode.value);
};

// 处理主题模式变更
const handleThemeModeChange = () => {
  applyThemeSettings();
  saveThemeSettings();
};

// 处理主色调变更
const handlePrimaryColorChange = (color: any) => {
  if (color) {
    primaryColor.value = color.toString();
    applyThemeSettings();
    saveThemeSettings();
  }
};

// 处理悬停色变更
const handlePrimaryHoverColorChange = (color: any) => {
  if (color) {
    primaryHoverColor.value = color.toString();
    applyThemeSettings();
    saveThemeSettings();
  }
};

// 保存主题设置到本地存储
const saveThemeSettings = () => {
  const settings = {
    themeMode: themeMode.value,
    primaryColor: primaryColor.value,
    primaryHoverColor: primaryHoverColor.value,
  };
  localStorage.setItem("themeSettings", JSON.stringify(settings));
  message.success("主题设置已保存");
};

// 重置默认设置
const resetDefault = () => {
  themeMode.value = "light";
  primaryColor.value = "#1677ff";
  primaryHoverColor.value = "#0050b3";
  applyThemeSettings();
  saveThemeSettings();
};
</script>

<style scoped>
.theme-setting-item {
  margin-bottom: 24px;
  color: var(--text-primary);
}

.theme-setting-item h4 {
  margin-bottom: 12px;
  font-size: 14px;
  color: var(--text-primary);
}
</style>
