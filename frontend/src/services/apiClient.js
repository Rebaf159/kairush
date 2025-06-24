import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

// API client oluştur
const apiClient = axios.create({
  baseURL: "http://localhost:8010",
  timeout: 10000,
});

// Request interceptor - her isteğe token ekle
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - hata yönetimi
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const toast = useToast()
    
    // 401 Unauthorized - Token geçersiz
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      toast.error('Oturum süreniz doldu. Lütfen tekrar giriş yapın.')
      return Promise.reject(error)
    }
    
    // 403 Forbidden
    if (error.response?.status === 403) {
      toast.error('Bu işlem için yetkiniz bulunmuyor.')
      return Promise.reject(error)
    }
    
    // 404 Not Found
    if (error.response?.status === 404) {
      toast.error('Aradığınız kaynak bulunamadı.')
      return Promise.reject(error)
    }
    
    // 422 Validation Error
    if (error.response?.status === 422) {
      const validationErrors = error.response.data?.detail
      if (Array.isArray(validationErrors)) {
        validationErrors.forEach(err => {
          toast.error(`${err.loc?.join(' → ') || 'Hata'}: ${err.msg}`)
        })
      } else {
        toast.error('Girilen bilgilerde hata var. Lütfen kontrol edin.')
      }
      return Promise.reject(error)
    }
    
    // 429 Too Many Requests
    if (error.response?.status === 429) {
      toast.error('Çok fazla istek gönderdiniz. Lütfen biraz bekleyin.')
      return Promise.reject(error)
    }
    
    // 500 Internal Server Error
    if (error.response?.status >= 500) {
      toast.error('Sunucu hatası oluştu. Lütfen daha sonra tekrar deneyin.')
      return Promise.reject(error)
    }
    
    // Network Error
    if (error.code === 'NETWORK_ERROR' || !error.response) {
      toast.error('Bağlantı hatası. İnternet bağlantınızı kontrol edin.')
      return Promise.reject(error)
    }
    
    // Timeout Error
    if (error.code === 'ECONNABORTED') {
      toast.error('İstek zaman aşımına uğradı. Lütfen tekrar deneyin.')
      return Promise.reject(error)
    }
    
    // Diğer hatalar
    const message = error.response?.data?.detail || 'Beklenmeyen bir hata oluştu.'
    toast.error(message)
    
    return Promise.reject(error)
  }
)

export default apiClient