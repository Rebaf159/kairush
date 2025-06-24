<template>
  <div class="h-full flex flex-col">
    <!-- Chat Header -->
    <div class="glass-dark border-b border-white/10 p-4 flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <!-- Back Button -->
        <button 
          @click="goBack"
          class="p-2 text-gray-400 hover:text-white transition-colors duration-300 rounded-lg hover:bg-white/10"
        >
          <ArrowLeftIcon class="w-5 h-5" />
        </button>
        
        <!-- Character Info -->
        <div v-if="character" class="flex items-center space-x-3">
          <div class="w-12 h-12 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
            <img 
              v-if="character.profile_image_url" 
              :src="character.profile_image_url" 
              :alt="character.name"
              class="w-full h-full rounded-full object-cover"
            />
            <span v-else class="text-white font-semibold text-lg">
              {{ character.name.charAt(0) }}
            </span>
          </div>
          <div>
            <h2 class="text-lg font-semibold text-white">{{ character.name }}</h2>
            <p class="text-sm text-gray-400">{{ character.tagline || 'Sohbet etmeye hazır' }}</p>
          </div>
        </div>
        
        <!-- Loading State -->
        <div v-else class="flex items-center space-x-3">
          <div class="w-12 h-12 skeleton rounded-full"></div>
          <div>
            <div class="w-24 h-4 skeleton rounded mb-2"></div>
            <div class="w-32 h-3 skeleton rounded"></div>
          </div>
        </div>
      </div>
      
      <!-- Actions -->
      <div class="flex items-center space-x-2">
        <!-- Favorite Button -->
        <button 
          v-if="character"
          @click="toggleFavorite"
          class="p-2 rounded-lg transition-all duration-300"
          :class="character.is_favorite ? 'text-red-400 hover:text-red-300' : 'text-gray-400 hover:text-white'"
        >
          <HeartIcon v-if="!character.is_favorite" class="w-5 h-5" />
          <HeartIcon v-else class="w-5 h-5 fill-current" />
        </button>
        
        <!-- Menu Button -->
        <div class="relative" ref="menuRef">
          <button 
            @click="showMenu = !showMenu"
            class="p-2 text-gray-400 hover:text-white transition-colors duration-300 rounded-lg hover:bg-white/10"
          >
            <EllipsisVerticalIcon class="w-5 h-5" />
          </button>
          
          <!-- Dropdown Menu -->
          <div 
            v-if="showMenu"
            class="absolute right-0 top-full mt-2 w-48 glass-dark rounded-lg shadow-xl border border-white/10 py-2 z-50"
          >
            <button 
              @click="clearChat"
              class="w-full px-4 py-2 text-left text-gray-300 hover:text-white hover:bg-white/10 transition-colors duration-300 flex items-center space-x-2"
            >
              <TrashIcon class="w-4 h-4" />
              <span>Sohbeti Temizle</span>
            </button>
            <button 
              @click="exportChat"
              class="w-full px-4 py-2 text-left text-gray-300 hover:text-white hover:bg-white/10 transition-colors duration-300 flex items-center space-x-2"
            >
              <ArrowDownTrayIcon class="w-4 h-4" />
              <span>Sohbeti Dışa Aktar</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Chat Messages -->
    <div 
      ref="messagesContainer"
      class="flex-1 overflow-y-auto p-4 space-y-4"
      @scroll="handleScroll"
    >
      <!-- Welcome Message -->
      <div v-if="chatHistory.length === 0" class="text-center py-8">
        <div class="w-16 h-16 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <ChatBubbleLeftRightIcon class="w-8 h-8 text-white" />
        </div>
        <h3 class="text-xl font-semibold text-white mb-2">
          {{ character?.name || 'Karakterin' }} ile sohbete başla!
        </h3>
        <p class="text-gray-400 max-w-md mx-auto">
          Merhaba de, soru sor veya herhangi bir konuda konuşmaya başla.
        </p>
      </div>
      
      <!-- Messages -->
      <div v-for="message in chatHistory" :key="message.id" class="flex" :class="message.is_user ? 'justify-end' : 'justify-start'">
        <MessageBubble 
          :message="message"
          :character="character"
        />
      </div>
      
      <!-- Typing Indicator -->
      <div v-if="characterStore.chatLoading" class="flex justify-start">
        <div class="message-ai flex items-center space-x-2">
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-white rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
          <span class="text-sm text-white/70">yazıyor...</span>
        </div>
      </div>
    </div>
    
    <!-- Message Input -->
    <div class="glass-dark border-t border-white/10 p-4">
      <form @submit.prevent="sendMessage" class="flex space-x-4">
        <div class="flex-1 relative">
          <textarea
            ref="messageInput"
            v-model="newMessage"
            placeholder="Mesajını yaz..."
            class="form-textarea resize-none"
            rows="1"
            :disabled="characterStore.chatLoading || !character"
            @keydown="handleKeyDown"
            @input="adjustTextareaHeight"
          ></textarea>
          
          <!-- Character Count -->
          <div class="absolute bottom-2 right-2 text-xs text-gray-500">
            {{ newMessage.length }}/1000
          </div>
        </div>
        
        <button
          type="submit"
          class="btn-primary px-6 flex items-center justify-center min-w-[100px]"
          :disabled="!newMessage.trim() || characterStore.chatLoading || !character"
        >
          <template v-if="characterStore.chatLoading">
            <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </template>
          <template v-else>
            <PaperAirplaneIcon class="w-5 h-5" />
          </template>
        </button>
      </form>
      
      <!-- Quick Actions -->
      <div class="flex items-center justify-between mt-3 text-sm text-gray-400">
        <div class="flex items-center space-x-4">
          <span>Kredi: {{ authStore.user?.credits || 0 }}</span>
          <span>•</span>
          <span>{{ chatHistory.length }} mesaj</span>
        </div>
        
        <div class="flex items-center space-x-2">
          <button 
            @click="addQuickMessage('Merhaba!')"
            class="px-3 py-1 bg-dark-800 hover:bg-dark-700 rounded-full transition-colors duration-300"
          >
            👋 Merhaba
          </button>
          <button 
            @click="addQuickMessage('Nasılsın?')"
            class="px-3 py-1 bg-dark-800 hover:bg-dark-700 rounded-full transition-colors duration-300"
          >
            😊 Nasılsın?
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  ArrowLeftIcon,
  HeartIcon,
  EllipsisVerticalIcon,
  TrashIcon,
  ArrowDownTrayIcon,
  ChatBubbleLeftRightIcon,
  PaperAirplaneIcon
} from '@heroicons/vue/24/outline'
import { useCharacterStore } from '@/stores/character'
import { useAuthStore } from '@/stores/auth'
import MessageBubble from '../components/MessageBubble.vue'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const characterStore = useCharacterStore()
const authStore = useAuthStore()
const toast = useToast()

