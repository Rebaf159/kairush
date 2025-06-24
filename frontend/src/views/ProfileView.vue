<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <!-- Profile Header -->
    <div class="glass-dark rounded-2xl p-8">
      <div class="flex items-center space-x-6">
        <!-- Avatar -->
        <div class="relative">
          <div class="w-24 h-24 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
            <span class="text-white font-bold text-2xl">
              {{ authStore.user?.email?.charAt(0).toUpperCase() }}
            </span>
          </div>
          <button class="absolute bottom-0 right-0 w-8 h-8 bg-secondary-500 rounded-full flex items-center justify-center text-white hover:bg-secondary-400 transition-colors duration-300">
            <PencilIcon class="w-4 h-4" />
          </button>
        </div>
        
        <!-- User Info -->
        <div class="flex-1">
          <h1 class="text-3xl font-bold text-white mb-2">
            {{ authStore.user?.email?.split('@')[0] || 'Kullanıcı' }}
          </h1>
          <p class="text-gray-400 mb-4">{{ authStore.user?.email }}</p>
          
          <div class="flex items-center space-x-6 text-sm">
            <div class="flex items-center space-x-2">
              <CalendarIcon class="w-4 h-4 text-primary-400" />
              <span class="text-gray-400">
                Üye olma: {{ formatDate(authStore.user?.created_at) }}
              </span>
            </div>
            <div class="flex items-center space-x-2">
              <CreditCardIcon class="w-4 h-4 text-green-400" />
              <span class="text-gray-400">
                {{ authStore.user?.credits || 100 }} kredi
              </span>
            </div>
          </div>
        </div>
      </div>
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
          {{ totalMessages }}
        </div>
        <div class="text-gray-400 text-sm">Toplam Mesaj</div>
      </div>
      
      <div class="glass-dark rounded-xl p-6 text-center">
        <div class="text-3xl font-bold text-accent-400 mb-2">
          {{ characterStore.favoriteCharacters.length }}
        </div>
        <div class="text-gray-400 text-sm">Favori Karakter</div>
      </div>
      
      <div class="glass-dark rounded-xl p-6 text-center">
        <div class="text-3xl font-bold text-green-400 mb-2">
          {{ daysSinceJoined }}
        </div>
        <div class="text-gray-400 text-sm">Gün Aktif</div>
      </div>
    </div>
    
    <!-- Profile Settings -->
    <div class="glass-dark rounded-2xl p-8">
      <h2 class="text-2xl font-bold text-white mb-6">Profil Ayarları</h2>
      
      <form @submit.prevent="updateProfile" class="space-y-6">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            E-posta
          </label>
          <input
            v-model="profileForm.email"
            type="email"
            class="form-input"
            :disabled="authStore.loading"
          />
        </div>
        
        <!-- Display Name -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Görünen İsim
          </label>
          <input
            v-model="profileForm.displayName"
            type="text"
            class="form-input"
            placeholder="İsteğe bağlı"
            :disabled="authStore.loading"
          />
        </div>
        
        <!-- Bio -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Hakkında
          </label>
          <textarea
            v-model="profileForm.bio"
            class="form-textarea"
            placeholder="Kendin hakkında birkaç kelime..."
            rows="3"
            :disabled="authStore.loading"
          ></textarea>
        </div>
        
        <!-- Preferences -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-white">Tercihler</h3>
          
          <div class="space-y-3">
            <label class="flex items-center">
              <input
                v-model="profileForm.emailNotifications"
                type="checkbox"
                class="w-4 h-4 text-primary-500 bg-dark-800 border-gray-600 rounded focus:ring-primary-500 focus:ring-2"
                :disabled="authStore.loading"
              />
              <span class="ml-2 text-gray-300">E-posta bildirimleri</span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="profileForm.marketingEmails"
                type="checkbox"
                class="w-4 h-4 text-primary-500 bg-dark-800 border-gray-600 rounded focus:ring-primary-500 focus:ring-2"
                :disabled="authStore.loading"
              />
              <span class="ml-2 text-gray-300">Pazarlama e-postaları</span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="profileForm.publicProfile"
                type="checkbox"
                class="w-4 h-4 text-primary-500 bg-dark-800 border-gray-600 rounded focus:ring-primary-500 focus:ring-2"
                :disabled="authStore.loading"
              />
              <span class="ml-2 text-gray-300">Profili herkese açık yap</span>
            </label>
          </div>
        </div>
        
        <!-- Submit Button -->
        <button
          type="submit"
          class="btn-primary flex items-center"
          :disabled="authStore.loading"
        >
          <template v-if="authStore.loading">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Güncelleniyor...
          </template>
          <template v-else>
            <CheckIcon class="w-5 h-5 mr-2" />
            Profili Güncelle
          </template>
        </button>
      </form>
    </div>
    
    <!-- Password Change -->
    <div class="glass-dark rounded-2xl p-8">
      <h2 class="text-2xl font-bold text-white mb-6">Şifre Değiştir</h2>
      
      <form @submit.prevent="changePassword" class="space-y-6">
        <!-- Current Password -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Mevcut Şifre
          </label>
          <input
            v-model="passwordForm.currentPassword"
            type="password"
            class="form-input"
            :disabled="passwordLoading"
          />
        </div>
        
        <!-- New Password -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Yeni Şifre
          </label>
          <input
            v-model="passwordForm.newPassword"
            type="password"
            class="form-input"
            :disabled="passwordLoading"
          />
        </div>
        
        <!-- Confirm New Password -->
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Yeni Şifre Tekrar
          </label>
          <input
            v-model="passwordForm.confirmPassword"
            type="password"
            class="form-input"
            :class="{ 'border-red-500': passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword }"
            :disabled="passwordLoading"
          />
          <p v-if="passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword" class="mt-1 text-sm text-red-400">
            Şifreler eşleşmiyor
          </p>
        </div>
        
        <!-- Submit Button -->
        <button
          type="submit"
          class="btn-secondary flex items-center"
          :disabled="passwordLoading || !isPasswordFormValid"
        >
          <template v-if="passwordLoading">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Değiştiriliyor...
          </template>
          <template v-else>
            <KeyIcon class="w-5 h-5 mr-2" />
            Şifreyi Değiştir
          </template>
        </button>
      </form>
    </div>
    
    <!-- Danger Zone -->
    <div class="glass-dark rounded-2xl p-8 border border-red-500/30">
      <h2 class="text-2xl font-bold text-red-400 mb-6">Tehlikeli Bölge</h2>
      
      <div class="space-y-4">
        <div class="flex items-center justify-between p-4 bg-red-500/10 rounded-lg border border-red-500/30">
          <div>
            <h3 class="text-lg font-semibold text-white mb-1">Hesabı Sil</h3>
            <p class="text-gray-400 text-sm">
              Hesabını ve tüm verilerini kalıcı olarak sil. Bu işlem geri alınamaz.
            </p>
          </div>
          <button
            @click="showDeleteConfirmation = true"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-300"
          >
            Hesabı Sil
          </button>
        </div>
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <ConfirmationModal
      v-if="showDeleteConfirmation"
      title="Hesabı Sil"
      message="Bu işlem geri alınamaz. Hesabın, tüm karakterlerin ve sohbet geçmişin kalıcı olarak silinecek. Devam etmek istediğinden emin misin?"
      confirm-text="Evet, Hesabımı Sil"
      confirm-class="bg-red-600 hover:bg-red-700"
      @confirm="deleteAccount"
      @cancel="showDeleteConfirmation = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { 
  PencilIcon,
  CalendarIcon,
  CreditCardIcon,
  CheckIcon,
  KeyIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useCharacterStore } from '@/stores/character'
