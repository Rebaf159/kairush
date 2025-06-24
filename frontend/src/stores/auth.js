import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/services/apiClient'
import router from '@/router'
import { useToast } from 'vue-toastification'

export const useAuthStore = defineStore('auth', () => {
  const toast = useToast()
  
  // State
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const loading = ref(false)
  
  // Getters
  const isLoggedIn = computed(() => !!token.value)
  
  // Actions
  const login = async (credentials) => {
    try {
      loading.value = true
      const response = await apiClient.post('/auth/login', credentials)
      
      token.value = response.data.access_token
      user.value = response.data.user
      
      localStorage.setItem('token', token.value)
      
      toast.success('Başarıyla giriş yaptınız!')
      router.push('/app/dashboard')
      
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Giriş yapılırken bir hata oluştu'
      toast.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  const register = async (userData) => {
    try {
      loading.value = true
      const response = await apiClient.post('/auth/register', userData)
      
      token.value = response.data.access_token
      user.value = response.data.user
      
      localStorage.setItem('token', token.value)
      
      toast.success('Hesabınız başarıyla oluşturuldu!')
      router.push('/app/dashboard')
      
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Kayıt olurken bir hata oluştu'
      toast.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    
    toast.info('Başarıyla çıkış yaptınız')
    router.push('/')
  }
  
  const fetchUser = async () => {
    try {
      const response = await apiClient.get('/auth/me')
      user.value = response.data
      return response.data
    } catch (error) {
      console.error('Kullanıcı bilgileri alınamadı:', error)
      logout()
      throw error
    }
  }
  
  const initializeAuth = async () => {
    if (token.value && !user.value) {
      try {
        await fetchUser()
      } catch (error) {
        // Token geçersizse temizle
        logout()
      }
    }
  }
  
  const updateUser = async (userData) => {
    try {
      loading.value = true
      const response = await apiClient.put('/auth/profile', userData)
      user.value = response.data
      
      toast.success('Profil başarıyla güncellendi!')
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Profil güncellenirken bir hata oluştu'
      toast.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  return {
    // State
    token,
    user,
    loading,
    
    // Getters
    isLoggedIn,
    
    // Actions
    login,
    register,
    logout,
    fetchUser,
    initializeAuth,
    updateUser
  }
})