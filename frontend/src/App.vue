<template>
  <div class="app">
    <header v-if="authStore.isAuthenticated">
      <div class="header-content">
        <router-link to="/dashboard" class="logo">Nag Queen</router-link>
        <nav>
          <router-link to="/dashboard">Reminders</router-link>
          <button @click="logout" class="logout-btn">Logout</button>
        </nav>
      </div>
    </header>
    <main :class="{ 'full-width': isFullWidthRoute }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth.js'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isFullWidthRoute = computed(() => route.path === '/' || route.path === '/login')

function logout() {
  authStore.logout()
  router.push('/')
}
</script>

<style>
.app {
  min-height: 100vh;
}

header {
  background: #6366f1;
  color: white;
  padding: 1rem;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  text-decoration: none;
}

nav {
  display: flex;
  gap: 1rem;
  align-items: center;
}

nav a {
  color: white;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

main {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

main.full-width {
  max-width: none;
  padding: 0;
}
</style>
