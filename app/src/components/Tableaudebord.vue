<template>
  <div class="bg-gray-900 border border-gray-800 rounded-lg p-4">
    <h2 class="text-sm font-semibold text-white mb-4 uppercase tracking-wide">
      Current Conditions
    </h2>

    <div v-if="dataLoaded">
      <!--Localisation -->
      <div class="mb-4 pb-3 border-b border-gray-800">
        <p class="text-xs text-gray-400 mb-0.5">Location</p>
        <p class="text-sm font-medium text-white truncate">{{ displayName }}</p>
        <p class="text-xs text-gray-500">
          {{ props.location?.lat.toFixed(2) }}° / {{ props.location?.lon.toFixed(2) }}°
        </p>
      </div>
   
      <!-- Bloc confiance -->
<!-- Bloc Confiance -->
<div
  v-if="dataLoaded"
  class="mb-4 p-4 rounded-xl border border-gray-700 bg-gradient-to-br from-gray-800/60 to-gray-900/40 text-center relative overflow-hidden"
>
  <!-- Effet léger d'arrière-plan animé -->
  <div class="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_30%_20%,#3b82f6,transparent_70%)] pointer-events-none"></div>

  <p class="text-xs font-semibold tracking-wide uppercase mb-1 text-gray-300">
    {{ isFuturePrediction ? 'Confiance de la prédiction' : 'Données confirmées' }}
  </p>

  <div class="text-2xl mb-3"
       :class="isFuturePrediction ? '' : 'text-green-400'">
    {{ isFuturePrediction ? confiance + '%' : '100%' }}
  </div>

  <!-- Barre de progression -->
  <div class="w-full bg-gray-700/50 rounded-full h-4 overflow-hidden">
    <div
      :style="{
        width: confiance + '%',
        background: `linear-gradient(90deg, ${couleurConfiance}, #60a5fa)`
      }"
      class="h-4 rounded-full transition-all duration-700 shadow-[0_0_10px_var(--tw-shadow-color)]"
     
    ></div>
  </div>

  <!-- Légende -->
  <p class="mt-2 text-xs text-gray-400">
    {{ isFuturePrediction
      ? 'Plus la date est éloignée, moins la précision est garantie'
      : 'Ces données proviennent de l’historique réel' }}
  </p>
</div>



      <!-- météo -->
      <div class="mt-6 bg-gray-800/40 border border-gray-700 rounded-lg p-5 m-2 text-center">
        <p class="text-sm font-medium text-white mb-1">Analyse rapide</p>
        <p class="text-gray-300 text-sm leading-relaxed">
          {{ weatherSummary }}
        </p>
      </div>

      <!-- Suggestions -->
      <div class="mt-6 bg-gray-800/50 p-4 rounded-lg border border-gray-700 m-2">
        <h3 class="text-sm text-gray-400 uppercase font-semibold mb-2">Suggestion du jour</h3>
        <p class="text-lg font-bold text-white">{{ activitySuggestion.title }}</p>
        <p class="text-sm text-gray-300 mt-1">{{ activitySuggestion.activity }}</p>

        <div class="mt-3 bg-gray-900/60 rounded-lg border border-gray-800 p-3">
          <h4 class="text-xs uppercase text-gray-400 font-semibold mb-2">Préparatifs recommandés</h4>
          <ul class="list-disc list-inside text-xs text-gray-400 text-left space-y-1">
            <li v-for="(item, i) in activitySuggestion.preparations" :key="i">{{ item }}</li>
          </ul>
        </div>

        <p class="text-xs text-gray-500 mt-2 italic">{{ activitySuggestion.tips }}</p>
      </div>

      <!-- Statistiques -->
      <div class="grid grid-cols-2 gap-3 mt-4">
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
 class="relative flex items-center gap-2 px-5 py-2.5
         rounded-xl font-semibold text-gray-100
         border border-gray-700
          from-gray-800 via-gray-900 to-black
         hover:from-blue-700 hover:via-blue-800 hover:to-gray-900
         hover:border-gray-600 hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]
         active:scale-95 transition-all duration-300 ease-out
         overflow-hidden">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          Download Report
        </button>

        <button
          @click="resetView"
          class="py-2 px-3 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-300
           hover:text-white text-sm font-medium transition-colors duration-200 hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]
         active:scale-95 transition-all duration-300 ease-out
         overflow-hidden"
        >
          Reset View
        </button>
      </div>
    </div>

    <!-- Aucun résultat -->
    <div v-else class="text-center py-6 text-gray-600">
      <svg class="w-10 h-10 mx-auto mb-2 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <p class="text-xs">Select a location and date</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { jsPDF } from 'jspdf'
import axios from 'axios'

// ===Props / Emit ===
const props = defineProps({
  location: { type: Object, default: null },
  selectedDate: { type: Date, default: () => new Date() },
})

const isFuturePrediction = computed(() => {
  const today = new Date()
  const selected = new Date(props.selectedDate)
  return selected > today
})

