<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 bg-black bg-opacity-75 transition-opacity"
        @click="$emit('close')"
      ></div>
      
      <!-- Modal panel -->
      <div class="inline-block align-bottom glass-dark rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        <div class="p-6">
          <!-- Header -->
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-white">
              {{ character.name }} Düzenle
            </h3>
            <button
              @click="$emit('close')"
              class="text-gray-400 hover:text-white transition-colors duration-300"
            >
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>
          
          <!-- Edit Form -->
          <form @submit.prevent="handleSave" class="space-y-6">
            <!-- Character Name -->
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Karakter Adı *
              </label>
              <input
                v-model="form.name"
                type="text"
                class="form-input"
                required
                :disabled="loading"
              />
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
                <option value="Sevgili">Sevgili</option>
                <option value="Arkadaş">Arkadaş</option>
                <option value="Mentor">Mentor</option>
                <option value="Kardeş">Kardeş</option>
                <option value="Öğretmen">Öğretmen</option>
                <option value="Rehber">Rehber</option>
                <option value="Sırdaş">Sırdaş</option>
                <option value="Partner">Partner</option>
              </select>
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
              <div class="flex justify-end mt-1">
                <span class="text-xs text-gray-500">
                  {{ form.tagline.length }}/100
                </span>
              </div>
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
                required
                :disabled="loading"
              ></textarea>
              <div class="flex justify-end mt-1">
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
                :disabled="loading"
              ></textarea>
              <div class="flex justify-end mt-1">
                <span class="text-xs text-gray-500">
                  {{ form.appearance_prompt.length }}/500
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
              </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="flex space-x-4 pt-6">
              <button
                type="button"
                @click="$emit('close')"
                class="flex-1 btn-ghost"
                :disabled="loading"
              >
                İptal
              </button>
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
                  Kaydediliyor...
                </template>
                <template v-else>
                  <CheckIcon class="w-5 h-5 mr-2" />
                  Değişiklikleri Kaydet
                </template>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import {
  XMarkIcon,
  ChevronDownIcon,
  CheckIcon
} from '@heroicons/vue/24/outline'
import { useToast } from 'vue-toastification'

// Props
const props = defineProps({
  character: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'save'])

// Composables
const toast = useToast()

// Reactive data
const loading = ref(false)
const showAdvanced = ref(false)

const form = reactive({
  name: '',
  relationship: '',
  tagline: '',
  personality_prompt: '',
  appearance_prompt: '',
  temperature: 0.7,
  max_tokens: 300,
  system_prompt: ''
})

// Computed properties
const isFormValid = computed(() => {
  return form.name.trim() && 
         form.relationship && 
         form.personality_prompt.trim().length >= 10
})

// Methods
const handleSave = async () => {
  if (!isFormValid.value) return
  
  try {
    loading.value = true
    
    const updatedData = {
      id: props.character.id,
      name: form.name.trim(),
      relationship: form.relationship,
      tagline: form.tagline.trim(),
      personality_prompt: form.personality_prompt.trim(),
      appearance_prompt: form.appearance_prompt.trim(),
      temperature: form.temperature,
      max_tokens: form.max_tokens,
      system_prompt: form.system_prompt.trim()
    }
    
    emit('save', updatedData)
    toast.success('Karakter başarıyla güncellendi!')
  } catch (error) {
    console.error('Failed to update character:', error)
    toast.error('Karakter güncellenemedi')
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  // Initialize form with character data
  Object.assign(form, {
    name: props.character.name || '',
    relationship: props.character.relationship || '',
    tagline: props.character.tagline || '',
    personality_prompt: props.character.personality_prompt || '',
    appearance_prompt: props.character.appearance_prompt || '',
    temperature: props.character.temperature || 0.7,
    max_tokens: props.character.max_tokens || 300,
    system_prompt: props.character.system_prompt || ''
  })
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
</style>