<template>
  <div class="glass-dark rounded-2xl p-6 hover:scale-105 hover:shadow-2xl transition-all duration-300 group cursor-pointer">
    <!-- Character Image -->
    <div class="relative mb-4">
      <div class="w-full h-48 bg-gradient-to-br from-primary-500/20 to-accent-500/20 rounded-xl flex items-center justify-center overflow-hidden">
        <img 
          v-if="character.profile_image" 
          :src="character.profile_image" 
          :alt="character.name"
          class="w-full h-full object-cover"
        />
        <div v-else class="text-6xl text-white/50">
          {{ character.name?.charAt(0) || '?' }}
        </div>
      </div>
      
      <!-- Favorite Button -->
      <button
        @click.stop="toggleFavorite"
        class="absolute top-3 right-3 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300"
        :class="isFavorite ? 'bg-red-500 text-white' : 'bg-black/50 text-gray-400 hover:text-red-400'"
      >
        <HeartIcon 
          class="w-4 h-4" 
          :class="isFavorite ? 'fill-current' : ''"
        />
      </button>
      
      <!-- Online Status -->
      <div class="absolute bottom-3 left-3 flex items-center space-x-2">
        <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
        <span class="text-xs text-green-400 font-medium">Çevrimiçi</span>
      </div>
    </div>
    
    <!-- Character Info -->
    <div class="space-y-3">
      <!-- Name and Relationship -->
      <div>
        <h3 class="text-xl font-bold text-white group-hover:text-primary-400 transition-colors duration-300">
          {{ character.name }}
        </h3>
        <p class="text-sm text-primary-400 font-medium">
          {{ character.relationship || 'Arkadaş' }}
        </p>
      </div>
      
      <!-- Tagline -->
      <p class="text-gray-400 text-sm line-clamp-2">
        {{ character.tagline || 'Henüz bir açıklama eklenmemiş.' }}
      </p>
      
      <!-- Stats -->
      <div class="flex items-center justify-between text-xs text-gray-500">
        <div class="flex items-center space-x-1">
          <ChatBubbleLeftIcon class="w-4 h-4" />
          <span>{{ character.message_count || 0 }} mesaj</span>
        </div>
        <div class="flex items-center space-x-1">
          <ClockIcon class="w-4 h-4" />
          <span>{{ formatLastChat(character.last_chat_at) }}</span>
        </div>
      </div>
      
      <!-- Action Buttons -->
      <div class="flex space-x-2 pt-2">
        <button
          @click.stop="$emit('chat', character.id)"
          class="flex-1 btn-primary text-sm py-2"
        >
          <ChatBubbleLeftIcon class="w-4 h-4 mr-1" />
          Sohbet Et
        </button>
        
        <button
          @click.stop="$emit('edit', character.id)"
          class="btn-ghost p-2"
          title="Düzenle"
        >
          <PencilIcon class="w-4 h-4" />
        </button>
        
        <button
          @click.stop="showDeleteConfirmation = true"
          class="btn-ghost p-2 text-red-400 hover:text-red-300"
          title="Sil"
        >
          <TrashIcon class="w-4 h-4" />
        </button>
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      v-if="showDeleteConfirmation"
      :title="`${character.name} karakterini sil`"
      :message="`${character.name} karakterini ve tüm sohbet geçmişini kalıcı olarak silmek istediğinden emin misin?`"
      confirm-text="Evet, Sil"
      confirm-class="bg-red-600 hover:bg-red-700"
      @confirm="deleteCharacter"
      @cancel="showDeleteConfirmation = false"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  HeartIcon,
  ChatBubbleLeftIcon,
  ClockIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import { useCharacterStore } from '@/stores/character'
import ConfirmationModal from './ConfirmationModal.vue'
import { useToast } from 'vue-toastification'

// Props
const props = defineProps({
  character: {
    type: Object,
    required: true
  }
})

// Emits
defineEmits(['chat', 'edit', 'delete'])

// Store and composables
const characterStore = useCharacterStore()
const toast = useToast()

// Reactive data
const showDeleteConfirmation = ref(false)

// Computed properties
const isFavorite = computed(() => {
  return characterStore.favoriteCharacters.some(char => char.id === props.character.id)
})

// Methods
const toggleFavorite = async () => {
  try {
    if (isFavorite.value) {
      await characterStore.removeFavorite(props.character.id)
      toast.success(`${props.character.name} favorilerden çıkarıldı`)
    } else {
      await characterStore.addFavorite(props.character.id)
      toast.success(`${props.character.name} favorilere eklendi`)
    }
  } catch (error) {
    console.error('Failed to toggle favorite:', error)
    toast.error('Favori durumu değiştirilemedi')
  }
}

const deleteCharacter = async () => {
  try {
    await characterStore.deleteCharacter(props.character.id)
    toast.success(`${props.character.name} başarıyla silindi`)
  } catch (error) {
    console.error('Failed to delete character:', error)
    toast.error('Karakter silinemedi')
  } finally {
    showDeleteConfirmation.value = false
  }
}

const formatLastChat = (dateString) => {
  if (!dateString) return 'Hiç'
  
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return 'Dün'
  if (diffDays < 7) return `${diffDays} gün önce`
  if (diffDays < 30) return `${Math.ceil(diffDays / 7)} hafta önce`
  return `${Math.ceil(diffDays / 30)} ay önce`
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>