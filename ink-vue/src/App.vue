<script setup lang="ts">
// import { useRouter } from 'vue-router';
// const router = useRouter();
</script>

<template>
  <div class="layout-container">
    <nav class="sidebar-menu">
        <router-link to="/" class="menu-item" active-class="active-menu" exact>
          <home-outlined :style="{fontSize: '24px', color: '#595959'}"/>
        </router-link>
        <router-link to="/ai-creation" class="menu-item" title="AI创作" active-class="active-menu">
          <edit-outlined :style="{fontSize: '24px', color: '#595959'}"/>
        </router-link>
      <router-link to="/add" class="menu-item" title="添加" active-class="active-menu">
        <plus-outlined :style="{fontSize: '24px', color: '#595959'}"/>
      </router-link>
    </nav>
    <div class="main-content">
      <router-view/>
    </div>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
