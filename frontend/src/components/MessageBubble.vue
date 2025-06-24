<template>
  <div 
    class="flex mb-4"
    :class="isUser ? 'justify-end' : 'justify-start'"
  >
    <!-- AI Avatar -->
    <div 
      v-if="!isUser" 
      class="flex-shrink-0 mr-3"
    >
      <div class="w-8 h-8 bg-gradient-to-r from-secondary-500 to-accent-500 rounded-full flex items-center justify-center">
        <span class="text-white text-sm font-medium">
          {{ character?.name?.charAt(0) || 'AI' }}
        </span>
      </div>
    </div>
    
    <!-- Message Content -->
    <div 
      class="max-w-xs lg:max-w-md px-4 py-3 rounded-2xl shadow-lg"
      :class="messageClasses"
    >
      <!-- Message Text -->
      <div 
        class="text-sm leading-relaxed"
        :class="isUser ? 'text-white' : 'text-gray-100'"
        v-html="formattedMessage"
      ></div>
      
      <!-- Timestamp -->
      <div 
        class="text-xs mt-2 opacity-70"
        :class="isUser ? 'text-primary-100' : 'text-gray-400'"
      >
        {{ formatTime(message.created_at) }}
      </div>
      
      <!-- Message Status (for user messages) -->
      <div 
        v-if="isUser && message.status"
        class="flex items-center mt-1 text-xs text-primary-200"
      >
        <CheckIcon 
          v-if="message.status === 'sent'"
          class="w-3 h-3 mr-1"
        />
        <CheckIcon 
          v-else-if="message.status === 'delivered'"
          class="w-3 h-3 mr-1"
        />
        <ExclamationTriangleIcon 
          v-else-if="message.status === 'error'"
          class="w-3 h-3 mr-1 text-red-400"
        />
        <span>{{ getStatusText(message.status) }}</span>
      </div>
    </div>
    
    <!-- User Avatar -->
    <div 
      v-if="isUser" 
      class="flex-shrink-0 ml-3"
    >
      <div class="w-8 h-8 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
        <span class="text-white text-sm font-medium">
          {{ userInitial }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { 
  CheckIcon, 
  ExclamationTriangleIcon 
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'

// Props
const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  character: {
    type: Object,
    default: null
  }
})

// Store
const authStore = useAuthStore()

// Computed properties
const isUser = computed(() => {
  return props.message.sender === 'user' || props.message.is_user
})

const userInitial = computed(() => {
  return authStore.user?.email?.charAt(0).toUpperCase() || 'U'
})

const messageClasses = computed(() => {
  if (isUser.value) {
    return 'bg-gradient-to-r from-primary-500 to-primary-600 text-white message-bubble-user'
  } else {
    return 'bg-gradient-to-r from-secondary-500/20 to-accent-500/20 backdrop-blur-sm border border-secondary-500/30 message-bubble-ai'
  }
})

const formattedMessage = computed(() => {
  if (!props.message.content) return ''
  
  // Convert line breaks to HTML
  let formatted = props.message.content.replace(/\n/g, '<br>')
  
  // Convert **bold** to <strong>
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  
  // Convert *italic* to <em>
  formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  return formatted
})

// Methods
const formatTime = (timestamp) => {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffMinutes = Math.ceil(diffTime / (1000 * 60))
  const diffHours = Math.ceil(diffTime / (1000 * 60 * 60))
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffMinutes < 1) return 'Şimdi'
  if (diffMinutes < 60) return `${diffMinutes}dk önce`
  if (diffHours < 24) return `${diffHours}sa önce`
  if (diffDays === 1) return 'Dün'
  if (diffDays < 7) return `${diffDays} gün önce`
  
  return date.toLocaleDateString('tr-TR', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusText = (status) => {
  switch (status) {
    case 'sending':
      return 'Gönderiliyor...'
    case 'sent':
      return 'Gönderildi'
    case 'delivered':
      return 'İletildi'
    case 'error':
      return 'Hata'
    default:
      return ''
  }
}
</script>

<style scoped>
.message-bubble-user {
  border-radius: 1.5rem 1.5rem 0.5rem 1.5rem;
}

.message-bubble-ai {
  border-radius: 1.5rem 1.5rem 1.5rem 0.5rem;
}

/* Custom scrollbar for long messages */
.message-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.message-content::-webkit-scrollbar {
  width: 4px;
}

.message-content::-webkit-scrollbar-track {
  background: transparent;
}

.message-content::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}
</style>