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
          {{ props.location?.lat.toFixed(2) }}° / {{ props.location?.lon.toFixed(2) }}°
        </p>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-2 gap-3">
        <div
          v-for="(item, i) in weatherData"
          :key="i"
          class="bg-gray-800/40 rounded-lg p-3 hover:bg-gray-800/60 transition"
        >
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
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          Download Report
        </button>

        <button
          @click="resetView"
          class="py-2 px-3 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-300 hover:text-white text-sm font-medium transition-colors duration-200"
        >
          Reset View
        </button>
      </div>
    </div>

    <div v-else class="text-center py-6 text-gray-600">
      <svg
        class="w-10 h-10 mx-auto mb-2 text-gray-700"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        ></path>
      </svg>
      <p class="text-xs">Select a location and date</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { jsPDF } from 'jspdf'
import axios from 'axios'

const props = defineProps({
  location: { type: Object, default: null },
  selectedDate: { type: Date, default: () => new Date() },
})
const emit = defineEmits(['reset-view'])

const temperature = ref('--')
const tMin = ref('--')
const tMax = ref('--')
const humidity = ref('--')
const wind = ref('--')
const pressure = ref('--')
const rain = ref('--')
const dataLoaded = ref(false)

const displayName = computed(
  () => props.location?.geojson?.properties?.display_name || 'Selected Location',
)

const weatherData = computed(() => [
  { name: 'Temp moyenne', value: `${temperature.value}°C` },
  { name: 'Min / Max', value: `${tMin.value}°C / ${tMax.value}°C` },
  { name: 'Humidité', value: `${humidity.value}%` },
  { name: 'Vent', value: `${wind.value} m/s` },
  { name: 'Pression', value: `${pressure.value} kPa` },
  { name: 'Pluie', value: `${rain.value} mm` },
])

watch(
  () => [props.location, props.selectedDate],
  ([loc, date]) => {
    if (loc?.lat && loc?.lon) fetchWeather(loc, date)
    else dataLoaded.value = false
  },
  { deep: true },
)

function isSameDayUTC(a, b) {
  const da = new Date(Date.UTC(a.getUTCFullYear(), a.getUTCMonth(), a.getUTCDate()))
  const db = new Date(Date.UTC(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate()))
  return da.getTime() === db.getTime()
}

function isPastOrTodayUTC(d) {
  const today = new Date()
  const dUTC = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()))
  const tUTC = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()))
  return dUTC.getTime() <= tUTC.getTime()
}

