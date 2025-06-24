<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 bg-black bg-opacity-75 transition-opacity"
        @click="$emit('cancel')"
      ></div>
      
      <!-- Modal panel -->
      <div class="inline-block align-bottom glass-dark rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="p-6">
          <!-- Icon -->
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
            <ExclamationTriangleIcon class="h-6 w-6 text-red-600" />
          </div>
          
          <!-- Content -->
          <div class="text-center">
            <h3 class="text-lg leading-6 font-medium text-white mb-2">
              {{ title }}
            </h3>
            <div class="mt-2">
              <p class="text-sm text-gray-400">
                {{ message }}
              </p>
            </div>
          </div>
        </div>
        
        <!-- Actions -->
        <div class="px-6 py-4 bg-dark-800/50 flex flex-col-reverse sm:flex-row sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0">
          <button
            type="button"
            class="btn-ghost w-full sm:w-auto"
            @click="$emit('cancel')"
          >
            {{ cancelText }}
          </button>
          <button
            type="button"
            class="w-full sm:w-auto px-4 py-2 text-white font-medium rounded-lg transition-colors duration-300"
            :class="confirmClass"
            @click="$emit('confirm')"
          >
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

// Props
defineProps({
  title: {
    type: String,
    default: 'Emin misin?'
  },
  message: {
    type: String,
    default: 'Bu işlem geri alınamaz.'
  },
  confirmText: {
    type: String,
    default: 'Evet'
  },
  cancelText: {
    type: String,
    default: 'İptal'
  },
  confirmClass: {
    type: String,
    default: 'bg-red-600 hover:bg-red-700'
  }
})

// Emits
defineEmits(['confirm', 'cancel'])
</script>