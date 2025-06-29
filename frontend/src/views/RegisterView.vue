<template>
  <div>
    <!-- Form Header -->
    <div class="text-center mb-6">
      <h2 class="text-2xl font-bold text-white mb-2">Hesap Oluştur</h2>
      <p class="text-gray-400">Yolculuğuna başla ve ilk yoldaşını yarat</p>
    </div>
    
    <!-- Register Form -->
    <form @submit.prevent="handleRegister" class="space-y-6">
      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
          E-posta
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          class="form-input"
          placeholder="ornek@email.com"
          :disabled="authStore.loading"
        />
      </div>
      
      <!-- Password -->
      <div>
        <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
          Şifre
        </label>
        <div class="relative">
          <input
            id="password"
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            required
            class="form-input pr-12"
            placeholder="••••••••"
            :disabled="authStore.loading"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white transition-colors duration-300"
            :disabled="authStore.loading"
          >
            <EyeIcon v-if="!showPassword" class="w-5 h-5" />
            <EyeSlashIcon v-else class="w-5 h-5" />
          </button>
        </div>
        <div class="mt-2">
          <div class="flex items-center space-x-2 text-xs">
            <div class="flex-1 h-1 bg-gray-700 rounded">
              <div 
                class="h-1 rounded transition-all duration-300"
                :class="passwordStrengthColor"
                :style="{ width: passwordStrengthWidth }"
              ></div>
            </div>
            <span :class="passwordStrengthColor" class="font-medium">
              {{ passwordStrengthText }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Confirm Password -->
      <div>
        <label for="confirmPassword" class="block text-sm font-medium text-gray-300 mb-2">
          Şifre Tekrarı
        </label>
        <div class="relative">
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            required
            class="form-input pr-12"
            :class="{ 'border-red-500': form.confirmPassword && form.password !== form.confirmPassword }"
            placeholder="••••••••"
            :disabled="authStore.loading"
          />
          <button
            type="button"
            @click="showConfirmPassword = !showConfirmPassword"
            class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white transition-colors duration-300"
            :disabled="authStore.loading"
          >
            <EyeIcon v-if="!showConfirmPassword" class="w-5 h-5" />
            <EyeSlashIcon v-else class="w-5 h-5" />
          </button>
        </div>
        <p v-if="form.confirmPassword && form.password !== form.confirmPassword" class="mt-1 text-sm text-red-400">
          Şifreler eşleşmiyor
        </p>
      </div>
      
      <!-- Terms and Privacy -->
      <div>
        <label class="flex items-start">
          <input
            v-model="form.acceptTerms"
            type="checkbox"
            required
            class="w-4 h-4 text-primary-500 bg-dark-800 border-gray-600 rounded focus:ring-primary-500 focus:ring-2 mt-1"
            :disabled="authStore.loading"
          />
          <span class="ml-2 text-sm text-gray-300">
            <a href="#" class="text-primary-400 hover:text-primary-300 transition-colors duration-300">Kullanım Şartları</a>
            ve 
            <a href="#" class="text-primary-400 hover:text-primary-300 transition-colors duration-300">Gizlilik Politikası</a>'nı
            okudum ve kabul ediyorum.
          </span>
        </label>
      </div>
      
      <!-- Marketing Emails -->
      <div>
        <label class="flex items-center">
          <input
            v-model="form.acceptMarketing"
            type="checkbox"
            class="w-4 h-4 text-primary-500 bg-dark-800 border-gray-600 rounded focus:ring-primary-500 focus:ring-2"
            :disabled="authStore.loading"
          />
          <span class="ml-2 text-sm text-gray-300">
            Yeni özellikler ve güncellemeler hakkında e-posta almak istiyorum.
          </span>
        </label>
      </div>
      
      <!-- Submit Button -->
      <button
        type="submit"
        class="w-full btn-primary flex items-center justify-center"
        :disabled="authStore.loading || !isFormValid"
      >
        <template v-if="authStore.loading">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Hesap oluşturuluyor...
        </template>
        <template v-else>
          <UserPlusIcon class="w-5 h-5 mr-2" />
          Hesap Oluştur
        </template>
      </button>
    </form>
    
    <!-- Divider -->
    <div class="mt-6 mb-6">
      <div class="relative">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-600"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-dark-900 text-gray-400">veya</span>
        </div>
      </div>
    </div>
    
    <!-- Social Register -->
    <div class="space-y-3">
      <button
        type="button"
        class="w-full flex items-center justify-center px-4 py-3 border border-gray-600 rounded-lg text-gray-300 hover:bg-gray-800 hover:border-gray-500 transition-all duration-300"
        disabled
      >
        <svg class="w-5 h-5 mr-3" viewBox="0 0 24 24">
          <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
          <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        Google ile Kayıt Ol
        <span class="ml-2 text-xs text-gray-500">(Yakında)</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { EyeIcon, EyeSlashIcon, UserPlusIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
  acceptMarketing: false
})

// Password strength calculation
const passwordStrength = computed(() => {
  const password = form.password
  if (!password) return 0
  
  let score = 0
  if (password.length >= 8) score++
  if (/[a-z]/.test(password)) score++
  if (/[A-Z]/.test(password)) score++
  if (/[0-9]/.test(password)) score++
  if (/[^A-Za-z0-9]/.test(password)) score++
  
  return score
})

const passwordStrengthWidth = computed(() => {
  return `${(passwordStrength.value / 5) * 100}%`
})

const passwordStrengthColor = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 1) return 'text-red-400'
  if (strength <= 2) return 'text-orange-400'
  if (strength <= 3) return 'text-yellow-400'
  if (strength <= 4) return 'text-blue-400'
  return 'text-green-400'
})

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value
  if (strength <= 1) return 'Zayıf'
  if (strength <= 2) return 'Orta'
  if (strength <= 3) return 'İyi'
  if (strength <= 4) return 'Güçlü'
  return 'Çok Güçlü'
})

const isFormValid = computed(() => {
  return form.email && 
         form.password && 
         form.confirmPassword && 
         form.password === form.confirmPassword && 
         form.acceptTerms &&
         passwordStrength.value >= 2
})

const handleRegister = async () => {
  if (!isFormValid.value) return
  
  try {
    await authStore.register({
      email: form.email,
      password: form.password,
      accept_marketing: form.acceptMarketing
    })
  } catch (error) {
    console.error('Register error:', error)
  }
}
</script>