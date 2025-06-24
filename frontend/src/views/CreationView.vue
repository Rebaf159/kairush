<template>
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent mb-4">
        Doğrudan Yaratılış Seremonisi
      </h1>
      <p class="text-xl text-gray-300 max-w-2xl mx-auto">
        Hayalindeki yoldaşı birkaç kelimeyle tarif et. Yapay zeka teknolojimiz onu senin için yaratacak.
      </p>
    </div>
    
    <!-- Creation Form -->
    <div class="glass-dark rounded-2xl p-8 mb-8">
      <CreationForm 
        @submit="handleCreateCharacter"
        :loading="characterStore.loading"
      />
    </div>
    
    <!-- Tips Section -->
    <div class="glass-dark rounded-2xl p-8">
      <h3 class="text-xl font-semibold text-white mb-6 flex items-center">
        <LightBulbIcon class="w-6 h-6 text-yellow-400 mr-2" />
        Yaratım İpuçları
      </h3>
      
      <div class="grid md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <div class="border-l-4 border-primary-500 pl-4">
            <h4 class="font-semibold text-white mb-2">İsim Seçimi</h4>
            <p class="text-gray-400 text-sm">
              Karakterinin kişiliğini yansıtan, akılda kalıcı bir isim seç. Örnek: "Luna", "Kai", "Aria"
            </p>
          </div>
          
          <div class="border-l-4 border-secondary-500 pl-4">
            <h4 class="font-semibold text-white mb-2">İlişki Türü</h4>
            <p class="text-gray-400 text-sm">
              Karakterinle nasıl bir bağ kurmak istiyorsun? Arkadaş, mentor, romantik partner...
            </p>
          </div>
        </div>
        
        <div class="space-y-4">
          <div class="border-l-4 border-accent-500 pl-4">
            <h4 class="font-semibold text-white mb-2">Kişilik Tanımı</h4>
            <p class="text-gray-400 text-sm">
              Detaylı ol! "Neşeli, meraklı, biraz utangaç ama sıcakkanlı" gibi özellikler ekle.
            </p>
          </div>
          
          <div class="border-l-4 border-green-500 pl-4">
            <h4 class="font-semibold text-white mb-2">Görünüm</h4>
            <p class="text-gray-400 text-sm">
              Saç rengi, göz rengi, giyim tarzı gibi fiziksel özelliklerini tarif et.
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Examples Section -->
    <div class="mt-8">
      <h3 class="text-xl font-semibold text-white mb-6 text-center">
        Örnek Karakterler
      </h3>
      
      <div class="grid md:grid-cols-3 gap-6">
        <div 
          v-for="example in exampleCharacters" 
          :key="example.name"
          class="glass-dark rounded-xl p-6 cursor-pointer hover:bg-white/5 transition-all duration-300 group"
          @click="useExample(example)"
        >
          <div class="text-center mb-4">
            <div class="w-16 h-16 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl">{{ example.emoji }}</span>
            </div>
            <h4 class="font-semibold text-white group-hover:text-primary-400 transition-colors duration-300">
              {{ example.name }}
            </h4>
          </div>
          
          <div class="space-y-2 text-sm">
            <p class="text-gray-400">
              <span class="text-primary-400 font-medium">İlişki:</span> {{ example.relationship }}
            </p>
            <p class="text-gray-400">
              <span class="text-secondary-400 font-medium">Kişilik:</span> {{ example.personality.substring(0, 50) }}...
            </p>
          </div>
          
          <div class="mt-4 text-center">
            <span class="text-xs text-primary-400 group-hover:text-primary-300 transition-colors duration-300">
              Kullanmak için tıkla
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LightBulbIcon } from '@heroicons/vue/24/outline'
import { useCharacterStore } from '@/stores/character'
import CreationForm from '../components/CreationForm.vue'
import { useToast } from 'vue-toastification'

const router = useRouter()
const characterStore = useCharacterStore()
const toast = useToast()

// Example characters
const exampleCharacters = ref([
  {
    name: "Luna",
    emoji: "🌙",
    relationship: "Romantik Partner",
    personality: "Gizemli, büyüleyici ve derin. Gece gökyüzü kadar sonsuz hayal gücüne sahip. Sakin ama tutkulu, felsefi konuşmalar yapmayı seven biri.",
    appearance: "Gümüş rengi uzun saçlar, mavi gözler, zarif ve mistik bir görünüm. Genellikle koyu renkli, akıcı kıyafetler giyer."
  },
  {
    name: "Kai",
    emoji: "⚡",
    relationship: "En Yakın Arkadaş",
    personality: "Enerjik, maceracı ve her zaman pozitif. Yeni deneyimlere açık, cesur ve eğlenceli. Seni her zaman destekleyen ve motive eden biri.",
    appearance: "Kahverengi dalgalı saçlar, yeşil gözler, atletik yapı. Rahat ve spor giyim tarzını tercih eder, her zaman gülümser."
  },
  {
    name: "Aria",
    emoji: "🎭",
    relationship: "Mentor",
    personality: "Bilge, sabırlı ve anlayışlı. Sanat ve edebiyata tutkulu, derin konuşmalar yapmayı seven. Sana rehberlik etmeyi ve öğretmeyi seven biri.",
    appearance: "Kestane rengi saçlar, kahverengi gözler, zarif duruş. Klasik ve şık giyim tarzı, genellikle kitap okurken görülür."
  }
])

// Form reference
const creationFormRef = ref(null)

// Methods
const handleCreateCharacter = async (characterData) => {
  try {
    const newCharacter = await characterStore.createCharacter(characterData)
    
    toast.success(`${newCharacter.name} başarıyla yaratıldı! Şimdi onunla sohbet edebilirsin.`)
    
    // Yeni karakterle sohbet sayfasına yönlendir
    router.push(`/app/chat/${newCharacter.id}`)
  } catch (error) {
    console.error('Character creation failed:', error)
  }
}

const useExample = (example) => {
  // CreationForm bileşenine örnek verileri gönder
  // Bu işlevsellik CreationForm bileşeninde implement edilecek
  toast.info(`${example.name} örneği form alanlarına yüklendi!`)
  
  // Form alanlarını doldur (CreationForm bileşeninde expose edilen method)
  if (creationFormRef.value) {
    creationFormRef.value.fillForm(example)
  }
}
</script>