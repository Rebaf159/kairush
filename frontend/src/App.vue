<template>
  <div id="app" class="min-h-screen bg-gradient-primary animate-gradient">
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Uygulama başlatıldığında token kontrolü yap
onMounted(() => {
  authStore.initializeAuth()
})
</script>

<style>
/* Global styles are in assets/main.css */
</style>