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

    <div class="flex gap-2 mt-4">

        <button
            class="flex-1 px-5 py-2 rounded-lg font-semibold text-white 
                   bg-blue-600 border border-blue-700 
                   hover:bg-blue-700 hover:border-blue-800 
                   transition-colors duration-200 
                   shadow-md"
            @click="generatePDF()"
        >
            <svg class="" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
            Download Report
        </button>

        <button 
            @click="resetView" 
            class="py-2 px-3 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-400 hover:text-white text-sm font-medium transition-colors duration-200"
        >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m3.987 8l-.626 1.458M15 11l-3 3-3-3m-6 3l1.874 4.373A8.001 8.001 0 0020.428 15"></path></svg>
        </button>
    </div>
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

import { jsPDF } from "jspdf"

const generatePDF = () => {
  const doc = new jsPDF()

  
  doc.setFont("helvetica", "bold")
  doc.setFontSize(20)
  doc.text(" Rapport meteo", 105, 20, { align: "center" })

  
  doc.setLineWidth(0.5)
  doc.line(20, 25, 190, 25)

  
  doc.setFontSize(12)
  doc.setFont("helvetica", "normal")
  doc.text("Date du rapport : " + new Date().toLocaleDateString(), 20, 35)

  
  const data = [
    ["Température", "25°C"],
    ["Précipitations", "0 mm"],
    ["Vitesse du vent", "10 m/s"],
    ["Qualité de l’air", "Bonne"],
    ["Humidité", "65%"],
  ]

  let y = 50
  doc.setFont("helvetica", "bold")
  doc.text("Résumé des conditions :", 20, y)
  y += 8

  doc.setFont("helvetica", "normal")

  data.forEach(([label, value]) => {
    doc.text(`• ${label} :`, 25, y)
    doc.text(value, 90, y)
    y += 8
  })


  doc.setFontSize(10)
  doc.setTextColor(100)

  doc.save("rapport_meteo.pdf")
}


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