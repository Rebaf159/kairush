<template>
  <div class="animate-pulse">
    <!-- Character Card Skeleton -->
    <div v-if="type === 'character-card'" class="glass-dark rounded-2xl p-6">
      <!-- Image skeleton -->
      <div class="w-full h-48 bg-gray-700 rounded-xl mb-4"></div>
      
      <!-- Content skeleton -->
      <div class="space-y-3">
        <!-- Name -->
        <div class="h-6 bg-gray-700 rounded w-3/4"></div>
        <!-- Relationship -->
        <div class="h-4 bg-gray-700 rounded w-1/2"></div>
        <!-- Description -->
        <div class="space-y-2">
          <div class="h-3 bg-gray-700 rounded"></div>
          <div class="h-3 bg-gray-700 rounded w-5/6"></div>
        </div>
        <!-- Stats -->
        <div class="flex justify-between">
          <div class="h-3 bg-gray-700 rounded w-1/4"></div>
          <div class="h-3 bg-gray-700 rounded w-1/4"></div>
        </div>
        <!-- Buttons -->
        <div class="flex space-x-2 pt-2">
          <div class="flex-1 h-8 bg-gray-700 rounded"></div>
          <div class="h-8 w-8 bg-gray-700 rounded"></div>
          <div class="h-8 w-8 bg-gray-700 rounded"></div>
        </div>
      </div>
    </div>
    
    <!-- Message Bubble Skeleton -->
    <div v-else-if="type === 'message'" class="flex mb-4" :class="isUser ? 'justify-end' : 'justify-start'">
      <!-- Avatar -->
      <div v-if="!isUser" class="flex-shrink-0 mr-3">
        <div class="w-8 h-8 bg-gray-700 rounded-full"></div>
      </div>
      
      <!-- Message content -->
      <div class="max-w-xs lg:max-w-md">
        <div class="h-16 bg-gray-700 rounded-2xl"></div>
      </div>
      
      <!-- User avatar -->
      <div v-if="isUser" class="flex-shrink-0 ml-3">
        <div class="w-8 h-8 bg-gray-700 rounded-full"></div>
      </div>
    </div>
    
    <!-- List Item Skeleton -->
    <div v-else-if="type === 'list-item'" class="glass-dark rounded-xl p-4 mb-4">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 bg-gray-700 rounded-full"></div>
        <div class="flex-1 space-y-2">
          <div class="h-4 bg-gray-700 rounded w-3/4"></div>
          <div class="h-3 bg-gray-700 rounded w-1/2"></div>
        </div>
        <div class="h-8 w-20 bg-gray-700 rounded"></div>
      </div>
    </div>
    
    <!-- Stats Card Skeleton -->
    <div v-else-if="type === 'stats-card'" class="glass-dark rounded-xl p-6 text-center">
      <div class="h-8 bg-gray-700 rounded w-16 mx-auto mb-2"></div>
      <div class="h-4 bg-gray-700 rounded w-24 mx-auto"></div>
    </div>
    
    <!-- Form Field Skeleton -->
    <div v-else-if="type === 'form-field'" class="space-y-2">
      <div class="h-4 bg-gray-700 rounded w-1/4"></div>
      <div class="h-10 bg-gray-700 rounded"></div>
    </div>
    
    <!-- Text Lines Skeleton -->
    <div v-else-if="type === 'text'" class="space-y-2">
      <div v-for="i in lines" :key="i" class="h-4 bg-gray-700 rounded" :class="getLineWidth(i)"></div>
    </div>
    
    <!-- Default Rectangle Skeleton -->
    <div v-else class="bg-gray-700 rounded" :style="{ width: width, height: height }"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  type: {
    type: String,
    default: 'default',
    validator: (value) => [
      'character-card',
      'message',
      'list-item',
      'stats-card',
      'form-field',
      'text',
      'default'
    ].includes(value)
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '20px'
  },
  lines: {
    type: Number,
    default: 3
  },
  isUser: {
    type: Boolean,
    default: false
  }
})

// Methods
const getLineWidth = (lineNumber) => {
  const widths = ['w-full', 'w-5/6', 'w-4/6', 'w-3/6', 'w-2/6']
  const index = (lineNumber - 1) % widths.length
  return widths[index]
}
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>