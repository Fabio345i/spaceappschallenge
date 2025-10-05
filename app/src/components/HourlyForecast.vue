<template>
  <div class="h-full flex flex-col">
    <div class="grid grid-cols-4 gap-3 flex-1">
      <template v-if="loading">
        <div
          v-for="n in 4"
          :key="`loading-${n}`"
          class="rounded p-5 bg-gray-800/50 border border-gray-800 text-center animate-pulse flex flex-col justify-around"
        >
          <div class="h-3 w-10 bg-gray-700/60 rounded mx-auto mb-2"></div>
          <div class="h-5 w-12 bg-gray-600/60 rounded mx-auto mb-2"></div>
          <div class="h-3 w-8 bg-gray-700/60 rounded mx-auto"></div>
        </div>
      </template>

      <template v-else-if="error">
        <div class="col-span-4 flex items-center justify-center text-red-500 text-sm">
          {{ error }}
        </div>
      </template>

      <template v-else>
        <div
          v-for="period in periods"
          :key="period.label"
          class="rounded p-5 bg-gray-900 border border-gray-800 text-center flex flex-col justify-around"
        >
          <p class="text-sm text-gray-500 mb-1">{{ period.label }}</p>
          <p class="text-lg font-semibold text-white leading-tight">{{ period.rain.toFixed(1) }}</p>
          <p class="text-xs text-gray-600">mm</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from "vue"
import axios from "axios"

const props = defineProps({
  selectedDate: Date,
  latitude: Number,
  longitude: Number
})

const loading = ref(true)
const error = ref("")
const totalRain = ref(0)
const customPeriods = ref([])

const periods = computed(() => {
  if (customPeriods.value.length) return customPeriods.value
  const rainPerPeriod = totalRain.value / 4
  return ["Night", "Morning", "Afternoon", "Evening"].map(label => ({
    label,
    rain: Math.max(0, rainPerPeriod + (Math.random() * 0.5 - 0.25))
  }))
})

const isFuture = date => {
  const today = new Date()
  const d = new Date(date)
  return d.setHours(0, 0, 0, 0) > today.setHours(0, 0, 0, 0)
}

async function fetchPrecipitation() {
  if (!props.latitude || !props.longitude || !props.selectedDate) {
    loading.value = false
    totalRain.value = 0
    customPeriods.value = []
    return
  }

  loading.value = true
  error.value = ""
  totalRain.value = 0
  customPeriods.value = []

  try {
    const d = props.selectedDate
    const y = d.getUTCFullYear()
    const m = d.getUTCMonth() + 1
    const day = d.getUTCDate()
    const dateStr = d.toISOString().split("T")[0].replace(/-/g, "")

    if (isFuture(d)) {
      const { data } = await axios.get("http://127.0.0.1:8000/algo/daily/predict_rain_hourly", {
        params: {
          lat: props.latitude,
          lon: props.longitude,
          day,
          month: m,
          base_years: 20,
          future_year: y,
          window_days: 3
        }
      })
      totalRain.value = data.precip_moyenne ?? 0
      customPeriods.value = data.periods || []
    } else {
      const { data } = await axios.get("http://127.0.0.1:8000/weather/rainfall", {
        params: { lat: props.latitude, lon: props.longitude, start: dateStr, end: dateStr }
      })
      totalRain.value = data?.data?.[dateStr] ?? 0
    }
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
