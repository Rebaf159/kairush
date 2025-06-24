<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Character Name -->
    <div>
      <label class="block text-sm font-medium text-gray-300 mb-2">
        Karakter Adı *
      </label>
      <input
        v-model="form.name"
        type="text"
        class="form-input"
        placeholder="Örn: Luna, Kai, Aria..."
        required
        :disabled="loading"
      />
      <p class="mt-1 text-xs text-gray-500">
        Karakterinin nasıl çağrılmasını istiyorsun?
      </p>
    </div>
    
    <!-- Relationship Type -->
    <div>
      <label class="block text-sm font-medium text-gray-300 mb-2">
        İlişki Türü *
      </label>
      <select
        v-model="form.relationship"
        class="form-select"
        required
        :disabled="loading"
      >
        <option value="">Seçiniz...</option>
        <option value="Sevgili">Sevgili</option>
        <option value="Arkadaş">Arkadaş</option>
        <option value="Mentor">Mentor</option>
        <option value="Kardeş">Kardeş</option>
        <option value="Öğretmen">Öğretmen</option>
        <option value="Rehber">Rehber</option>
        <option value="Sırdaş">Sırdaş</option>
        <option value="Partner">Partner</option>
      </select>
      <p class="mt-1 text-xs text-gray-500">
        Karakterinle nasıl bir ilişki kurmak istiyorsun?
      </p>
    </div>
    
    <!-- Personality Prompt -->
    <div>
      <label class="block text-sm font-medium text-gray-300 mb-2">
        Kişilik Tanımı *
      </label>
      <textarea
        v-model="form.personality_prompt"
        class="form-textarea"
        rows="4"
        placeholder="Karakterinin kişiliğini detaylı olarak tanımla. Nasıl davranır, nasıl konuşur, hangi özelliklere sahip?"
        required
        :disabled="loading"
        @input="adjustTextareaHeight"
      ></textarea>
      <div class="flex justify-between items-center mt-1">
        <p class="text-xs text-gray-500">
          Karakterinin ruhunu ve davranış biçimini tanımla
        </p>
        <span class="text-xs text-gray-500">
          {{ form.personality_prompt.length }}/1000
        </span>
      </div>
    </div>
    
    <!-- Appearance Prompt -->
    <div>
      <label class="block text-sm font-medium text-gray-300 mb-2">
        Görünüm Tanımı
      </label>
      <textarea
        v-model="form.appearance_prompt"
        class="form-textarea"
        rows="3"
        placeholder="Karakterinin fiziksel görünümünü tanımla. Saç rengi, göz rengi, boy, kıyafet tarzı..."
        :disabled="loading"
        @input="adjustTextareaHeight"
      ></textarea>
      <div class="flex justify-between items-center mt-1">
        <p class="text-xs text-gray-500">
          İsteğe bağlı - Karakterinin nasıl göründüğünü hayal et
        </p>
        <span class="text-xs text-gray-500">
          {{ form.appearance_prompt.length }}/500
        </span>
      </div>
    </div>
    
    <!-- Tagline -->
    <div>
      <label class="block text-sm font-medium text-gray-300 mb-2">
        Kısa Tanıtım
      </label>
      <input
        v-model="form.tagline"
        type="text"
        class="form-input"
        placeholder="Karakterini tek cümlede özetle..."
        maxlength="100"
        :disabled="loading"
      />
      <div class="flex justify-between items-center mt-1">
        <p class="text-xs text-gray-500">
          İsteğe bağlı - Karakter kartında görünecek kısa açıklama
        </p>
        <span class="text-xs text-gray-500">
          {{ form.tagline.length }}/100
        </span>
      </div>
    </div>
    
    <!-- Advanced Settings Toggle -->
    <div class="border-t border-gray-700 pt-6">
      <button
        type="button"
        @click="showAdvanced = !showAdvanced"
        class="flex items-center text-sm text-gray-400 hover:text-white transition-colors duration-300"
      >
        <ChevronDownIcon 
          class="w-4 h-4 mr-2 transition-transform duration-300"
          :class="showAdvanced ? 'rotate-180' : ''"
        />
        Gelişmiş Ayarlar
      </button>
    </div>
    
    <!-- Advanced Settings -->
    <div v-if="showAdvanced" class="space-y-6 border-l-2 border-primary-500/30 pl-6">
      <!-- Temperature -->
      <div>
        <label class="block text-sm font-medium text-gray-300 mb-2">
          Yaratıcılık Seviyesi: {{ form.temperature }}
        </label>
        <input
          v-model.number="form.temperature"
          type="range"
          min="0.1"
          max="1.0"
          step="0.1"
          class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
          :disabled="loading"
        />
        <div class="flex justify-between text-xs text-gray-500 mt-1">
          <span>Tutarlı</span>
          <span>Yaratıcı</span>
        </div>
      </div>
      
      <!-- Max Tokens -->
      <div>
        <label class="block text-sm font-medium text-gray-300 mb-2">
          Maksimum Yanıt Uzunluğu
        </label>
        <select
          v-model.number="form.max_tokens"
          class="form-select"
          :disabled="loading"
        >
          <option :value="150">Kısa (150 token)</option>
          <option :value="300">Orta (300 token)</option>
          <option :value="500">Uzun (500 token)</option>
          <option :value="800">Çok Uzun (800 token)</option>
        </select>
      </div>
      
      <!-- System Prompt -->
      <div>
        <label class="block text-sm font-medium text-gray-300 mb-2">
          Sistem Talimatları
        </label>
        <textarea
          v-model="form.system_prompt"
          class="form-textarea"
          rows="3"
          placeholder="Karakterin nasıl davranması gerektiğine dair özel talimatlar..."
          :disabled="loading"
        ></textarea>
        <p class="mt-1 text-xs text-gray-500">
          İsteğe bağlı - Karakterin davranışını daha spesifik olarak yönlendir
        </p>
      </div>
    </div>
    
    <!-- Submit Button -->
    <div class="flex space-x-4 pt-6">
      <button
        type="submit"
        class="flex-1 btn-primary flex items-center justify-center"
        :disabled="loading || !isFormValid"
      >
        <template v-if="loading">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Yaratılıyor...
        </template>
        <template v-else>
          <SparklesIcon class="w-5 h-5 mr-2" />
          Karakteri Yarat
        </template>
      </button>
      
      <button
        type="button"
        @click="resetForm"
        class="btn-ghost"
        :disabled="loading"
      >
        <ArrowPathIcon class="w-5 h-5 mr-2" />
        Sıfırla
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, computed, nextTick } from 'vue'
import {
  ChevronDownIcon,
  SparklesIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  initialData: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['submit'])

