<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12">
    <div class="max-w-md w-full">
      <!-- Logo ve Başlık -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent mb-2">
          KAI Rush
        </h1>
        <p class="text-gray-400 text-lg">
          Hayalindeki Yoldaşı Yarat
        </p>
      </div>
      
      <!-- Auth Form Container -->
      <div class="glass-dark rounded-2xl p-8 shadow-2xl">
        <router-view />
      </div>
      
      <!-- Alt Navigasyon -->
      <div class="text-center mt-6">
        <router-link 
          v-if="$route.name === 'Login'"
          to="/auth/register" 
          class="text-primary-400 hover:text-primary-300 transition-colors duration-300"
        >
          Hesabın yok mu? Kayıt ol
        </router-link>
        <router-link 
          v-else-if="$route.name === 'Register'"
          to="/auth/login" 
          class="text-primary-400 hover:text-primary-300 transition-colors duration-300"
        >
          Zaten hesabın var mı? Giriş yap
        </router-link>
      </div>
      
      <!-- Ana Sayfaya Dön -->
      <div class="text-center mt-4">
        <router-link 
          to="/" 
          class="text-gray-400 hover:text-white transition-colors duration-300 text-sm"
        >
          ← Ana Sayfaya Dön
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
// Bu layout giriş ve kayıt sayfaları için kullanılır
</script>