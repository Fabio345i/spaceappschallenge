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

const loading = ref(false)
const error = ref("")
const totalRain = ref(0)
const customPeriods = ref([])

const formattedDate = computed(() =>
  props.selectedDate?.toLocaleDateString("en-US", { month: "short", day: "numeric" })
)

// ✅ periods : soit les valeurs prédictives (future), soit génération simple si date passée
const periods = computed(() => {
  if (customPeriods.value.length) return customPeriods.value

  // Si pas de prédiction spécifique, on répartit la pluie totale
  const rainPerPeriod = totalRain.value / 4
  return [
    { label: "Night", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Morning", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Afternoon", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
    { label: "Evening", rain: rainPerPeriod + (Math.random() * 0.5 - 0.25) },
  ].map(p => ({ ...p, rain: Math.max(0, p.rain) }))
})

const isFuture = (date) => {
  const today = new Date()
  const d = new Date(date)
  return d.setHours(0,0,0,0) > today.setHours(0,0,0,0)
}

const fetchPrecipitation = async () => {
  if (!props.latitude || !props.longitude || !props.selectedDate) return

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
      // 🔮 FUTUR : appel à l'API de prédiction
      const res = await axios.get("http://127.0.0.1:8000/algo/daily/predict_rain_hourly", {
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
      totalRain.value = res.data.precip_moyenne ?? 0
      customPeriods.value = res.data.periods || []
    } else {
      // 🌧️ PASSÉ / PRÉSENT : données réelles NASA POWER
      const res = await axios.get("http://127.0.0.1:8000/weather/rainfall", {
        params: { lat: props.latitude, lon: props.longitude, start: dateStr, end: dateStr }
      })
      const nasaData = res.data?.data || {}
      totalRain.value = nasaData[dateStr] ?? 0
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

<style scoped>
</style>