const k = 0.001

const confiance = computed(() => {
  if (!isFuturePrediction.value) return 100

  const today = new Date()
  const selected = new Date(props.selectedDate)
  const joursFuturs = Math.max(0, Math.ceil((selected - today) / (1000 * 60 * 60 * 24)))

  return Math.round(80 * Math.exp(-k * (joursFuturs - 1)))
})

const couleurConfiance = computed(() => {
  if (confiance.value > 75) return '#22c55e'
  if (confiance.value > 50) return '#facc15'
  return '#ef4444'
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
  () => props.location?.geojson?.properties?.display_name || 'Selected Location'
)

const weatherData = computed(() => [
  { name: 'Temp moyenne', value: `${temperature.value}°C` },
  { name: 'Min / Max', value: `${tMin.value}°C / ${tMax.value}°C` },
  { name: 'Humidité', value: `${humidity.value}%` },
  { name: 'Vent', value: `${wind.value} m/s` },
  { name: 'Pression', value: `${pressure.value} kPa` },
  { name: 'Pluie', value: `${rain.value} mm` },
])

watch(() => [props.location, props.selectedDate], ([loc, date]) => {
  if (loc?.lat && loc?.lon) fetchWeather(loc, date)
  else dataLoaded.value = false
}, { deep: true })

async function fetchWeather(loc, date) {
  try {
    const d = new Date(date)
    const y = d.getUTCFullYear()
    const m = String(d.getUTCMonth() + 1).padStart(2, "0")
    const day = String(d.getUTCDate()).padStart(2, "0")
    const dateStr = `${y}${m}${day}`
    dataLoaded.value = false

    const { data } = await axios.get("http://127.0.0.1:8000/algo/daily/analyse", {
      params: { lat: loc.lat, lon: loc.lon, day, month: m, years: 20 }
    })
    const a = data || {}

    temperature.value = a.T_moyenne?.toFixed(1) ?? "--"
    tMin.value = a.Tmin_moyenne?.toFixed(1) ?? "--"
    tMax.value = a.Tmax_moyenne?.toFixed(1) ?? "--"
    humidity.value = a.humidite_moyenne?.toFixed(0) ?? "--"
    wind.value = a.vent_moyen_m_s?.toFixed(1) ?? "--"
    pressure.value = a.pression_moy_kPa?.toFixed(1) ?? "--"
    rain.value = (a.precipitation_totale ?? 0).toFixed(1)

    dataLoaded.value = true
  } catch (e) {
    console.error("Erreur API :", e)


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

const weatherSummary = computed(() => {
  const t = Number(temperature.value)
  const h = Number(humidity.value)
  const w = Number(wind.value)
  const r = Number(rain.value)
  if (isNaN(t) || isNaN(h) || isNaN(w)) return "Analyse en cours..."

  let summary = ""
  if (t < 0) summary += " Froid intense"
  else if (t < 10) summary += "Temps froid"
  else if (t < 20) summary += "Temps frais"
  else if (t < 28) summary += "Agréable"
  else summary += "Chaleur marquée"

  if (r > 5) summary += ", risque de pluie"
  if (h > 80) summary += ", humidité élevée"
  if (w > 10) summary += ", vent sensible"

  return summary + "."
})

const activitySuggestion = computed(() => {
  const t = Number(temperature.value)
  const r = Number(rain.value)
  const w = Number(wind.value)
  const h = Number(humidity.value)

  if (r > 5) {
    return {
      title: "Journée pluvieuse",
      activity: "Idéale pour rester au chaud — film, lecture ou détente.",
      tips: "Pense à ton parapluie",
      preparations: ["Parapluie ou imperméable", "Chaussures étanches", "Boisson chaude", "Éviter les trajets longs"]
    }
  }
  if (t <= 0) {
    return {
      title: "Temps froid",
      activity: "Ski, patin, ou soirée cocooning à la maison.",
      tips: "Habille-toi chaudement",
      preparations: ["Gants et bonnet", "S'assure d'avoir des vêtements chauds", "Surveiller les routes glacées"]
    }
  }
  if (t > 25 && r < 2) {
    return {
      title: "Belle journée",
      activity: "Parfaite pour une sortie nature ou un BBQ.",
      tips: "Pense à la crème solaire ",
      preparations: ["Crème solaire ", "Bouteille d’eau", "Lunettes de soleil", "Vêtements légers"]
    }
  }
  if (w > 25) {
    return {
      title: " Vent fort",
      activity: "Privilégie les activités intérieures.",
      tips: "Évite les balades en vélo",
      preparations: ["Veste coupe-vent", "Bien attacher les objets dehors", "Reporter les sorties en altitude"]
    }
  }
  return {
    title: " Météo douce",
    activity: "Idéale pour marcher ou flâner en ville.",
    tips: "Profite du plein air",
    preparations: ["Veste légère", "Chaussures confortables", "Planifier une sortie tranquille"]
  }
})

function generatePDF() {
  const doc = new jsPDF()
  const d = new Date(props.selectedDate)

  const primary = [243, 244, 246]        // texte principal (gray-100)
  const accent = [156, 163, 175]         // gris subtil (gray-400)
  const background = [0, 0, 0]           // fond principal noir
  const backgroundSecondary = [17, 24, 39] // gray-900
  const border = [31, 41, 55]            // gray-800
  const borderLight = [55, 65, 81]       // gray-700
  const textGray = [209, 213, 219]       // gray-300
  const textSubtle = [156, 163, 175]     // gray-400

  doc.setFillColor(...background)
  doc.rect(0, 0, 210, 297, 'F')

  doc.setFont('helvetica', 'bold')
  doc.setFontSize(22)
  doc.setTextColor(...primary)
  doc.text("NASA Weather Report", 20, 22)

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  doc.setTextColor(...textSubtle)
  doc.text(
    `Generated: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`,
    20,
    29
  )

  doc.setDrawColor(...border)
  doc.setLineWidth(0.4)
  doc.line(20, 33, 190, 33)

  let y = 45
  doc.setTextColor(...textGray)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(13)
  doc.text("General Information", 20, y)

  y += 3
  doc.setDrawColor(...borderLight)
  doc.setLineWidth(1)
  doc.line(20, y, 75, y)

  y += 10
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(11)
  doc.setTextColor(...primary)
  doc.text(`Location:`, 20, y)
  doc.setFont('helvetica', 'bold')
  doc.text(`${displayName.value}`, 60, y)

  y += 7
  doc.setFont('helvetica', 'normal')
  doc.text(`Date:`, 20, y)
  doc.setFont('helvetica', 'bold')
  doc.text(
    `${d.toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' })}`,
    60,
    y
  )

  y += 10
  doc.setDrawColor(...borderLight)
  doc.line(20, y, 190, y)

  y += 10
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...textGray)
  doc.setFontSize(13)
  doc.text("Weather Summary", 20, y)

  y += 3
  doc.setDrawColor(...borderLight)
  doc.setLineWidth(1)
  doc.line(20, y, 85, y)

  y += 10
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  doc.setTextColor(...textSubtle)
  const summary = doc.splitTextToSize(weatherSummary.value, 170)
  doc.text(summary, 20, y)

  // Bloc data météo
  y += 20
  const weatherData = [
    ["Average Temp", `${temperature.value} °C`],
    ["Min / Max", `${tMin.value} °C / ${tMax.value} °C`],
    ["Humidity", `${humidity.value} %`],
    ["Wind Speed", `${wind.value} m/s`],
    ["Pressure", `${pressure.value} kPa`],
    ["Precipitation", `${rain.value} mm`],
  ]

  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...textGray)
  doc.text("Key Weather Data", 20, y)
  y += 5

  doc.setDrawColor(...border)
  doc.setFillColor(...backgroundSecondary)
  doc.rect(20, y, 170, 45, 'F')

  doc.setFont('helvetica', 'normal')
  doc.setTextColor(...primary)
  let ty = y + 9
  weatherData.forEach(([label, value]) => {
    doc.text(label, 25, ty)
    doc.text(value, 185, ty, { align: 'right' })
    ty += 7
  })

  y = ty + 12
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(13)
  doc.setTextColor(...textGray)
  doc.text("Suggested Activity", 20, y)

  y += 3
  doc.setDrawColor(...borderLight)
  doc.line(20, y, 80, y)

  y += 10
  doc.setTextColor(...primary)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(12)
  doc.text(activitySuggestion.value.title, 20, y)

  y += 8
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  doc.setTextColor(...textGray)
  doc.text(doc.splitTextToSize(activitySuggestion.value.activity, 170), 20, y)

  y += 10
  doc.setFont('helvetica', 'italic')
  doc.setFontSize(9)
  doc.setTextColor(...textSubtle)
  doc.text(activitySuggestion.value.tips, 20, y)

  y += 10
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...textGray)
  doc.setFontSize(11)
  doc.text("Preparations Checklist:", 20, y)

  y += 6
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(9)
  doc.setTextColor(...textSubtle)
  activitySuggestion.value.preparations.forEach((p) => {
    doc.text(`• ${p}`, 25, y)
    y += 5
  })

  y = 275
  doc.setDrawColor(...border)
  doc.line(20, y, 190, y)
  y += 6

  doc.setTextColor(...textSubtle)
  doc.setFontSize(8)
  doc.text("Data: NASA POWER, NLDAS2, Open-Meteo", 20, y)
  doc.text("© 2025 SpaceApps – fait par Les GOLMONS :)", 190, y, { align: "right" })

  const filename = `weather_report_${d.toISOString().split("T")[0]}_${displayName.value.replace(/[^a-zA-Z0-9]/g, "_")}.pdf`
  doc.save(filename)
}


function resetView() {
  emit('reset-view')
}
</script>
