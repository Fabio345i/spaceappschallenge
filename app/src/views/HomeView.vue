<script setup>
import { ref } from 'vue'
import SearchBar from '@/components/SearchBar.vue'
import GlobeCesium from '@/components/GlobeCesium.vue'
import Tableaudebord from '@/components/Tableaudebord.vue'

const target = ref(null)
const mobileMenuOpen = ref(false)
const favoritesOpen = ref(false)

const favorites = ref([
  { name: 'New York, USA', lat: 40.7128, lon: -74.0060 },
  { name: 'Paris, France', lat: 48.8566, lon: 2.3522 },
  { name: 'Tokyo, Japan', lat: 35.6762, lon: 139.6503 }
])

function selectFavorite(fav) {
  target.value = { lat: fav.lat, lon: fav.lon }
  favoritesOpen.value = false
}
</script>

<template>
  <div class="flex flex-col h-screen w-full bg-black text-gray-100">
    
    <header class="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800">
      <nav class="max-w-full px-6">
        <div class="flex items-center justify-between h-16">
          
          <div class="flex items-center space-x-3">
            <span class="text-xl font-semibold text-white tracking-tight">
              NASA Weather
            </span>
          </div>

          <div class="hidden md:flex items-center space-x-8">
            <a href="#" class="text-gray-300 hover:text-white transition-colors font-medium">
              Home
            </a>
            
            <div class="relative">
              <button 
                @click="favoritesOpen = !favoritesOpen"
                class="text-gray-300 hover:text-white transition-colors flex items-center space-x-2 font-medium"
              >
                <span>Favoris</span>
                <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': favoritesOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>
              
              <div 
                v-if="favoritesOpen"
                class="absolute top-full mt-2 right-0 w-64 bg-gray-800 border border-gray-700 rounded-lg shadow-2xl overflow-hidden"
              >
                <div class="py-2">
                  <div 
                    v-for="fav in favorites" 
                    :key="fav.name"
                    @click="selectFavorite(fav)"
                    class="px-4 py-3 hover:bg-gray-700 cursor-pointer transition-colors border-b border-gray-700 last:border-b-0"
                  >
                    <div class="text-white text-sm font-medium">{{ fav.name }}</div>
                    <div class="text-gray-500 text-xs">{{ fav.lat.toFixed(4) }}° / {{ fav.lon.toFixed(4) }}°</div>
                  </div>
                </div>
                <div class="border-t border-gray-700 px-4 py-2 bg-gray-900/50">
                  <button class="text-gray-400 hover:text-white text-xs transition-colors">
                    + Add to favorites
                  </button>
                </div>
              </div>
            </div>
            
            <a href="#" class="text-gray-300 hover:text-white transition-colors font-medium">
              Data
            </a>
            <a href="#" class="text-gray-300 hover:text-white transition-colors font-medium">
              About
            </a>
          </div>

          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden text-gray-300 hover:text-white text-2xl"
          >
            <span v-if="mobileMenuOpen">✕</span>
            <span v-else>☰</span>
          </button>
        </div>

        <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-800 py-4 space-y-3">
          <a href="#" class="block text-gray-300 hover:text-white transition-colors font-medium">
            Home
          </a>
          <a href="#" class="block text-gray-300 hover:text-white transition-colors font-medium">
            Favoris
          </a>
          <a href="#" class="block text-gray-300 hover:text-white transition-colors font-medium">
            Data
          </a>
          <a href="#" class="block text-gray-300 hover:text-white transition-colors font-medium">
            About
          </a>
        </div>
      </nav>
    </header>

    <main class="flex-1 flex min-h-0 relative pt-16"> 
      
      <div class="relative z-10 p-4 w-full sm:w-96 flex-shrink-0 bg-black/40 backdrop-blur-sm">
        <SearchBar @location-selected="target = $event" class="mb-4" />
        <Tableaudebord :location="target" class="overflow-y-auto max-h-full" />
      </div>

      <div class="flex-1 min-w-0 relative">
        <GlobeCesium :target="target" />
      </div>
      
    </main>
  </div>
</template>

<style scoped>
.h-screen {
  height: 100vh;
}
</style>