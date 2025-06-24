<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="max-w-4xl mx-auto text-center">
      <!-- Hero Section -->
      <div class="mb-12">
        <!-- Logo -->
        <h1 class="text-6xl md:text-8xl font-bold mb-6">
          <span class="bg-gradient-to-r from-primary-400 via-accent-400 to-secondary-400 bg-clip-text text-transparent animate-gradient">
            KAI Rush
          </span>
        </h1>
        
        <!-- Tagline -->
        <h2 class="text-2xl md:text-4xl font-semibold text-white mb-4">
          Hayalindeki Yoldaşı Yarat
        </h2>
        
        <!-- Description -->
        <p class="text-lg md:text-xl text-gray-300 mb-8 max-w-2xl mx-auto leading-relaxed">
          Yapay zeka teknolojisiyle kendi kişisel yoldaşını tasarla. 
          Benzersiz kişilik, görünüm ve hikayeyle donatılmış AI karakterinle 
          sınırsız sohbet deneyimi yaşa.
        </p>
      </div>
      
      <!-- CTA Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
        <router-link 
          to="/auth/register" 
          class="btn-primary text-lg px-8 py-4 min-w-[200px]"
        >
          <SparklesIcon class="w-6 h-6 mr-2" />
          Hemen Başla
        </router-link>
        
        <router-link 
          to="/auth/login" 
          class="btn-ghost text-lg px-8 py-4 min-w-[200px]"
        >
          <ArrowRightOnRectangleIcon class="w-6 h-6 mr-2" />
          Giriş Yap
        </router-link>
      </div>
      
      <!-- Features -->
      <div class="grid md:grid-cols-3 gap-8 mb-16">
        <div class="card text-center group">
          <div class="w-16 h-16 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
            <UserPlusIcon class="w-8 h-8 text-white" />
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Kolay Yaratım</h3>
          <p class="text-gray-400">
            Sadece birkaç kelimeyle karakterinin kişiliğini, görünümünü ve hikayesini tanımla.
          </p>
        </div>
        
        <div class="card text-center group">
          <div class="w-16 h-16 bg-gradient-to-r from-secondary-500 to-secondary-600 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
            <ChatBubbleLeftRightIcon class="w-8 h-8 text-white" />
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Akıllı Sohbet</h3>
          <p class="text-gray-400">
            Gelişmiş AI teknolojisiyle doğal, akıcı ve kişiselleştirilmiş konuşmalar yap.
          </p>
        </div>
        
        <div class="card text-center group">
          <div class="w-16 h-16 bg-gradient-to-r from-accent-500 to-accent-600 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
            <HeartIcon class="w-8 h-8 text-white" />
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Duygusal Bağ</h3>
          <p class="text-gray-400">
            Karakterin seninle olan her sohbeti hatırlar ve zamanla daha da yakınlaşır.
          </p>
        </div>
      </div>
      
      <!-- Stats -->
      <div class="glass-dark rounded-2xl p-8 mb-16">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-3xl font-bold text-primary-400 mb-2">10K+</div>
            <div class="text-gray-400">Yaratılan Karakter</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-secondary-400 mb-2">1M+</div>
            <div class="text-gray-400">Sohbet Mesajı</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-400 mb-2">5K+</div>
            <div class="text-gray-400">Aktif Kullanıcı</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-primary-400 mb-2">99%</div>
            <div class="text-gray-400">Memnuniyet</div>
          </div>
        </div>
      </div>
      
      <!-- Footer -->
      <div class="text-center text-gray-500">
        <p>&copy; 2024 KAI Rush. Tüm hakları saklıdır.</p>
      </div>
    </div>
    
    <!-- Floating Elements -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-primary-500/10 rounded-full blur-3xl animate-float"></div>
      <div class="absolute top-3/4 right-1/4 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl animate-float" style="animation-delay: -2s;"></div>
      <div class="absolute top-1/2 left-3/4 w-48 h-48 bg-secondary-500/10 rounded-full blur-3xl animate-float" style="animation-delay: -4s;"></div>
    </div>
  </div>
</template>

<script setup>
import { 
  SparklesIcon, 
  ArrowRightOnRectangleIcon,
  UserPlusIcon,
  ChatBubbleLeftRightIcon,
  HeartIcon
} from '@heroicons/vue/24/outline'
</script>

<style scoped>
@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-20px) rotate(1deg);
  }
  66% {
    transform: translateY(10px) rotate(-1deg);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}
</style>