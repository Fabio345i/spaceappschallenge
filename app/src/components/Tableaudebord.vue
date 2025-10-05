<template>
  <div class="w-full bg-gray-900/90 backdrop-blur-sm border border-gray-800 rounded-lg p-6 shadow-2xl">
    <header class="text-center mb-6">
      <h1 class="text-2xl font-semibold text-white mb-2">
        Weather Data
      </h1>
      <p class="text-gray-400 text-sm">
        Atmospheric Analysis • NASA Satellites
      </p>
    </header>

    <transition name="fade">
      <div v-if="dataLoaded" class="space-y-4">
        <div class="text-center mb-6 pb-4 border-b border-gray-800">
          <h2 class="text-base font-medium text-white mb-1">
            {{ displayName }}
          </h2>
          <p class="text-gray-500 text-xs">
            {{ props.location?.lat.toFixed(4) }}° / {{ props.location?.lon.toFixed(4) }}°
          </p>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div
            v-for="(item, i) in weatherData"
            :key="i"
            class="bg-gray-800/60 border border-gray-700 rounded-lg p-4 hover:bg-gray-800 hover:border-gray-600 transition-all"
          >
            <div class="text-center">
              <div class="text-xs text-gray-500 uppercase tracking-wider mb-2">
                {{ item.name }}
              </div>
              <p class="text-2xl font-semibold text-white mb-1">
                {{ item.value }}
              </p>
              <p class="text-gray-500 text-xs">{{ item.unit }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12 text-gray-500">
        <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-800 flex items-center justify-center">
          <svg class="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <p class="text-sm">Select a location to display weather data</p>
      </div>
    </transition>
 <button
  class="px-5 py-2 rounded-lg font-semibold text-gray-100 
         bg-gray-800 border border-gray-700 
         hover:bg-gray-700 hover:text-white 
         transition-colors duration-200 
         backdrop-blur-sm shadow-sm"
  @click="generatePDF()"
>
  Enregistrer le rapport météo
</button>


    <footer class="mt-6 text-gray-600 text-xs text-center border-t border-gray-800 pt-4">
      Data provided by <span class="text-gray-500">NASA GES DISC</span> and <span class="text-gray-500">Open-Meteo</span>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
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
});

const temperature = ref("--");
const precipitation = ref("--");
const windSpeed = ref("--");
const airQuality = ref("--");
const dataLoaded = ref(false);

const displayName = computed(() => {
  if (props.location?.geojson?.properties?.display_name) {
    return props.location.geojson.properties.display_name;
  }
  return 'Selected Location';
});

const weatherData = computed(() => [
  { name: "Temperature", value: `${temperature.value}°C`, unit: "Celsius" },
  { name: "Precipitation", value: `${precipitation.value} mm`, unit: "Millimeters" },
  { name: "Wind Speed", value: `${windSpeed.value} m/s`, unit: "Meters/sec" },
  { name: "Air Quality", value: airQuality.value, unit: "Index" },
]);

watch(
  () => props.location,
  (newLocation) => {
    if (newLocation && newLocation.lat && newLocation.lon) {
      console.log("Location received. Starting fetchWeather:", newLocation);
      fetchWeather();
    } else {
      dataLoaded.value = false;
    }
  },
  { deep: true }
);

function fetchWeather() {
  if (!props.location) return;

  temperature.value = (Math.random() * 30).toFixed(1);
  precipitation.value = (Math.random() * 10).toFixed(1);
  windSpeed.value = (Math.random() * 15).toFixed(1);
  airQuality.value = ["Good", "Moderate", "Poor"][Math.floor(Math.random() * 3)];

  dataLoaded.value = true;
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>