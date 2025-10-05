<template>
  <div class="bg-gray-900 border border-gray-800 rounded-lg p-4">
    <h2 class="text-sm font-semibold text-white mb-4 uppercase tracking-wide">
      Current Conditions
    </h2>

    <div v-if="dataLoaded">
      <!-- Localisation -->
      <div class="mb-4 pb-3 border-b border-gray-800">
        <p class="text-xs text-gray-400 mb-0.5">Location</p>
        <p class="text-sm font-medium text-white truncate">{{ displayName }}</p>
        <p class="text-xs text-gray-500">
          {{ props.location?.lat.toFixed(2) }}° /
          {{ props.location?.lon.toFixed(2) }}°
        </p>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-2 gap-3">
        <div v-for="(item, i) in weatherData" :key="i"
          class="bg-gray-800/40 rounded-lg p-3 hover:bg-gray-800/60 transition">
          <p class="text-xs text-gray-400 mb-1">{{ item.name }}</p>
          <p class="text-lg font-semibold text-white">{{ item.value }}</p>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-2 mt-6">
        <button
          @click="generatePDF()"
          class="flex items-center gap-2 py-2 px-3 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-300 hover:text-white text-sm font-medium transition-colors duration-200"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Download Report
        </button>

        <button @click="resetView"
          class="py-2 px-3 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-300 hover:text-white text-sm font-medium transition-colors duration-200">
          Reset View
        </button>
      </div>
    </div>

    <div v-else class="text-center py-6 text-gray-600">
      <svg class="w-10 h-10 mx-auto mb-2 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z">
        </path>
      </svg>
      <p class="text-xs">Select a location and date</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { jsPDF } from "jspdf"
import axios from "axios"

const props = defineProps({
  location: { type: Object, default: null },
  selectedDate: { type: Date, default: () => new Date() }
})
const emit = defineEmits(["reset-view"])

// --- Données météo ---
const temperature = ref("--")
const tMin = ref("--")
const tMax = ref("--")
const humidity = ref("--")
const wind = ref("--")
const pressure = ref("--")
const rain = ref("--")
const dataLoaded = ref(false)

const displayName = computed(() =>
  props.location?.geojson?.properties?.display_name || "Selected Location"
)

const weatherData = computed(() => [
  { name: "Temp moyenne", value: `${temperature.value}°C` },
  { name: "Min / Max", value: `${tMin.value}°C / ${tMax.value}°C` },
  { name: "Humidité", value: `${humidity.value}%` },
  { name: "Vent", value: `${wind.value} m/s` },
  { name: "Pression", value: `${pressure.value} kPa` },
  { name: "Pluie", value: `${rain.value} mm` },
])

watch(
  () => [props.location, props.selectedDate],
  ([loc, date]) => {
    if (loc?.lat && loc?.lon) fetchWeather(loc, date)
    else dataLoaded.value = false
  },
  { deep: true }
)

async function fetchWeather(loc, date) {
  try {
    const d = new Date(date)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, "0")
    const day = String(d.getDate()).padStart(2, "0")

    // --- 1. Analyse historique ---
    const analyseRes = await axios.get("http://127.0.0.1:8000/daily/analyse", {
      params: { lat: loc.lat, lon: loc.lon, day, month: m, years: 20 }
    })
    const analyse = analyseRes.data

    if (analyse && analyse.T_moyenne != null) {
      temperature.value = analyse.T_moyenne.toFixed(1)
      tMin.value = analyse.Tmin_moyenne?.toFixed(1) ?? "--"
      tMax.value = analyse.Tmax_moyenne?.toFixed(1) ?? "--"
      humidity.value = analyse.humidite_moyenne?.toFixed(0) ?? "--"
      wind.value = analyse.vent_moyen_m_s?.toFixed(1) ?? "--"
      pressure.value = analyse.pression_moy_kPa?.toFixed(1) ?? "--"
    } else {
      console.warn("Réponse inattendue de /daily/analyse :", analyse)
      temperature.value = tMin.value = tMax.value = humidity.value = wind.value = pressure.value = "--"
    }

    // --- 2. Données POWER exactes pour la date ---
    const dateStr = `${y}${m}${day}`
    const powerRes = await axios.get("http://127.0.0.1:8000/power/daily", {
      params: { lat: loc.lat, lon: loc.lon, start: dateStr, end: dateStr }
    })
    const params = powerRes.data?.parameters
    rain.value = params?.PRECTOTCORR?.[dateStr]?.toFixed(1) ?? "--"

    dataLoaded.value = true
  } catch (e) {
    console.error("Erreur API :", e)
    dataLoaded.value = false
  }
}

function generatePDF() {
  const doc = new jsPDF()
  const d = new Date(props.selectedDate)

  // --- Header ---
  doc.setFont("helvetica", "bold")
  doc.setFontSize(18)
  doc.text("Rapport Météo", 105, 20, { align: "center" })
  doc.setLineWidth(0.5)
  doc.line(20, 25, 190, 25)

  // --- Infos générales ---
  doc.setFontSize(12)
  doc.setFont("helvetica", "normal")
  doc.text(`Date du rapport : ${d.toLocaleDateString()}`, 20, 35)
  doc.text(
    `Position : ${displayName.value} (${props.location?.lat.toFixed(2)}°, ${props.location?.lon.toFixed(2)}°)`,
    20,
    43
  )

  // --- Données météo ---
  let y = 55
  doc.setFontSize(14)
  doc.setFont("helvetica", "bold")
  doc.text("Conditions météo :", 20, y)
  y += 10
  doc.setFontSize(12)
  doc.setFont("helvetica", "normal")

  const data = [
    ["Température moyenne", `${temperature.value} °C`],
    ["Température min / max", `${tMin.value} °C / ${tMax.value} °C`],
    ["Humidité moyenne", `${humidity.value} %`],
    ["Vent moyen", `${wind.value} m/s`],
    ["Pression", `${pressure.value} kPa`],
    ["Précipitations", `${rain.value} mm`],
  ]

  data.forEach(([label, value]) => {
    doc.text(`• ${label} :`, 25, y)
    doc.text(value, 100, y)
    y += 8
  })

  doc.setFontSize(10)
  doc.setTextColor(100)
  doc.text("Source : NASA POWER & données historiques internes", 20, y + 10)

  doc.save("rapport_meteo.pdf")
}

function resetView() {
  emit("reset-view")
}
</script>
