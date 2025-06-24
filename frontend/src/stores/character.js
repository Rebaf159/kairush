import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/services/apiClient'
import { useToast } from 'vue-toastification'

export const useCharacterStore = defineStore('character', () => {
  const toast = useToast()
  
  // State
  const characters = ref([])
  const activeCharacter = ref(null)
  const chatHistory = ref([])
  const loading = ref(false)
  const chatLoading = ref(false)
  
  // Getters
  const favoriteCharacters = computed(() => 
    characters.value.filter(char => char.is_favorite)
  )
  
  const recentCharacters = computed(() => 
    characters.value
      .filter(char => char.last_chat_at)
      .sort((a, b) => new Date(b.last_chat_at) - new Date(a.last_chat_at))
      .slice(0, 5)
  )
  
  // Actions
  const fetchCharacters = async () => {
    try {
      loading.value = true
      const response = await apiClient.get('/characters')
      characters.value = response.data
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Karakterler yüklenirken bir hata oluştu'
      toast.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  const createCharacter = async (characterData) => {
    try {
      loading.value = true
      const response = await apiClient.post('/creation/direct', characterData)
      
      const newCharacter = response.data
      characters.value.unshift(newCharacter)
      
      toast.success(`${newCharacter.name} başarıyla yaratıldı!`)
      return newCharacter
    } catch (error) {
      const message = error.response?.data?.detail || 'Karakter yaratılırken bir hata oluştu'
      toast.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  const getCharacter = async (characterId) => {
    try {
      const response = await apiClient.get(`/characters/${characterId}`)
      activeCharacter.value = response.data
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Karakter bilgileri alınamadı'
      toast.error(message)
      throw error
    }
  }
  
  const updateCharacter = async (characterId, updates) => {
    try {
      const response = await apiClient.put(`/characters/${characterId}`, updates)
      
      // Listedeki karakteri güncelle
      const index = characters.value.findIndex(char => char.id === characterId)
      if (index !== -1) {
        characters.value[index] = response.data
      }
      
      // Aktif karakterse onu da güncelle
      if (activeCharacter.value?.id === characterId) {
        activeCharacter.value = response.data
      }
      
      toast.success('Karakter başarıyla güncellendi!')
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Karakter güncellenirken bir hata oluştu'
      toast.error(message)
      throw error
    }
  }
  
  const deleteCharacter = async (characterId) => {
    try {
      await apiClient.delete(`/characters/${characterId}`)
      
      // Listeden kaldır
      characters.value = characters.value.filter(char => char.id !== characterId)
      
      // Aktif karakterse temizle
      if (activeCharacter.value?.id === characterId) {
        activeCharacter.value = null
        chatHistory.value = []
      }
      
      toast.success('Karakter başarıyla silindi!')
    } catch (error) {
      const message = error.response?.data?.detail || 'Karakter silinirken bir hata oluştu'
      toast.error(message)
      throw error
    }
  }
  
  const toggleFavorite = async (characterId) => {
    try {
      const character = characters.value.find(char => char.id === characterId)
      if (!character) return
      
      const response = await apiClient.post(`/characters/${characterId}/favorite`)
      
      // Listedeki karakteri güncelle
      const index = characters.value.findIndex(char => char.id === characterId)
      if (index !== -1) {
        characters.value[index].is_favorite = response.data.is_favorite
      }
      
      // Aktif karakterse onu da güncelle
      if (activeCharacter.value?.id === characterId) {
        activeCharacter.value.is_favorite = response.data.is_favorite
      }
      
      const message = response.data.is_favorite 
        ? 'Favorilere eklendi!' 
        : 'Favorilerden çıkarıldı!'
      toast.success(message)
      
      return response.data
    } catch (error) {
      const message = error.response?.data?.detail || 'Favori durumu değiştirilirken bir hata oluştu'
      toast.error(message)
      throw error
    }
  }
  
  const sendMessage = async (characterId, message) => {
    try {
      chatLoading.value = true
      
      // Kullanıcı mesajını hemen ekle
      const userMessage = {
        id: Date.now(),
        content: message,
        is_user: true,
        timestamp: new Date().toISOString()
      }
      chatHistory.value.push(userMessage)
      
      const response = await apiClient.post('/chat', {
        character_id: characterId,
        message: message
      })
      
      // AI yanıtını ekle
      const aiMessage = {
        id: Date.now() + 1,
        content: response.data.response,
        is_user: false,
        timestamp: new Date().toISOString()
      }
      chatHistory.value.push(aiMessage)
      
      // Son sohbet zamanını güncelle
      const character = characters.value.find(char => char.id === characterId)
      if (character) {
        character.last_chat_at = new Date().toISOString()
      }
      
      return response.data
    } catch (error) {
      // Hata durumunda kullanıcı mesajını kaldır
      chatHistory.value = chatHistory.value.filter(msg => msg.id !== userMessage.id)
      
      const message = error.response?.data?.detail || 'Mesaj gönderilirken bir hata oluştu'
      toast.error(message)
      throw error
    } finally {
      chatLoading.value = false
    }
  }
  
  const loadChatHistory = async (characterId) => {
    try {
      const response = await apiClient.get(`/characters/${characterId}/chat-history`)
      chatHistory.value = response.data
      return response.data
    } catch (error) {
      console.error('Sohbet geçmişi yüklenemedi:', error)
      chatHistory.value = []
    }
  }
  
  const clearChatHistory = () => {
    chatHistory.value = []
  }
  
  const setActiveCharacter = (character) => {
    activeCharacter.value = character
  }
  
  return {
    // State
    characters,
    activeCharacter,
    chatHistory,
    loading,
    chatLoading,
    
    // Getters
    favoriteCharacters,
    recentCharacters,
    
    // Actions
    fetchCharacters,
    createCharacter,
    getCharacter,
    updateCharacter,
    deleteCharacter,
    toggleFavorite,
    sendMessage,
    loadChatHistory,
    clearChatHistory,
    setActiveCharacter
  }
})