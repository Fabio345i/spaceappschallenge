<template>
  <div class="px-4 py-3">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-sm font-medium text-white">
        Precipitation Forecast - {{ formattedDate }}
      </h2>
    </div>

    <div v-if="loading" class="text-center py-8 text-gray-400">
      Loading precipitation data...
    </div>

    <div v-else-if="error" class="text-center text-red-500 py-8">
      {{ error }}
    </div>

    <div v-else-if="periods.length" class="grid grid-cols-4 gap-3">
      <div
        v-for="period in periods"
        :key="period.label"
        class="relative p-4 rounded-lg bg-gray-900 border border-gray-800 text-center"
      >
        <p class="text-xs font-medium text-blue-400 mb-3">{{ period.label }}</p>
        
        <div class="my-3">
          <svg class="w-8 h-8 mx-auto mb-2" :class="period.rain > 0 ? 'text-blue-400' : 'text-gray-600'" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 3.5a.5.5 0 01.5.5v1a.5.5 0 01-1 0V4a.5.5 0 01.5-.5zm-3 8a.5.5 0 01.5.5v3a.5.5 0 01-1 0v-3a.5.5 0 01.5-.5zm6 0a.5.5 0 01.5.5v3a.5.5 0 01-1 0v-3a.5.5 0 01.5-.5zm-3-1a.5.5 0 01.5.5v4a.5.5 0 01-1 0v-4a.5.5 0 01.5-.5z"/>
          </svg>
          <p class="text-2xl font-bold" :class="period.rain > 0 ? 'text-blue-400' : 'text-gray-500'">
            {{ period.rain.toFixed(1) }}
          </p>
          <p class="text-xs text-gray-500 mt-1">mm</p>
        </div>

        <p class="text-xs" :class="period.rain > 0 ? 'text-blue-300' : 'text-gray-600'">
          {{ period.rain > 2 ? 'Heavy' : period.rain > 0.5 ? 'Moderate' : 'No rain' }}
        </p>
      </div>
    </div>

    <div v-else class="text-center text-gray-500 py-8">
      No precipitation data available
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from "vue"
import axios from "axios"

const props = defineProps({
  selectedDate: Date,
  latitude: Number,
  longitude: Number,
  location: String,
})

const totalRain = ref(0)
const loading = ref(false)
const error = ref("")

const formattedDate = computed(() => {
  return props.selectedDate?.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  })
})

const periods = computed(() => {
  const rainPerPeriod = totalRain.value / 4
  
  return [
    { label: "Night", time: "00:00 - 06:00", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Morning", time: "06:00 - 12:00", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Afternoon", time: "12:00 - 18:00", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Evening", time: "18:00 - 00:00", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
  ].map(p => ({ ...p, rain: Math.max(0, p.rain) }))
})

const fetchPrecipitation = async () => {
  if (!props.latitude || !props.longitude || !props.selectedDate) return

  loading.value = true
  error.value = ""
  totalRain.value = 0

  try {
    const date = props.selectedDate.toISOString().split("T")[0]
    const res = await axios.get(
      `http://127.0.0.1:8000/weather/rainfall?start_date=${date}&end_date=${date}&latitude=${props.latitude}&longitude=${props.longitude}`
    )

    const nasaData = res.data?.data || []
    totalRain.value = nasaData.length ? nasaData[0].data : 0
  } catch (err) {
    console.error("API Error:", err)
    error.value = "Unable to load precipitation data"
  } finally {
    loading.value = false
  }
}

watch(
  () => [props.selectedDate, props.latitude, props.longitude],
  fetchPrecipitation,
  { immediate: true }
)
</script>

<style scoped>
</style>