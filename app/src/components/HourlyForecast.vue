<template>
  <div class="px-4 py-3">
    <div class="flex items-center justify-between mb-2">
      <h2 class="text-sm font-medium text-white">
        Hourly Forecast - {{ formattedDate }}
      </h2>
    </div>

    <div v-if="loading" class="text-center py-4 text-gray-400">Chargement des données...</div>
    <div v-else-if="error" class="text-center text-red-500 py-4">{{ error }}</div>

    <div v-else-if="hourlyData.length" class="flex overflow-x-auto space-x-2 pb-2">
      <div
        v-for="hour in hourlyData"
        :key="hour.time"
        class="flex-shrink-0 w-20 p-2 rounded bg-gray-900 border border-gray-800 text-center hover:border-gray-700"
      >
        <p class="text-xs text-gray-500 mb-1">{{ hour.time }}</p>
        <p class="text-base font-semibold text-white">{{ hour.temp }}°</p>
        <p class="text-xs text-gray-500 mt-1">{{ hour.condition }}</p>
        <p v-if="hour.rain > 0" class="text-xs text-blue-400 mt-1">{{ hour.rain.toFixed(2) }} mm</p>
      </div>
    </div>

    <div v-else class="text-center text-gray-500 py-4">
      Aucune donnée disponible pour cette journée.
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

const hourlyData = ref([])
const loading = ref(false)
const error = ref("")

const formattedDate = computed(() => {
  return props.selectedDate?.toLocaleDateString("fr-FR", {
    weekday: "short",
    month: "short",
    day: "numeric",
  })
})

const fetchHourlyForecast = async () => {
  if (!props.latitude || !props.longitude || !props.selectedDate) return

  loading.value = true
  error.value = ""
  hourlyData.value = []

  try {
    const date = props.selectedDate.toISOString().split("T")[0]
    const res = await axios.get(
      `http://127.0.0.1:8000/weather/rainfall?start_date=${date}&end_date=${date}&latitude=${props.latitude}&longitude=${props.longitude}`
    )

    const nasaData = res.data?.data || []
    const totalRain = nasaData.length ? nasaData[0].data : 0

    const conditions = ["Clear", "Cloudy", "Rain", "Overcast"]

    hourlyData.value = Array.from({ length: 24 }, (_, i) => {
      const hour = `${String(i).padStart(2, "0")}:00`
      const condition = totalRain > 1 && i % 5 === 0 ? "Rain" : conditions[Math.floor(Math.random() * conditions.length)]

      const baseTemp = 18 + 6 * Math.sin((i / 24) * Math.PI * 2)
      const temp = Math.round(baseTemp + (Math.random() * 2 - 1))

      const rain = condition === "Rain" ? totalRain / 24 + Math.random() * 0.3 : 0

      return { time: hour, temp, condition, rain }
    })
  } catch (err) {
    console.error("Erreur API :", err)
    error.value = "Impossible de charger les données météo."
  } finally {
    loading.value = false
  }
}

watch(
  () => [props.selectedDate, props.latitude, props.longitude],
  fetchHourlyForecast,
  { immediate: true }
)
</script>

<style scoped>
.overflow-x-auto::-webkit-scrollbar {
  height: 4px;
}
.overflow-x-auto::-webkit-scrollbar-track {
  background: #1f2937;
}
.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 2px;
}
</style>
