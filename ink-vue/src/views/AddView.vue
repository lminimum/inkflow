<template>
  <div class="ink-container">
    <h1 class="title">墨迹添新</h1>
    <div class="ink-drop">
      <!-- 这里放置添加内容表单 -->
    </div>
  </div>
</template>

<style scoped>
.ink-drop {
  background: url('data:image/svg+xml;utf8,<svg...></svg>');
  animation: ink-spread 1.5s ease-in-out;
}
@keyframes ink-spread {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
</style>