<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-white mb-2">Karakterlerim</h1>
        <p class="text-gray-400">
          {{ filteredCharacters.length }} karakter bulundu
        </p>
      </div>
      
      <router-link to="/app/create" class="btn-primary flex items-center">
        <PlusIcon class="w-5 h-5 mr-2" />
        Yeni Karakter
      </router-link>
    </div>
    
    <!-- Filters and Search -->
    <div class="glass-dark rounded-xl p-6 mb-8">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1">
          <div class="relative">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Karakter ara..."
              class="form-input pl-10"
            />
          </div>
        </div>
        
        <!-- Filter Buttons -->
        <div class="flex space-x-2">
          <button
            @click="activeFilter = 'all'"
            class="px-4 py-2 rounded-lg transition-all duration-300"
            :class="activeFilter === 'all' ? 'bg-primary-500 text-white' : 'bg-dark-800 text-gray-400 hover:text-white'"
          >
            Tümü
          </button>
          <button
            @click="activeFilter = 'favorites'"
            class="px-4 py-2 rounded-lg transition-all duration-300 flex items-center space-x-1"
            :class="activeFilter === 'favorites' ? 'bg-red-500 text-white' : 'bg-dark-800 text-gray-400 hover:text-white'"
          >
            <HeartIcon class="w-4 h-4" />
            <span>Favoriler</span>
          </button>
          <button
            @click="activeFilter = 'recent'"
            class="px-4 py-2 rounded-lg transition-all duration-300 flex items-center space-x-1"
            :class="activeFilter === 'recent' ? 'bg-secondary-500 text-white' : 'bg-dark-800 text-gray-400 hover:text-white'"
          >
            <ClockIcon class="w-4 h-4" />
            <span>Son Sohbet</span>
          </button>
        </div>
        
        <!-- Sort -->
        <select
          v-model="sortBy"
          class="form-input w-auto min-w-[150px]"
        >
          <option value="name">İsme Göre</option>
          <option value="created_at">Yaratılma Tarihi</option>
          <option value="last_chat_at">Son Sohbet</option>
        </select>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="characterStore.loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <SkeletonLoader v-for="i in 6" :key="i" type="character-card" />
    </div>
    
    <!-- Characters Grid -->
    <div v-else-if="filteredCharacters.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <CharacterCard 
        v-for="character in filteredCharacters" 
        :key="character.id"
        :character="character"
        @click="goToChat(character.id)"
        @favorite="toggleFavorite(character.id)"
        @edit="editCharacter(character.id)"
        @delete="deleteCharacter(character.id)"
        show-actions
      />
    </div>
    
    <!-- Empty State -->
    <div v-else class="text-center py-16">
      <div class="w-24 h-24 bg-gradient-to-r from-primary-500/20 to-accent-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
        <component :is="getEmptyStateIcon()" class="w-12 h-12 text-primary-400" />
      </div>
      <h3 class="text-2xl font-bold text-white mb-4">{{ getEmptyStateTitle() }}</h3>
      <p class="text-gray-400 mb-8 max-w-md mx-auto">
        {{ getEmptyStateDescription() }}
      </p>
      <router-link 
        v-if="activeFilter === 'all' && searchQuery === ''"
        to="/app/create" 
        class="btn-primary inline-flex items-center"
      >
        <SparklesIcon class="w-5 h-5 mr-2" />
        İlk Karakterini Yarat
      </router-link>
      <button 
        v-else
        @click="clearFilters"
        class="btn-secondary inline-flex items-center"
      >
        <XMarkIcon class="w-5 h-5 mr-2" />
        Filtreleri Temizle
      </button>
    </div>
    
    <!-- Character Edit Modal -->
    <CharacterEditModal 
      v-if="editingCharacter"
      :character="editingCharacter"
      @close="editingCharacter = null"
      @save="handleCharacterUpdate"
    />
    
    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      v-if="deletingCharacter"
      :title="`${deletingCharacter.name} karakterini sil`"
      :message="`Bu işlem geri alınamaz. ${deletingCharacter.name} ve tüm sohbet geçmişi kalıcı olarak silinecek.`"
      confirm-text="Sil"
      confirm-class="btn-danger"
      @confirm="confirmDelete"
      @cancel="deletingCharacter = null"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  PlusIcon, 
  MagnifyingGlassIcon,
  HeartIcon,
  ClockIcon,
  SparklesIcon,
  XMarkIcon,
  UserGroupIcon,
  FaceSmileIcon
} from '@heroicons/vue/24/outline'
import { useCharacterStore } from '@/stores/character'
import CharacterCard from '../components/CharacterCard.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import CharacterEditModal from '../components/CharacterEditModal.vue'
import ConfirmationModal from '../components/ConfirmationModal.vue'
import { useToast } from 'vue-toastification'