// Reactive data
const showAdvanced = ref(false)

const form = reactive({
  name: '',
  relationship: '',
  personality_prompt: '',
  appearance_prompt: '',
  tagline: '',
  temperature: 0.7,
  max_tokens: 300,
  system_prompt: '',
  ...props.initialData
})

// Computed properties
const isFormValid = computed(() => {
  return form.name.trim() && 
         form.relationship && 
         form.personality_prompt.trim().length >= 10
})

// Methods
const handleSubmit = () => {
  if (!isFormValid.value) return
  
  emit('submit', { ...form })
}

const resetForm = () => {
  Object.assign(form, {
    name: '',
    relationship: '',
    personality_prompt: '',
    appearance_prompt: '',
    tagline: '',
    temperature: 0.7,
    max_tokens: 300,
    system_prompt: ''
  })
  showAdvanced.value = false
}

const adjustTextareaHeight = async (event) => {
  await nextTick()
  const textarea = event.target
  textarea.style.height = 'auto'
  textarea.style.height = textarea.scrollHeight + 'px'
}

// Expose methods for parent component
defineExpose({
  resetForm,
  setFormData: (data) => Object.assign(form, data)
})
</script>

<style scoped>
/* Custom slider styles */
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: linear-gradient(45deg, #EC4899, #8B5CF6);
  cursor: pointer;
  box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
}

.slider::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: linear-gradient(45deg, #EC4899, #8B5CF6);
  cursor: pointer;
  border: none;
  box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
}

/* Auto-expanding textarea */
.form-textarea {
  resize: none;
  overflow: hidden;
  min-height: 80px;
}
</style>