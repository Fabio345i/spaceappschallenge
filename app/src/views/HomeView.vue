<script setup>
import { ref } from 'vue'
import SearchBar from '@/components/SearchBar.vue'
import GlobeCesium from '@/components/GlobeCesium.vue'
import Tableaudebord from '@/components/Tableaudebord.vue'
import Calendar from '@/components/Calendar.vue'
import HourlyForecast from '@/components/HourlyForecast.vue'
import TutorialDriver from '@/components/tutorial/TutorialDriver.vue'
const tutorial = ref(null)

const target = ref(null)
const mobileMenuOpen = ref(false)
const favoritesOpen = ref(false)
const resetTrigger = ref(0)

const favorites = ref([
  { name: 'New York, USA', lat: 40.7128, lon: -74.006 },
  { name: 'Paris, France', lat: 48.8566, lon: 2.3522 },
  { name: 'Tokyo, Japan', lat: 35.6762, lon: 139.6503 },
])

function selectFavorite(fav) {
  target.value = { lat: fav.lat, lon: fav.lon }
  favoritesOpen.value = false
}

const selectedDate = ref(new Date())

function handleDateSelected(date) {
  selectedDate.value = date
}

function handleResetView() {
  resetTrigger.value++
}
</script>

<template>
  <TutorialDriver ref="tutorial" />
  <div class="flex flex-col h-screen w-full bg-black text-gray-100">
    <header
      class="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800"
    >
      <nav class="max-w-full px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-4">
            <div>
              <h1 class="text-lg font-semibold text-white">NASA Weather</h1>
              <p class="text-xs text-gray-500">Earth Observation System</p>
            </div>
          </div>

          <div class="hidden md:flex items-center space-x-8">
            <a
              href="#"
              class="text-gray-400 hover:text-white transition-colors text-sm font-medium"
            >
              Home
            </a>

            <button
              @click="tutorial?.startTutorial()"
              class="text-gray-400 hover:text-white transition-colors text-sm font-medium"
            >
              Tutorial
            </button>

            <div class="relative">
              <button
                @click="favoritesOpen = !favoritesOpen"
                class="text-gray-400 hover:text-white transition-colors flex items-center space-x-2 text-sm font-medium"
              >
                <span>Favorites</span>
                <svg
                  class="w-4 h-4 transition-transform"
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

              <div
                v-if="favoritesOpen"
                class="absolute top-full mt-3 right-0 w-64 bg-gray-800 border border-gray-700 rounded-lg shadow-xl overflow-hidden"
              >
                <div class="p-2">
                  <div
                    v-for="fav in favorites"
                    :key="fav.name"
                    @click="selectFavorite(fav)"
                    class="px-4 py-3 hover:bg-gray-700 cursor-pointer transition-colors rounded"
                  >
                    <div class="text-white text-sm font-medium">{{ fav.name }}</div>
                    <div class="text-gray-500 text-xs mt-0.5">
                      {{ fav.lat.toFixed(2) }}° / {{ fav.lon.toFixed(2) }}°
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <a
              href="#"
              class="text-gray-400 hover:text-white transition-colors text-sm font-medium"
            >
              Data
            </a>
            <a
              href="#"
              class="text-gray-400 hover:text-white transition-colors text-sm font-medium"
            >
              About
            </a>
          </div>

          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden text-gray-400 hover:text-white"
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

        <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-800 py-3">
          <a
            href="#"
            class="block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded"
            >Home</a
          >
          <a
            href="#"
            class="block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded"
            >Favorites</a
          >
          <a
            href="#"
            class="block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded"
            >Data</a
          >
          <a
            href="#"
            class="block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 text-sm rounded"
            >About</a
          >
        </div>
      </nav>
    </header>

    <main class="flex-1 flex pt-16 overflow-hidden">
      <aside class="w-96 flex-shrink-0 bg-gray-950 border-r border-gray-800 overflow-y-auto">
        <div class="p-6 space-y-6">
          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Location Search
            </h2>
            <SearchBar @location-selected="target = $event" />
            <p class="text-xs text-gray-600 mt-2">
              Search for any city, region, or coordinates worldwide
            </p>
          </div>

          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Forecast Date
            </h2>
            <Calendar :selected-date="selectedDate" @date-selected="handleDateSelected" />
            <p class="text-xs text-gray-600 mt-2">
              Select a date to view historical or forecast data
            </p>
          </div>

          <div>
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
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

      <div class="flex-1 flex flex-col gap-10 overflow-hidden">
        <div class="border-b border-gray-800 bg-gray-950">
          <div class="px-6 py-4">
            <h2 class="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Hourly Forecast
            </h2>
            <HourlyForecast
              v-if="target"
              :selected-date="selectedDate"
              :latitude="target.lat"
              :longitude="target.lon"
              :location="`${target.lat}, ${target.lon}`"
            />
          </div>
        </div>

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

</style>
