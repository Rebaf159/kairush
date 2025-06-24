<template>
  <div class="min-h-screen flex bg-dark-900">
    <!-- Sidebar -->
    <div class="w-64 glass-dark border-r border-white/10 flex flex-col">
      <!-- Logo -->
      <div class="p-6 border-b border-white/10">
        <h1 class="text-2xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">
          KAI Rush
        </h1>
      </div>
      
      <!-- User Info -->
      <div class="p-6 border-b border-white/10" v-if="authStore.user">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
            <span class="text-white font-semibold text-sm">
              {{ authStore.user.email?.charAt(0).toUpperCase() }}
            </span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-white font-medium truncate">
              {{ authStore.user.email }}
            </p>
            <p class="text-primary-400 text-sm">
              Krediler: {{ authStore.user.credits || 100 }}
            </p>
          </div>
        </div>
      </div>
      
      <!-- Navigation -->
      <nav class="flex-1 p-6">
        <ul class="space-y-2">
          <li>
            <router-link
              to="/app/dashboard"
              class="nav-link"
              :class="{ 'nav-link-active': $route.name === 'Dashboard' }"
            >
              <HomeIcon class="w-5 h-5" />
              Dashboard
            </router-link>
          </li>
          <li>
            <router-link
              to="/app/create"
              class="nav-link"
              :class="{ 'nav-link-active': $route.name === 'Creation' }"
            >
              <PlusIcon class="w-5 h-5" />
              Yeni Karakter
            </router-link>
          </li>
          <li>
            <router-link
              to="/app/characters"
              class="nav-link"
              :class="{ 'nav-link-active': $route.name === 'Characters' }"
            >
              <UserGroupIcon class="w-5 h-5" />
              Karakterlerim
            </router-link>
          </li>
          <li>
            <router-link
              to="/app/profile"
              class="nav-link"
              :class="{ 'nav-link-active': $route.name === 'Profile' }"
            >
              <UserIcon class="w-5 h-5" />
              Profil
            </router-link>
          </li>
        </ul>
      </nav>
      
      <!-- Logout Button -->
      <div class="p-6 border-t border-white/10">
        <button
          @click="handleLogout"
          class="w-full flex items-center space-x-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-300"
        >
          <ArrowRightOnRectangleIcon class="w-5 h-5" />
          <span>Çıkış Yap</span>
        </button>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="glass-dark border-b border-white/10 px-6 py-4">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold text-white">
            {{ getPageTitle() }}
          </h2>
          
          <!-- Quick Actions -->
          <div class="flex items-center space-x-4">
            <!-- Notifications -->
            <button class="p-2 text-gray-400 hover:text-white transition-colors duration-300">
              <BellIcon class="w-5 h-5" />
            </button>
            
            <!-- Settings -->
            <button class="p-2 text-gray-400 hover:text-white transition-colors duration-300">
              <Cog6ToothIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>
      
      <!-- Page Content -->
      <main class="flex-1 overflow-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { 
  HomeIcon, 
  PlusIcon, 
  UserGroupIcon, 
  UserIcon,
  ArrowRightOnRectangleIcon,
  BellIcon,
  Cog6ToothIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const route = useRoute()

const handleLogout = () => {
  authStore.logout()
}

const getPageTitle = () => {
  const titles = {
    'Dashboard': 'Dashboard',
    'Creation': 'Yeni Karakter Yarat',
    'Characters': 'Karakterlerim',
    'Chat': 'Sohbet',
    'Profile': 'Profil Ayarları'
  }
  return titles[route.name] || 'KAI Rush'
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center space-x-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-300;
}

.nav-link-active {
  @apply text-white bg-gradient-to-r from-primary-500/20 to-accent-500/20 border border-primary-500/30;
}
</style>