async function fetchWeather(loc, date) {
  const d = new Date(date)
  const y = d.getUTCFullYear()
  const m = String(d.getUTCMonth() + 1).padStart(2, "0")
  const day = String(d.getUTCDate()).padStart(2, "0")
  const dateStr = `${y}${m}${day}`

  dataLoaded.value = false

  try {
    if (isPastOrTodayUTC(d)) {
      // ---- Historique ----
      const { data: a } = await axios.get("http://127.0.0.1:8000/algo/daily/analyse", {
        params: { lat: loc.lat, lon: loc.lon, day, month: m, years: 20 }
      })

      temperature.value = a.T_moyenne != null ? a.T_moyenne.toFixed(1) : "--"
      tMin.value        = a.Tmin_moyenne != null ? a.Tmin_moyenne.toFixed(1) : "--"
      tMax.value        = a.Tmax_moyenne != null ? a.Tmax_moyenne.toFixed(1) : "--"
      humidity.value    = a.humidite_moyenne != null ? a.humidite_moyenne.toFixed(0) : "--"
      wind.value        = a.vent_moyen_m_s != null ? a.vent_moyen_m_s.toFixed(1) : "--"
      pressure.value    = a.pression_moy_kPa != null ? a.pression_moy_kPa.toFixed(1) : "--"

      // ✅ Affiche le panneau même si la pluie échoue
      dataLoaded.value = true

      // Pluie historique (peut échouer sans casser l’UI)
      try {
        const { data: r } = await axios.get("http://127.0.0.1:8000/weather/rainfall", {
          params: { lat: loc.lat, lon: loc.lon, start: dateStr, end: dateStr }
        })
        const obj = r?.data || {}
        rain.value = obj[dateStr] != null ? Number(obj[dateStr]).toFixed(1) : "--"
      } catch (e) {
        console.warn("Rainfall (historique) KO:", e)
        rain.value = "--"
      }

    } else {
      // ---- Futur (prédiction) ----
      const { data: p } = await axios.get("http://127.0.0.1:8000/algo/daily/predict", {
        params: {
          lat: loc.lat,
          lon: loc.lon,
          day,
          month: m,
          base_years: 20,
          future_year: y,       // ok si ton backend accepte l'année absolue (tu as un 200)
          window_days: 3
        }
      })

      const safe = v => (v != null && !Number.isNaN(Number(v))) ? Number(v) : null
      temperature.value = safe(p.T_moyenne)?.toFixed(1) ?? "--"
      tMin.value        = safe(p.Tmin_ajustee ?? p.Tmin_base)?.toFixed(1) ?? "--"
      tMax.value        = safe(p.Tmax_ajustee ?? p.Tmax_base)?.toFixed(1) ?? "--"
      humidity.value    = safe(p.humidite_moyenne)?.toFixed(0) ?? "--"
      wind.value        = safe(p.vent_moyen_m_s)?.toFixed(1) ?? "--"
      pressure.value    = safe(p.pression_moy_kPa)?.toFixed(1) ?? "--"

      // ✅ Affiche le panneau même si la pluie future n’existe pas
      dataLoaded.value = true

      // Pluie future: NASA POWER n’en fournit pas → on tente, mais on n’échoue pas l’UI
      try {
        const { data: r } = await axios.get("http://127.0.0.1:8000/weather/rainfall", {
          params: { lat: loc.lat, lon: loc.lon, start: dateStr, end: dateStr }
        })
        const obj = r?.data || {}
        rain.value = obj[dateStr] != null ? Number(obj[dateStr]).toFixed(1) : "--"
      } catch (e) {
        console.warn("Rainfall (futur) indisponible:", e)
        rain.value = "--"
      }
    }
  } catch (e) {
    console.error("Erreur API principale :", e)
    temperature.value = tMin.value = tMax.value = humidity.value = wind.value = pressure.value = rain.value = "--"
    dataLoaded.value = false
  }
}

