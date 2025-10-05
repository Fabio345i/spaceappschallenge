<template>
  <div class="bg-gray-900 border border-gray-800 rounded-md p-3">
    <h2 class="text-sm font-medium text-white mb-3">Current Conditions</h2>

    <div v-if="dataLoaded">
      <div class="mb-3 pb-3 border-b border-gray-800">
        <p class="text-xs text-gray-500 mb-0.5">Location</p>
        <p class="text-sm text-white truncate">{{ displayName }}</p>
        <p class="text-xs text-gray-600">{{ props.location?.lat.toFixed(2) }}° / {{ props.location?.lon.toFixed(2) }}°</p>
      </div>

      <div class="grid grid-cols-2 gap-2 mb-3">
        <div v-for="(item, i) in weatherData" :key="i" class="bg-gray-800/50 rounded p-2">
          <p class="text-xs text-gray-500 mb-1">{{ item.name }}</p>
          <p class="text-lg font-semibold text-white">{{ item.value }}</p>
        </div>
      </div>

      <button @click="resetView" class="w-full py-1.5 px-3 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded text-gray-400 hover:text-white text-xs">
        Reset View
      </button>
    </div>

    <div v-else class="text-center py-6 text-gray-600">
      <svg class="w-10 h-10 mx-auto mb-2 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <p class="text-xs">Select a location</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"

const props = defineProps({
  location: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['reset-view'])

const temperature = ref("--")
const precipitation = ref("--")
const windSpeed = ref("--")
const airQuality = ref("--")
const dataLoaded = ref(false)

const displayName = computed(() => {
  if (props.location?.geojson?.properties?.display_name) {
    return props.location.geojson.properties.display_name
  }
  return 'Selected Location'
})

const weatherData = computed(() => [
  { name: "Temp", value: `${temperature.value}°C` },
  { name: "Precip", value: `${precipitation.value}mm` },
  { name: "Wind", value: `${windSpeed.value}m/s` },
  { name: "AQI", value: airQuality.value },
])

watch(
  () => props.location,
  (newLocation) => {
    if (newLocation && newLocation.lat && newLocation.lon) {
      fetchWeather()
    } else {
      dataLoaded.value = false
    }
  },
  { deep: true }
)

function fetchWeather() {
  if (!props.location) return

  temperature.value = (Math.random() * 30).toFixed(1)
  precipitation.value = (Math.random() * 10).toFixed(1)
  windSpeed.value = (Math.random() * 15).toFixed(1)
  airQuality.value = ["Good", "Moderate", "Poor"][Math.floor(Math.random() * 3)]

  dataLoaded.value = true
}

function resetView() {
  emit('reset-view')
}
</script>