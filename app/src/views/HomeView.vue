<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import SearchBar from '@/components/SearchBar.vue'
import GlobeCesium from '@/components/GlobeCesium.vue'
import Tableaudebord from '@/components/Tableaudebord.vue'
import Calendar from '@/components/Calendar.vue'
import HourlyForecast from '@/components/HourlyForecast.vue'
import TutorialDriver from '@/components/tutorial/TutorialDriver.vue'
import LoginPopover from '@/components/LoginPopover.vue'
import RegisterPopover from '@/components/RegisterPopover.vue'
import Confidence from '@/components/Confidence.vue'
const tutorialOpen = ref(true)

import AboutPopover from '@/components/AboutPopover.vue'

const showAboutPopover = ref(false)
function openAbout() {
  showAboutPopover.value = true
}

const isFuturePrediction = computed(() => {
  if (!selectedDate.value) return null
  const today = new Date()
  const selected = new Date(selectedDate.value)
  return selected > today
})

const k = 0.001
const confiance = computed(() => {
  if (!selectedDate.value) return null
  if (!isFuturePrediction.value) return 100

  const today = new Date()
  const selected = new Date(selectedDate.value)
  const joursFuturs = Math.max(0, Math.ceil((selected - today) / (1000 * 60 * 60 * 24)))
  return Math.round(80 * Math.exp(-k * (joursFuturs - 1)))
})

const tutorial = ref(null)
import router from '@/router'
import axios from 'axios'

const disasterHeadlines = ref([])
const headlinesLoading = ref(true)
const target = ref(null)
const mobileMenuOpen = ref(false)
const favoritesOpen = ref(false)
const resetTrigger = ref(0)
const isAuthenticated = ref(!!localStorage.getItem('token'))
const favorites = ref([])
const favoriteAdded = ref(false)
const logoutLoading = ref(false)

// Popovers states
const showLoginPopover = ref(false)
const showRegisterPopover = ref(false)

const isCurrentLocationFavorite = computed(() => {
  if (!target.value || !favorites.value.length) return false

  const name =
    target.value.city ||
    target.value.town ||
    target.value.village ||
    target.value.display_name ||
    `${target.value.lat.toFixed(2)}, ${target.value.lon.toFixed(2)}`

  return favorites.value.some((f) => f.name === name)
})

onMounted(async () => {
  if (!isAuthenticated.value) return
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://localhost:8000/auth/favorites', {
      headers: { Authorization: `Bearer ${token}` },
    })
    favorites.value = data
  } catch (err) {
    console.error('Failed to fetch favorites', err)
  }
})

function openLogin() {
  showLoginPopover.value = true
  showRegisterPopover.value = false
}

function openRegister() {
  showRegisterPopover.value = true
  showLoginPopover.value = false
}

async function handleLoginSuccess() {
  isAuthenticated.value = true
  try {
    const token = localStorage.getItem('token')
    const { data } = await axios.get('http://localhost:8000/auth/favorites', {
      headers: { Authorization: `Bearer ${token}` },
    })
    favorites.value = data
  } catch (err) {
    console.error('Failed to fetch favorites', err)
  }
}

