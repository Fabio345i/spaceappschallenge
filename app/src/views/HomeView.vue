<script setup>
import { ref, onMounted, watch } from 'vue'
import SearchBar from '@/components/SearchBar.vue'
import GlobeCesium from '@/components/GlobeCesium.vue'
import Tableaudebord from '@/components/Tableaudebord.vue'
import Calendar from '@/components/Calendar.vue'
import HourlyForecast from '@/components/HourlyForecast.vue'
import TutorialDriver from '@/components/tutorial/TutorialDriver.vue'
import Loading from '@/views/LoadingOverlay.vue'

const tutorial = ref(null)
import router from '@/router'

import axios from 'axios'
const disasterHeadlines = ref([])
const headlinesLoading = ref(true)

const target = ref(null)
const mobileMenuOpen = ref(false)
const favoritesOpen = ref(false)
const resetTrigger = ref(0)

const isAuthenticated = ref(!!localStorage.getItem("token"))

const favorites = ref([])

onMounted(async () => {
  if (!isAuthenticated.value) return
  try {
    const token = localStorage.getItem("token")
    const { data } = await axios.get("http://localhost:8000/auth/favorites", {
      headers: { Authorization: `Bearer ${token}` }
    })
    favorites.value = data
  } catch (err) {
    console.error("Failed to fetch favorites", err)
  }
})

async function addFavorite(location) {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }

  const name =
    location.city || 
    location.town || 
    location.village || 
    location.display_name || 
    `${location.lat.toFixed(2)}, ${location.lon.toFixed(2)}`

  const exists = favorites.value.some(f => f.name === name)
  if (exists) return

  const favorite = { name, lat: location.lat, lon: location.lon }

  try {
    const token = localStorage.getItem("token")
    await axios.post("http://localhost:8000/auth/favorites", favorite, {
      headers: { Authorization: `Bearer ${token}` }
    })
    favorites.value.push(favorite)
  } catch (err) {
    console.error("Failed to add favorite", err)
  }
}

function toggleFavorites() {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }
  favoritesOpen.value = !favoritesOpen.value
}

function selectFavorite(fav) {
  target.value = { lat: fav.lat, lon: fav.lon }
  favoritesOpen.value = false
}

function logout() {
  localStorage.removeItem("token")
  isAuthenticated.value = false
  router.push("/")
}

const selectedDate = ref(new Date())

function handleDateSelected(date) {
  selectedDate.value = date
}

function handleResetView() {
  resetTrigger.value++
}

function extractCoordinates(headline) {
  const regex = /(\d+\.?\d*)°([NS]),\s*(\d+\.?\d*)°([EW])/
  const match = headline.match(regex)
  
  if (match) {
    let lat = parseFloat(match[1])
    let lon = parseFloat(match[3])
    
    if (match[2] === 'S') lat = -lat
    if (match[4] === 'W') lon = -lon
    
    return { lat, lon }
  }
  return null
}