// Reactive data
const character = ref(null)
const newMessage = ref('')
const showMenu = ref(false)
const messagesContainer = ref(null)
const messageInput = ref(null)
const menuRef = ref(null)

// Computed
const chatHistory = computed(() => characterStore.chatHistory)
const characterId = computed(() => route.params.id)

// Methods
const goBack = () => {
  router.push('/app/characters')
}

const toggleFavorite = async () => {
  if (!character.value) return
  
  try {
    await characterStore.toggleFavorite(character.value.id)
    character.value.is_favorite = !character.value.is_favorite
  } catch (error) {
    console.error('Failed to toggle favorite:', error)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !character.value) return
  
  const message = newMessage.value.trim()
  newMessage.value = ''
  
  try {
    await characterStore.sendMessage(character.value.id, message)
    scrollToBottom()
  } catch (error) {
    console.error('Failed to send message:', error)
    newMessage.value = message // Restore message on error
  }
}

const addQuickMessage = (message) => {
  newMessage.value = message
  nextTick(() => {
    messageInput.value?.focus()
  })
}

const clearChat = () => {
  characterStore.clearChatHistory()
  showMenu.value = false
  toast.info('Sohbet geçmişi temizlendi')
}

const exportChat = () => {
  const chatData = {
    character: character.value?.name,
    messages: chatHistory.value,
    exportDate: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(chatData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${character.value?.name || 'chat'}-${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
  
  showMenu.value = false
  toast.success('Sohbet dışa aktarıldı')
}

const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const adjustTextareaHeight = () => {
  const textarea = messageInput.value
  if (textarea) {
    textarea.style.height = 'auto'
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleScroll = () => {
  // Auto-load more messages when scrolled to top (if needed)
}

const handleClickOutside = (event) => {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    showMenu.value = false
  }
}

// Lifecycle
onMounted(async () => {
  try {
    // Load character
    character.value = await characterStore.getCharacter(characterId.value)
    
    // Load chat history
    await characterStore.loadChatHistory(characterId.value)
    
    // Scroll to bottom
    scrollToBottom()
    
    // Focus input
    nextTick(() => {
      messageInput.value?.focus()
    })
    
    // Add click outside listener
    document.addEventListener('click', handleClickOutside)
  } catch (error) {
    console.error('Failed to load character or chat:', error)
    toast.error('Karakter yüklenemedi')
    router.push('/app/characters')
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  characterStore.clearChatHistory()
})

// Watch for new messages to auto-scroll
watch(() => chatHistory.value.length, () => {
  scrollToBottom()
})

// Watch for character changes
watch(() => characterId.value, async (newId) => {
  if (newId) {
    try {
      character.value = await characterStore.getCharacter(newId)
      await characterStore.loadChatHistory(newId)
      scrollToBottom()
    } catch (error) {
      console.error('Failed to load character:', error)
    }
  }
})
</script>

<style scoped>
/* Custom scrollbar for messages */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>