function generatePDF() {
  const doc = new jsPDF()
  const d = new Date(props.selectedDate)

  // Couleurs professionnelles épurées
  const primary = [30, 58, 138] // Bleu foncé professionnel
  const accent = [59, 130, 246] // Bleu moyen
  const textDark = [17, 24, 39] // Gris très foncé
  const textGray = [107, 114, 128] // Gris moyen
  const borderGray = [229, 231, 235] // Bordure légère

  // === HEADER MINIMALISTE ===
  doc.setDrawColor(...borderGray)
  doc.setLineWidth(0.3)
  doc.line(20, 30, 190, 30)

  doc.setTextColor(...primary)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(24)
  doc.text('Weather Report', 20, 20)

  doc.setTextColor(...textGray)
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  doc.text(
    `Generated on ${new Date().toLocaleDateString('en-US')} at ${new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`,
    20,
    27,
  )

  // === INFORMATIONS GÉNÉRALES ===
  let y = 45

  doc.setTextColor(...textDark)
  doc.setFontSize(12)
  doc.setFont('helvetica', 'bold')
  doc.text('General Information', 20, y)

  y += 2
  doc.setDrawColor(...accent)
  doc.setLineWidth(1.5)
  doc.line(20, y, 70, y)

  y += 10

  // Tableau d'informations
  doc.setFontSize(10)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(...textDark)

  doc.text('Analysis Date', 20, y)
  doc.setFont('helvetica', 'bold')
  doc.text(
    d.toLocaleDateString('en-US', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    }),
    80,
    y,
  )

  y += 8
  doc.setFont('helvetica', 'normal')
  doc.text('Location', 20, y)
  doc.setFont('helvetica', 'bold')
  const locationName =
    props.location?.city ||
    props.location?.town ||
    props.location?.village ||
    props.location?.display_name ||
    `${props.location?.lat.toFixed(2)}°, ${Math.abs(props.location?.lon).toFixed(2)}°${props.location?.lon >= 0 ? 'E' : 'W'}`
  doc.text(locationName, 80, y)

  y += 8
  doc.setFont('helvetica', 'normal')
  doc.text('Coordinates', 20, y)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(...textGray)
  doc.text(
    `${props.location?.lat.toFixed(4)}° N, ${Math.abs(props.location?.lon).toFixed(4)}° ${props.location?.lon >= 0 ? 'E' : 'W'}`,
    80,
    y,
  )

  // === DONNÉES MÉTÉOROLOGIQUES ===
  y += 20

  doc.setTextColor(...textDark)
  doc.setFontSize(12)
  doc.setFont('helvetica', 'bold')
  doc.text('Weather Conditions', 20, y)

  y += 2
  doc.setDrawColor(...accent)
  doc.setLineWidth(1.5)
  doc.line(20, y, 80, y)

  y += 12

  // Tableau de données épuré
  const weatherData = [
    { label: 'Average Temperature', value: `${temperature.value} °C`, unit: '°C' },
    { label: 'Minimum Temperature', value: `${tMin.value} °C`, unit: '°C' },
    { label: 'Maximum Temperature', value: `${tMax.value} °C`, unit: '°C' },
    { label: 'Relative Humidity', value: `${humidity.value} %`, unit: '%' },
    { label: 'Wind Speed', value: `${wind.value} m/s`, unit: 'm/s' },
    { label: 'Atmospheric Pressure', value: `${pressure.value} kPa`, unit: 'kPa' },
    { label: 'Precipitation', value: `${rain.value} mm`, unit: 'mm' },
  ]

  // En-tête du tableau
  doc.setFillColor(249, 250, 251)
  doc.rect(20, y, 170, 8, 'F')

  doc.setDrawColor(...borderGray)
  doc.setLineWidth(0.3)
  doc.rect(20, y, 170, 8)

  doc.setTextColor(...textDark)
  doc.setFontSize(9)
  doc.setFont('helvetica', 'bold')
  doc.text('Parameter', 25, y + 5.5)
  doc.text('Value', 160, y + 5.5)

  y += 8

  // Lignes de données
  weatherData.forEach((item, index) => {
    // Ligne de séparation
    doc.setDrawColor(...borderGray)
    doc.setLineWidth(0.3)
    doc.line(20, y, 190, y)

    // Contenu
    doc.setTextColor(...textDark)
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(9)
    doc.text(item.label, 25, y + 5.5)

    doc.setFont('helvetica', 'bold')
    const valueWidth = doc.getTextWidth(item.value)
    doc.text(item.value, 185 - valueWidth, y + 5.5)

    y += 8
  })

  // Bordure finale du tableau
  doc.setDrawColor(...borderGray)
  doc.line(20, y, 190, y)

  // Bordures verticales du tableau
  doc.line(20, y - weatherData.length * 8 - 8, 20, y)
  doc.line(190, y - weatherData.length * 8 - 8, 190, y)

  // === FOOTER ===
  y = 270

  doc.setDrawColor(...borderGray)
  doc.setLineWidth(0.3)
  doc.line(20, y, 190, y)

  y += 6

  doc.setTextColor(...textGray)
  doc.setFontSize(8)
  doc.setFont('helvetica', 'normal')
  doc.text('Data source: NASA POWER API', 20, y)

  doc.text(`Page 1/1`, 190, y, { align: 'right' })

  // Sauvegarde
  const locationForFile = props.location?.name || props.location?.display_name || 'location'
  const fileName = `weather_report_${d.toISOString().split('T')[0]}_${locationForFile.replace(/[^a-zA-Z0-9]/g, '_')}.pdf`
  doc.save(fileName)
}

function resetView() {
  emit('reset-view')
}
</script>