function handleHeadlineClick(headline) {
  const coords = extractCoordinates(headline)
  if (coords) {
    target.value = coords
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

async function fetchCatastrophesNaturelles() {
  try {
    const today = selectedDate.value.toISOString().split('T')[0]
    const response = await fetch(`http://localhost:8000/disasters/headlines?date=${today}&limit=20`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    disasterHeadlines.value = data.headlines || []
  } catch (error) {
    console.error('Error - Natural Disasters:', error)
    disasterHeadlines.value = ['Error loading disaster alerts']
  } finally {
    headlinesLoading.value = false
  }
}

onMounted(() => {
  fetchCatastrophesNaturelles()
})

watch(selectedDate, () => {
  headlinesLoading.value = true
  fetchCatastrophesNaturelles()
})

const isGlobalLoading = ref(false)
const loadingStates = ref({
  map: false,
  precipitation: false,
  weather: false,
  forecast: false
})

function startGlobalLoading() {
  isGlobalLoading.value = true
  loadingStates.value = {
    map: false,
    precipitation: false,
    weather: false,
    forecast: false
  }
  
  setTimeout(() => {
    markAsLoaded('map')
    markAsLoaded('precipitation')
    markAsLoaded('weather')
    markAsLoaded('forecast')
  }, 3000)
}

function markAsLoaded(module) {
  loadingStates.value[module] = true
  
  const allLoaded = Object.values(loadingStates.value).every(state => state)
  if (allLoaded) {
    setTimeout(() => {
      isGlobalLoading.value = false
    }, 500)
  }
}

function handleLocationSelected(location) {
  target.value = location
  startGlobalLoading()
}

</script>

<template>
  <Loading :is-loading="isGlobalLoading" :loading-states="loadingStates" />
  
  <TutorialDriver ref="tutorial" />
  
  <div class="flex flex-col h-screen w-full bg-black text-gray-100">
    <header class="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800">
      <nav class="max-w-full px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-4">
            <div>
              <h1 class="text-lg font-semibold text-white">NASA Weather</h1>
              <p class="text-xs text-gray-500">Earth Observation System</p>
            </div>
          </div>

          <div class="hidden md:flex items-center space-x-8">
            <a href="#" class="text-gray-400 hover:text-white transition-colors text-sm font-medium">Home</a>
            <button @click="tutorial?.startTutorial()" class="text-gray-400 hover:text-white transition-colors text-sm font-medium">Tutorial</button>
            
            <div class="relative">
              <button @click="toggleFavorites" class="text-gray-400 hover:text-white transition-colors flex items-center space-x-2 text-sm font-medium">
                <span>Favorites</span>
                <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': favoritesOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>

              <div v-if="favoritesOpen" class="absolute top-full mt-3 right-0 w-64 bg-gray-800 border border-gray-700 rounded-lg shadow-xl overflow-hidden">
                <div class="p-2">
                  <div v-for="fav in favorites" :key="fav.name" @click="selectFavorite(fav)" class="px-4 py-3 hover:bg-gray-700 cursor-pointer transition-colors rounded">
                    <div class="text-white text-sm font-medium">{{ fav.name }}</div>
                    <div class="text-gray-500 text-xs mt-0.5">{{ fav.lat.toFixed(2) }}° / {{ fav.lon.toFixed(2) }}°</div>
                  </div>
                </div>
              </div>
            </div>
            
            <a href="#" class="text-gray-400 hover:text-white transition-colors text-sm font-medium">Data</a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors text-sm font-medium">About</a>
            <button v-if="isAuthenticated" @click="logout" class="text-gray-400 hover:text-white transition-colors text-sm font-medium">Disconnect</button>
          </div>

          <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden text-gray-400 hover:text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
        </div>

        <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-800 py-3">
          <a href="#" class="block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded">Home</a>
          <a href="#" class="block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded">Favorites</a>
          <a href="#" class="block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded">Data</a>
          <a href="#" class="block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded">About</a>
        </div>
      </nav>
    </header>

    <div class="fixed top-16 left-0 right-0 z-40 bg-yellow-600 text-black overflow-hidden border-b-2 border-yellow-600">
      <div class="h-10 flex items-center">
        <div v-if="headlinesLoading" class="px-4 text-sm font-medium">Loading disaster alerts...</div>
        <div v-else class="ticker-wrapper">
          <div class="ticker-content">
            <span v-for="(headline, index) in disasterHeadlines" :key="index" class="ticker-item" @click="handleHeadlineClick(headline)">
              <span class="font-bold">ALERT:</span> {{ headline }}
            </span>
            <span v-for="(headline, index) in disasterHeadlines" :key="`dup-${index}`" class="ticker-item" @click="handleHeadlineClick(headline)">
              <span class="font-bold">ALERT:</span> {{ headline }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <main class="flex-1 flex pt-16 overflow-hidden">
      <aside class="w-96 flex-shrink-0 bg-gray-950 border-r border-gray-800 overflow-y-auto mt-10">
        <div class="p-6 space-y-6">
          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">Location Search</h2>
            <SearchBar @location-selected="handleLocationSelected" />
            <button v-if="isAuthenticated && target" @click="addFavorite(target)" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">+ Favorite</button>
            <p class="text-xs text-gray-600 mt-2">Search for any city, region, or coordinates worldwide</p>
          </div>

          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">Forecast Date</h2>
            <Calendar :selected-date="selectedDate" @date-selected="handleDateSelected" />
            <p class="text-xs text-gray-600 mt-2">Select a date to view historical or forecast data</p>
          </div>

          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">Weather Summary</h2>
            <Tableaudebord :location="target" :selected-date="selectedDate" @reset-view="handleResetView" />
          </div>

          <div class="pt-6 border-t border-gray-800">
            <p class="text-xs text-gray-600 leading-relaxed">
              Data provided by NASA's Earth Observing System satellites and Open-Meteo API. Updates every 1-3 hours based on satellite orbital patterns.
            </p>
          </div>
        </div>
      </aside>

      <div class="flex-1 flex flex-col overflow-hidden mt-10">
        <div class="border-b border-gray-800 bg-gray-950">
          <div class="px-6 py-4">
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">Hourly Forecast</h2>
            <HourlyForecast v-if="target" :selected-date="selectedDate" :latitude="target.lat" :longitude="target.lon" :location="`${target.lat}, ${target.lon}`" />
          </div>
        </div>

        <div class="flex justify-center items-center p-4">
          <div id="cesiumContainer" class="w-[400px] h-[400px]">
            <GlobeCesium :target="target" :reset-trigger="resetTrigger" :is-loading="isGlobalLoading" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.h-screen {
  height: 100vh;
}

#cesiumContainer {
  width: 100%;
  height: 100%;
}


.ticker-wrapper {
  width: 100%;
  overflow: hidden;
}

.ticker-content {
  display: flex;
  white-space: nowrap;
  animation: scroll 60s linear infinite;
}

.ticker-item {
  display: inline-block;
  padding: 0 3rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.ticker-item:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

@keyframes scroll {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

.ticker-content:hover {
  animation-play-state: paused;
}
</style>