const router = useRouter()
const characterStore = useCharacterStore()
const toast = useToast()

// Reactive data
const searchQuery = ref('')
const activeFilter = ref('all')
const sortBy = ref('name')
const editingCharacter = ref(null)
const deletingCharacter = ref(null)

// Computed properties
const filteredCharacters = computed(() => {
  let characters = [...characterStore.characters]
  
  // Apply filter
  if (activeFilter.value === 'favorites') {
    characters = characters.filter(char => char.is_favorite)
  } else if (activeFilter.value === 'recent') {
    characters = characters.filter(char => char.last_chat_at)
  }
  
  // Apply search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    characters = characters.filter(char => 
      char.name.toLowerCase().includes(query) ||
      char.tagline?.toLowerCase().includes(query) ||
      char.personality_prompt?.toLowerCase().includes(query)
    )
  }
  
  // Apply sort
  characters.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'created_at':
        return new Date(b.created_at) - new Date(a.created_at)
      case 'last_chat_at':
        if (!a.last_chat_at && !b.last_chat_at) return 0
        if (!a.last_chat_at) return 1
        if (!b.last_chat_at) return -1
        return new Date(b.last_chat_at) - new Date(a.last_chat_at)
      default:
        return 0
    }
  })
  
  return characters
})

// Methods
const goToChat = (characterId) => {
  router.push(`/app/chat/${characterId}`)
}

const toggleFavorite = async (characterId) => {
  try {
    await characterStore.toggleFavorite(characterId)
  } catch (error) {
    console.error('Failed to toggle favorite:', error)
  }
}

const editCharacter = (characterId) => {
  const character = characterStore.characters.find(char => char.id === characterId)
  if (character) {
    editingCharacter.value = { ...character }
  }
}

const deleteCharacter = (characterId) => {
  const character = characterStore.characters.find(char => char.id === characterId)
  if (character) {
    deletingCharacter.value = character
  }
}

const confirmDelete = async () => {
  if (!deletingCharacter.value) return
  
  try {
    await characterStore.deleteCharacter(deletingCharacter.value.id)
    deletingCharacter.value = null
  } catch (error) {
    console.error('Failed to delete character:', error)
  }
}

const handleCharacterUpdate = async (updatedCharacter) => {
  try {
    await characterStore.updateCharacter(updatedCharacter.id, updatedCharacter)
    editingCharacter.value = null
  } catch (error) {
    console.error('Failed to update character:', error)
  }
}

const clearFilters = () => {
  searchQuery.value = ''
  activeFilter.value = 'all'
  sortBy.value = 'name'
}

const getEmptyStateIcon = () => {
  if (activeFilter.value === 'favorites') return HeartIcon
  if (activeFilter.value === 'recent') return ClockIcon
  if (searchQuery.value) return MagnifyingGlassIcon
  return UserGroupIcon
}

const getEmptyStateTitle = () => {
  if (activeFilter.value === 'favorites') return 'Henüz Favori Karakterin Yok'
  if (activeFilter.value === 'recent') return 'Henüz Sohbet Etmemişsin'
  if (searchQuery.value) return 'Arama Sonucu Bulunamadı'
  return 'Henüz Karakterin Yok'
}

const getEmptyStateDescription = () => {
  if (activeFilter.value === 'favorites') return 'Beğendiğin karakterleri favorilere ekleyerek buradan kolayca erişebilirsin.'
  if (activeFilter.value === 'recent') return 'Karakterlerinle sohbet etmeye başla, son konuştuklarını burada görebilirsin.'
  if (searchQuery.value) return `"${searchQuery.value}" araması için sonuç bulunamadı. Farklı kelimeler deneyin.`
  return 'İlk karakterini yaratarak bu büyülü yolculuğa başla!'
}

// Lifecycle
onMounted(async () => {
  if (characterStore.characters.length === 0) {
    try {
      await characterStore.fetchCharacters()
    } catch (error) {
      console.error('Failed to fetch characters:', error)
    }
  }
})

// Watch for URL query parameters
watch(() => router.currentRoute.value.query, (newQuery) => {
  if (newQuery.search) {
    searchQuery.value = newQuery.search
  }
  if (newQuery.filter) {
    activeFilter.value = newQuery.filter
  }
}, { immediate: true })
</script>