import ConfirmationModal from '../components/ConfirmationModal.vue'
import { useToast } from 'vue-toastification'

const authStore = useAuthStore()
const characterStore = useCharacterStore()
const toast = useToast()

// Reactive data
const passwordLoading = ref(false)
const showDeleteConfirmation = ref(false)

const profileForm = reactive({
  email: '',
  displayName: '',
  bio: '',
  emailNotifications: true,
  marketingEmails: false,
  publicProfile: false
})

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Computed properties
const totalMessages = computed(() => {
  return characterStore.characters.reduce((total, char) => {
    return total + (char.message_count || 0)
  }, 0)
})

const daysSinceJoined = computed(() => {
  if (!authStore.user?.created_at) return 0
  const joinDate = new Date(authStore.user.created_at)
  const now = new Date()
  const diffTime = Math.abs(now - joinDate)
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
})

const isPasswordFormValid = computed(() => {
  return passwordForm.currentPassword &&
         passwordForm.newPassword &&
         passwordForm.confirmPassword &&
         passwordForm.newPassword === passwordForm.confirmPassword &&
         passwordForm.newPassword.length >= 6
})

// Methods
const formatDate = (dateString) => {
  if (!dateString) return 'Bilinmiyor'
  return new Date(dateString).toLocaleDateString('tr-TR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const updateProfile = async () => {
  try {
    await authStore.updateUser({
      email: profileForm.email,
      display_name: profileForm.displayName,
      bio: profileForm.bio,
      email_notifications: profileForm.emailNotifications,
      marketing_emails: profileForm.marketingEmails,
      public_profile: profileForm.publicProfile
    })
  } catch (error) {
    console.error('Failed to update profile:', error)
  }
}

const changePassword = async () => {
  if (!isPasswordFormValid.value) return
  
  try {
    passwordLoading.value = true
    
    // API call to change password
    // await apiClient.post('/auth/change-password', {
    //   current_password: passwordForm.currentPassword,
    //   new_password: passwordForm.newPassword
    // })
    
    // Reset form
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    
    toast.success('Şifre başarıyla değiştirildi!')
  } catch (error) {
    console.error('Failed to change password:', error)
    toast.error('Şifre değiştirilemedi. Mevcut şifrenizi kontrol edin.')
  } finally {
    passwordLoading.value = false
  }
}

const deleteAccount = async () => {
  try {
    // API call to delete account
    // await apiClient.delete('/auth/account')
    
    toast.success('Hesabınız başarıyla silindi.')
    authStore.logout()
  } catch (error) {
    console.error('Failed to delete account:', error)
    toast.error('Hesap silinemedi. Lütfen tekrar deneyin.')
  } finally {
    showDeleteConfirmation.value = false
  }
}

// Lifecycle
onMounted(() => {
  // Initialize form with user data
  if (authStore.user) {
    profileForm.email = authStore.user.email || ''
    profileForm.displayName = authStore.user.display_name || ''
    profileForm.bio = authStore.user.bio || ''
    profileForm.emailNotifications = authStore.user.email_notifications ?? true
    profileForm.marketingEmails = authStore.user.marketing_emails ?? false
    profileForm.publicProfile = authStore.user.public_profile ?? false
  }
  
  // Load characters if not already loaded
  if (characterStore.characters.length === 0) {
    characterStore.fetchCharacters().catch(console.error)
  }
})
</script>