async function addFavorite(location) {
  if (!isAuthenticated.value) {
    openLogin()
    return
  }

  // Essayer d'obtenir un nom descriptif
  let name =
    location.city ||
    location.town ||
    location.village ||
    location.municipality ||
    location.county ||
    location.state ||
    location.country

  // Si toujours pas de nom, utiliser display_name s'il existe
  if (!name && location.display_name) {
    name = location.display_name
  }

  // En dernier recours, utiliser les coordonnées
  if (!name) {
    name = `${location.lat.toFixed(2)}°, ${location.lon.toFixed(2)}°`
  }

  const exists = favorites.value.some((f) => f.name === name)
  if (exists) return

  const favorite = { name, lat: location.lat, lon: location.lon }

  try {
    const token = localStorage.getItem('token')
    await axios.post('http://localhost:8000/auth/favorites', favorite, {
      headers: { Authorization: `Bearer ${token}` },
    })
    favorites.value.push(favorite)

    favoriteAdded.value = true
    setTimeout(() => {
      favoriteAdded.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to add favorite', err)
  }
}

function toggleFavorites() {
  if (!isAuthenticated.value) {
    openLogin()
    return
  }
  favoritesOpen.value = !favoritesOpen.value
}

function selectFavorite(fav) {
  target.value = { lat: fav.lat, lon: fav.lon }
  favoritesOpen.value = false
}

function logout() {
  logoutLoading.value = true
  setTimeout(() => {
    localStorage.removeItem('token')
    isAuthenticated.value = false
    favorites.value = []
    favoritesOpen.value = false
    logoutLoading.value = false
    router.push('/')
  }, 300)
}

function handleClickOutside(event) {
  const favoritesButton = event.target.closest('[data-favorites-button]')
  const favoritesDropdown = event.target.closest('[data-favorites-dropdown]')
  if (!favoritesButton && !favoritesDropdown) {
    favoritesOpen.value = false
  }
}

onMounted(() => {
  fetchCatastrophesNaturelles()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

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

function handleLocationSelected(location) {
  target.value = location
}
</script>

<template>
  <TutorialDriver ref="tutorial" v-if="tutorialOpen" @close="tutorialOpen = false" />

  <!-- Popovers Login/Register -->
  <LoginPopover
    :visible="showLoginPopover"
    @close="showLoginPopover = false"
    @switch-to-register="openRegister"
    @login-success="handleLoginSuccess"
  />

  <RegisterPopover
    :visible="showRegisterPopover"
    @close="showRegisterPopover = false"
    @switch-to-login="openLogin"
    @register-success="openLogin"
  />

  <AboutPopover :visible="showAboutPopover" @close="showAboutPopover = false">
    <h2 class="text-xl font-semibold mb-4">À propos</h2>
    <p class="text-sm text-gray-300 leading-relaxed">
      Ici tu mets ton contenu « About » : présentation du projet, crédits, etc.
    </p>
  </AboutPopover>

  <div class="flex flex-col h-screen w-full bg-black text-gray-100">
    <header
      class="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800 transition-all duration-300"
    >
      <nav class="max-w-full px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-4">
            <div class="transition-all duration-200 hover:opacity-90">
              <h1 class="text-lg font-semibold text-white">NASA Weather</h1>
              <p class="text-xs text-gray-500">Earth Observation System</p>
            </div>
          </div>

          <div class="hidden md:flex items-center space-x-8">
            <a href="#" class="text-gray-400 hover:text-white transition-all duration-200 text-sm font-medium px-3 py-1.5 rounded-md hover:bg-gray-800"
              >Home</a
            >
            <button
              @click="tutorial?.startTutorial()"
              class="text-gray-400 hover:text-white transition-all duration-200 text-sm font-medium px-3 py-1.5 rounded-md hover:bg-gray-800"
            >
              Tutorial
            </button>

            <div class="relative">
              <button
                data-favorites-button
                @click="toggleFavorites"
                class="text-gray-400 hover:text-white transition-all duration-200 flex items-center space-x-2 text-sm font-medium px-3 py-1.5 rounded-md hover:bg-gray-800"
              >
                <span>Favorites</span>
                <svg
                  class="w-4 h-4 transition-transform duration-200"
                  :class="{ 'rotate-180': favoritesOpen }"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  ></path>
                </svg>
              </button>

              <transition
                enter-active-class="transition ease-out duration-200"
                enter-from-class="opacity-0 translate-y-1"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-150"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="opacity-0 translate-y-1"
              >
                <div
                  data-favorites-dropdown
                  v-if="favoritesOpen"
                  class="absolute top-full mt-2 right-0 w-64 bg-gray-800 border border-gray-700 rounded-lg shadow-xl overflow-hidden z-50"
                >
                  <div class="p-2 max-h-64 overflow-y-auto">
                    <div
                      v-if="favorites.length === 0"
                      class="px-4 py-3 text-gray-500 text-sm text-center"
                    >
                      No favorites yet
                    </div>
                    <div
                      v-for="fav in favorites"
                      :key="fav.name"
                      @click="selectFavorite(fav)"
                      class="px-4 py-3 hover:bg-gray-700 cursor-pointer transition-all duration-150 rounded active:bg-gray-600"
                    >
                      <div class="text-white text-sm font-medium">{{ fav.name }}</div>
                      <div class="text-gray-500 text-xs mt-0.5">
                        {{ fav.lat.toFixed(2) }}° / {{ fav.lon.toFixed(2) }}°
                      </div>
                    </div>
                  </div>
                </div>
              </transition>
            </div>

            <button
              v-if="!isAuthenticated"
              @click="openLogin"
              class="text-gray-400 hover:text-white transition-all duration-200 text-sm font-medium px-3 py-1.5 rounded-md hover:bg-gray-800"
            >
              Login
            </button>
            <button
              v-else
              @click="logout"
              :disabled="logoutLoading"
              class="text-gray-400 hover:text-white transition-all duration-200 text-sm font-medium px-3 py-1.5 rounded-md hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <svg v-if="logoutLoading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ logoutLoading ? 'Logging out...' : 'Logout' }}
            </button>

            <button 
              @click="showAboutPopover = true" 
              class="text-gray-400 hover:text-white transition-all duration-200 text-sm font-medium px-3 py-1.5 rounded-md hover:bg-gray-800"
            >
              About
            </button>
          </div>

          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden text-gray-400 hover:text-white transition-all duration-200 p-2 rounded-md hover:bg-gray-800"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                v-if="mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
          </button>
        </div>

        <transition
          enter-active-class="transition ease-out duration-200"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition ease-in duration-150"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-800 py-3 space-y-1">
            <a
              href="#"
              class="block px-4 py-2.5 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded-md transition-all duration-200"
              >Home</a
            >
            <button
              @click="tutorial?.startTutorial(); mobileMenuOpen = false"
              class="block w-full text-left px-4 py-2.5 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded-md transition-all duration-200"
            >
              Tutorial
            </button>
            <button
              @click="toggleFavorites; mobileMenuOpen = false"
              class="block w-full text-left px-4 py-2.5 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded-md transition-all duration-200"
            >
              Favorites
            </button>
            <button
              v-if="!isAuthenticated"
              @click="openLogin(); mobileMenuOpen = false"
              class="block w-full text-left px-4 py-2.5 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded-md transition-all duration-200"
            >
              Login
            </button>
            <button
              v-else
              @click="logout(); mobileMenuOpen = false"
              class="block w-full text-left px-4 py-2.5 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded-md transition-all duration-200"
            >
              Logout
            </button>
            <button
              @click="showAboutPopover = true; mobileMenuOpen = false"
              class="block w-full text-left px-4 py-2.5 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded-md transition-all duration-200"
            >
              About
            </button>
          </div>
        </transition>
      </nav>
    </header>

    <div
      class="fixed top-16 left-0 right-0 z-40 bg-yellow-600 text-black overflow-hidden border-b-2 border-yellow-600 transition-all duration-300"
    >
      <div class="h-10 flex items-center">
        <div v-if="headlinesLoading" class="px-4 text-sm font-medium">
          Loading disaster alerts...
        </div>
        <div v-else class="ticker-wrapper">
          <div class="ticker-content">
            <span
              v-for="(headline, index) in disasterHeadlines"
              :key="index"
              class="ticker-item"
              @click="handleHeadlineClick(headline)"
            >
              <span class="font-bold">ALERT:</span> {{ headline }}
            </span>
            <span
              v-for="(headline, index) in disasterHeadlines"
              :key="`dup-${index}`"
              class="ticker-item"
              @click="handleHeadlineClick(headline)"
            >
              <span class="font-bold">ALERT:</span> {{ headline }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <main class="flex pt-16 overflow-hidden">
      <aside class="w-96 shrink-0 bg-gray-950 border-r border-gray-800 overflow-y-auto mt-10 transition-all duration-300">
        <div class="p-6 space-y-6">
          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3 transition-colors duration-200">
              Location Search
            </h2>
            <SearchBar @location-selected="handleLocationSelected" />
            <button
              v-if="isAuthenticated && target"
              @click="addFavorite(target)"
              class="mt-2 w-full px-3 py-2 bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-300 hover:text-white text-sm font-medium rounded-lg transition-all duration-300 flex items-center justify-center gap-2 active:scale-95"
              :class="{
                'bg-yellow-900/30 border-yellow-700/50 text-yellow-300': favoriteAdded || isCurrentLocationFavorite,
              }"
            >
              <svg
                class="w-4 h-4 transition-all duration-300"
                :class="{
                  'fill-yellow-400 stroke-yellow-400 scale-110': favoriteAdded || isCurrentLocationFavorite,
                }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                ></path>
              </svg>
              {{ favoriteAdded || isCurrentLocationFavorite ? 'Added to Favorites' : 'Add to Favorites' }}
            </button>
            <p class="text-xs text-gray-600 mt-2">
              Search for any city, region, or coordinates worldwide
            </p>
          </div>

          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3 transition-colors duration-200">
              Forecast Date
            </h2>
            <Calendar :selected-date="selectedDate" @date-selected="handleDateSelected" />
            <p class="text-xs text-gray-600 mt-2">
              Select a date to view historical or forecast data
            </p>
          </div>

          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3 transition-colors duration-200">
              Weather Summary
            </h2>
            <Tableaudebord
              :location="target"
              :selected-date="selectedDate"
              @reset-view="handleResetView"
            />
          </div>

          <div class="pt-6 border-t border-gray-800">
            <p class="text-xs text-gray-600 leading-relaxed">
              Data provided by NASA's Earth Observing System satellites and Open-Meteo API. Updates
              every 1-3 hours based on satellite orbital patterns.
            </p>
          </div>
        </div>
      </aside>
      <div class="w-full flex flex-col overflow-hidden mt-10">
        <!-- Bloc Forecast + Confidence -->
        <div class="border-b border-gray-800 bg-gray-950 py-5 px-5">
          <div class="flex flex-col md:flex-row gap-5 h-full">
            <div class="h-full">
              <HourlyForecast
                :selected-date="selectedDate"
                :latitude="target?.lat"
                :longitude="target?.lon"
                :location="`${target?.lat}, ${target?.lon}`"
                class="h-full"
              />
            </div>

            <!-- Confidence -->
            <div class="w-full md:w-64 lg:w-72 h-full">
              <div
                class="bg-gray-900/60 border border-gray-700 rounded-lg p-4 h-full flex flex-col justify-center"
              >
                <Confidence
                  v-if="confiance !== null && isFuturePrediction !== null"
                  :is-future-prediction="isFuturePrediction"
                  :confiance="confiance"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Globe -->
        <div class="flex justify-center items-center p-4">
          <div id="cesiumContainer" class="w-[400px] h-[400px]">
            <GlobeCesium :target="target" :reset-trigger="resetTrigger" />
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
  background-color: rgba(0, 0, 0, 0.15);
  transform: scale(1.02);
  transition: all 0.2s ease;
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
