<template>
  <a-drawer
    class="theme-settings-drawer"
    :width="300"
    :open="open"
    placement="right"
    @close="onClose"
    style="background-color: var(--bg-color)"
    :close-icon="customCloseIcon"
  >
    <template #title>
      <span style="color: var(--text-primary); font-weight: bold"
        >主题设置</span
      >
    </template>
    <div class="theme-setting-item">
      <h4>主题模式</h4>
      <a-radio-group v-model:value="themeMode" @change="handleThemeModeChange">
        <a-radio value="light">浅色</a-radio>
        <a-radio value="dark">深色</a-radio>
      </a-radio-group>
    </div>

    <div class="theme-setting-item">
      <h4>主色调</h4>
      <div class="color-options">
        <div
          v-for="option in colorOptions"
          :key="option.value"
          class="color-option"
          :style="{ backgroundColor: option.value }"
          :class="{ selected: primaryColor === option.value }"
          @click="handlePrimaryColorChange(option.value)"
          :title="option.name"
        ></div>
      </div>
    </div>

    <template #extra>
      <a-button
        @click="resetDefault"
        style="color: var(--text-primary); background-color: var(--bg-color)"
        >重置默认</a-button
      >
    </template>
  </a-drawer>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { message } from "ant-design-vue";
import { CloseOutlined } from "@ant-design/icons-vue";

import { h } from "vue";
const customCloseIcon = h(CloseOutlined, {
  style: { color: "var(--text-primary)", fontSize: "18px" },
});
// 预设主题颜色选项
const colorOptions = [
  { value: "#1677ff", name: "蓝色" },
  { value: "#f5222d", name: "红色" },
  { value: "#fa8c16", name: "橙色" },
  { value: "#faad14", name: "黄色" },
  { value: "#52c41a", name: "绿色" },
  { value: "#1890ff", name: "亮蓝" },
  { value: "#722ed1", name: "紫色" },
  { value: "#eb2f96", name: "粉色" },
  { value: "#000000", name: "黑色" },
  { value: "#8c8c8c", name: "灰色" },
  { value: "#13c2c2", name: "青色" },
  { value: "#fa8c8f", name: "浅粉" },
];

// 颜色处理工具函数
const getHoverColor = (color: string) => {
  // 将十六进制颜色转换为RGB
  const r = parseInt(color.slice(1, 3), 16);
  const g = parseInt(color.slice(3, 5), 16);
  const b = parseInt(color.slice(5, 7), 16);

  // 将RGB转换为HSL
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0,
    s,
    l = (max + min) / 2 / 255;

  if (max === min) {
    h = s = 0; // 灰色
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0);
        break;
      case g:
        h = (b - r) / d + 2;
        break;
      case b:
        h = (r - g) / d + 4;
        break;
    }
    h /= 6;
  }

  // 降低亮度10%作为hover颜色
  l = Math.max(0, Math.min(1, l - 0.1));

  // 将HSL转换回十六进制
  const hue2rgb = (p: number, q: number, t: number) => {
    if (t < 0) t += 1;
    if (t > 1) t -= 1;
    if (t < 1 / 6) return p + (q - p) * 6 * t;
    if (t < 1 / 2) return q;
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
    return p;
  };

  let r2, g2, b2;
  if (s === 0) {
    r2 = g2 = b2 = l; // 灰色
  } else {
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r2 = hue2rgb(p, q, h + 1 / 3);
    g2 = hue2rgb(p, q, h);
    b2 = hue2rgb(p, q, h - 1 / 3);
  }

  return `#${Math.round(r2 * 255)
    .toString(16)
    .padStart(2, "0")}${Math.round(g2 * 255)
    .toString(16)
    .padStart(2, "0")}${Math.round(b2 * 255)
    .toString(16)
    .padStart(2, "0")}`;
};

defineProps<{
  open: boolean;
  onClose: () => void;
}>();

// 主题状态
const themeMode = ref<"light" | "dark">("light");
const primaryColor = ref<string>("#1677ff");
const primaryHoverColor = ref<string>("");

// 初始化主题设置
onMounted(() => {
  const savedTheme = localStorage.getItem("themeSettings");
  if (savedTheme) {
    const parsed = JSON.parse(savedTheme);
    themeMode.value = parsed.themeMode || "light";
    primaryColor.value = parsed.primaryColor || "#1677ff";
    primaryHoverColor.value = getHoverColor(primaryColor.value);
    applyThemeSettings();
  } else {
    primaryHoverColor.value = getHoverColor(primaryColor.value);
  }
});

// 应用主题设置到CSS变量
const applyThemeSettings = () => {
  document.documentElement.style.setProperty(
    "--primary-color",
    primaryColor.value
  );
  document.documentElement.style.setProperty(
    "--primary-hover",
    primaryHoverColor.value
  );
  document.documentElement.setAttribute("data-theme", themeMode.value);
};

// 处理主题模式变更
const handleThemeModeChange = () => {
  applyThemeSettings();
  saveThemeSettings();
};

// 处理主色调变更
const handlePrimaryColorChange = (color: string) => {
  primaryColor.value = color;
  primaryHoverColor.value = getHoverColor(color);
  applyThemeSettings();
  saveThemeSettings();
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
  primaryHoverColor.value = getHoverColor("#1677ff");
  applyThemeSettings();
  saveThemeSettings();
};
</script>

<style scoped>
:deep(.ant-radio-wrapper),
:deep(.theme-setting-item h4) {
  color: var(--text-primary) !important;
}

.theme-settings-drawer.ant-drawer
  .ant-drawer-header
  .ant-drawer-header-title
  h4.ant-drawer-title {
  color: var(--text-primary) !important;
}

.theme-setting-item {
  margin-bottom: 24px;
}

.theme-setting-item h4 {
  margin-bottom: 12px;
  font-size: 14px;
}

.color-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 8px;
}

.color-option {
  --option-width: 50px;
  width: var(--option-width);
  height: var(--option-width);
  border-radius: 25%;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid transparent;
}

.color-option.selected {
  transform: scale(1.15);
  box-shadow: 0 0 0 2px white, 0 0 0 4px var(--primary-color);
  border-color: #fff;
}

.color-option:hover:not(.selected) {
  transform: scale(1.05);
  box-shadow: 0 0 0 2px white, 0 0 0 3px #ddd;
}
</style>
