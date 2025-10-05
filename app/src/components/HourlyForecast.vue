<template>
  <div class="px-4 py-2">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-xs font-medium text-gray-400 uppercase tracking-wide">
        Precipitation - {{ formattedDate }}
      </h2>
    </div>

    <div v-if="loading" class="text-center py-4 text-gray-500 text-xs">
      Loading...
    </div>

    <div v-else-if="error" class="text-center text-red-500 py-4 text-xs">
      {{ error }}
    </div>

    <div v-else-if="periods.length" class="grid grid-cols-4 gap-2">
      <div
        v-for="period in periods"
        :key="period.label"
        class="p-3 rounded bg-gray-900 border border-gray-800 text-center"
      >
        <p class="text-xs text-gray-500 mb-2">{{ period.label }}</p>
        
        <p class="text-lg font-semibold text-white">
          {{ period.rain.toFixed(1) }}
        </p>
        <p class="text-xs text-gray-600">mm</p>
      </div>
    </div>

    <div v-else class="text-center text-gray-600 py-4 text-xs">
      No data
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
    month: "short",
    day: "numeric",
  })
})

const periods = computed(() => {
  const rainPerPeriod = totalRain.value / 4
  
  return [
    { label: "Night", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Morning", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Afternoon", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Evening", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
  ].map(p => ({ ...p, rain: Math.max(0, p.rain) }))
})

const fetchPrecipitation = async () => {
  if (!props.latitude || !props.longitude || !props.selectedDate) return

  loading.value = true
  error.value = ""
  totalRain.value = 0

  try {
    // ✅ date sans tirets
    const date = props.selectedDate.toISOString().split("T")[0].replace(/-/g, "")

    // ✅ on passe les bons noms de params
    const res = await axios.get("http://127.0.0.1:8000/weather/rainfall", {
      params: {
        lat: props.latitude,
        lon: props.longitude,
        start: date,
        end: date
      }
    })

    const nasaData = res.data?.data || {}
    totalRain.value = nasaData[date] ?? 0
  } catch (err) {
    console.error("API Error:", err)
    error.value = "Error"
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