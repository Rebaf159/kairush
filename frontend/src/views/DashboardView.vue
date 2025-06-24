<template>
  <div class="space-y-8">
    <!-- Welcome Section -->
    <div class="glass-dark rounded-2xl p-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-white mb-2">
            Hoş geldin, {{ authStore.user?.email?.split('@')[0] || 'Avcı' }}!
          </h1>
          <p class="text-gray-400 text-lg">
            Yoldaşlarınla sohbet etmeye hazır mısın?
          </p>
        </div>
        <div class="text-right">
          <div class="text-2xl font-bold text-primary-400 mb-1">
            {{ authStore.user?.credits || 100 }}
          </div>
          <div class="text-sm text-gray-400">Kredi</div>
        </div>
      </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="grid md:grid-cols-3 gap-6">
      <router-link 
        to="/app/create" 
        class="card group cursor-pointer border-2 border-transparent hover:border-primary-500/50 transition-all duration-300"
      >
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
            <PlusIcon class="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white group-hover:text-primary-400 transition-colors duration-300">
              Yeni Karakter
            </h3>
            <p class="text-gray-400 text-sm">Hayalindeki yoldaşı yarat</p>
          </div>
        </div>
      </router-link>
      
      <router-link 
        to="/app/characters" 
        class="card group cursor-pointer border-2 border-transparent hover:border-secondary-500/50 transition-all duration-300"
      >
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-gradient-to-r from-secondary-500 to-secondary-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
            <UserGroupIcon class="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white group-hover:text-secondary-400 transition-colors duration-300">
              Karakterlerim
            </h3>
            <p class="text-gray-400 text-sm">{{ characterStore.characters.length }} karakter</p>
          </div>
        </div>
      </router-link>
      
      <div class="card border-2 border-transparent">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-gradient-to-r from-accent-500 to-accent-600 rounded-lg flex items-center justify-center">
            <ChatBubbleLeftRightIcon class="w-6 h-6 text-white" />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white">
              Toplam Sohbet
            </h3>
            <p class="text-gray-400 text-sm">{{ totalChats }} mesaj</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Characters -->
    <div v-if="characterStore.recentCharacters.length > 0">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-white">Son Sohbet Ettiklerin</h2>
        <router-link 
          to="/app/characters" 
          class="text-primary-400 hover:text-primary-300 transition-colors duration-300 flex items-center space-x-1"
        >
          <span>Tümünü Gör</span>
          <ArrowRightIcon class="w-4 h-4" />
        </router-link>
      </div>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <CharacterCard 
          v-for="character in characterStore.recentCharacters" 
          :key="character.id"
          :character="character"
          @click="goToChat(character.id)"
        />
      </div>
    </div>
    
    <!-- Favorite Characters -->
    <div v-if="characterStore.favoriteCharacters.length > 0">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-white flex items-center space-x-2">
          <HeartIcon class="w-6 h-6 text-red-400" />
          <span>Favorilerin</span>
        </h2>
      </div>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <CharacterCard 
          v-for="character in characterStore.favoriteCharacters" 
          :key="character.id"
          :character="character"
          @click="goToChat(character.id)"
        />
      </div>
    </div>
    
    <!-- Empty State -->
    <div v-if="characterStore.characters.length === 0" class="text-center py-16">
      <div class="w-24 h-24 bg-gradient-to-r from-primary-500/20 to-accent-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
        <UserPlusIcon class="w-12 h-12 text-primary-400" />
      </div>
      <h3 class="text-2xl font-bold text-white mb-4">İlk Karakterini Yarat</h3>
      <p class="text-gray-400 mb-8 max-w-md mx-auto">
        Henüz hiç karakterin yok. Hemen ilk yoldaşını yaratarak bu büyülü yolculuğa başla!
      </p>
      <router-link to="/app/create" class="btn-primary inline-flex items-center">
        <SparklesIcon class="w-5 h-5 mr-2" />
        İlk Karakterimi Yarat
      </router-link>
    </div>
    
    <!-- Stats Cards -->
    <div class="grid md:grid-cols-4 gap-6">
      <div class="glass-dark rounded-xl p-6 text-center">
        <div class="text-3xl font-bold text-primary-400 mb-2">
          {{ characterStore.characters.length }}
        </div>
        <div class="text-gray-400 text-sm">Toplam Karakter</div>
      </div>
      
      <div class="glass-dark rounded-xl p-6 text-center">
        <div class="text-3xl font-bold text-secondary-400 mb-2">
          {{ characterStore.favoriteCharacters.length }}
        </div>
        <div class="text-gray-400 text-sm">Favori Karakter</div>
      </div>
      
      <div class="glass-dark rounded-xl p-6 text-center">
        <div class="text-3xl font-bold text-accent-400 mb-2">
          {{ totalChats }}
        </div>
        <div class="text-gray-400 text-sm">Toplam Mesaj</div>
      </div>
      
      <div class="glass-dark rounded-xl p-6 text-center">
        <div class="text-3xl font-bold text-green-400 mb-2">
          {{ authStore.user?.credits || 100 }}
        </div>
        <div class="text-gray-400 text-sm">Kalan Kredi</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  PlusIcon, 
  UserGroupIcon, 
  ChatBubbleLeftRightIcon,
  ArrowRightIcon,
  HeartIcon,
  UserPlusIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useCharacterStore } from '@/stores/character'
import CharacterCard from '@/components/CharacterCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const characterStore = useCharacterStore()

// Computed properties
const totalChats = computed(() => {
  // Bu değer gerçek API'den gelecek, şimdilik mock data
  return characterStore.characters.reduce((total, char) => {
    return total + (char.message_count || 0)
  }, 0)
})

// Methods
const goToChat = (characterId) => {
  router.push(`/app/chat/${characterId}`)
}

// Lifecycle
onMounted(async () => {
  try {
    await characterStore.fetchCharacters()
  } catch (error) {
    console.error('Failed to fetch characters:', error)
  }
})
</script>