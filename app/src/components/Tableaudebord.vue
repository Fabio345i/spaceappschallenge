<template>
  <div class="bg-gray-900 border border-gray-800 rounded-lg p-4">
    <h2 class="text-sm font-semibold text-white mb-4 uppercase tracking-wide">
      Current Conditions
    </h2>

    <!-- 🔥 Skeleton only if actually loading a location -->
    <template v-if="loading && hasLocation">
      <div class="animate-pulse space-y-4">
        <div class="h-4 w-40 bg-gray-700/60 rounded"></div>
        <div class="bg-gray-800/40 border border-gray-700 rounded-lg p-5">
          <div class="h-3 w-28 bg-gray-700/60 rounded mb-3"></div>
          <div class="h-3 w-full bg-gray-700/50 rounded mb-1"></div>
          <div class="h-3 w-3/4 bg-gray-700/50 rounded"></div>
        </div>
        <div class="bg-gray-800/50 p-4 rounded-lg border border-gray-700 space-y-3">
          <div class="h-3 w-32 bg-gray-700/60 rounded"></div>
          <div class="h-4 w-1/2 bg-gray-600/60 rounded"></div>
          <div class="h-3 w-full bg-gray-700/50 rounded"></div>
          <div class="h-3 w-3/4 bg-gray-700/50 rounded"></div>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div v-for="n in 4" :key="n" class="bg-gray-800/40 rounded-lg p-3">
            <div class="h-3 w-20 bg-gray-700/60 rounded mb-2"></div>
            <div class="h-5 w-16 bg-gray-600/60 rounded"></div>
          </div>
        </div>
        <div class="flex gap-2 mt-4">
          <div class="h-9 w-32 bg-gray-700/60 rounded"></div>
          <div class="h-9 w-24 bg-gray-700/60 rounded"></div>
        </div>
      </div>
    </template>

    <!-- 🔥 Actual content if data is loaded OR no location (we show 0s) -->
    <template v-else>
      <div class="mt-6 bg-gray-800/40 border border-gray-700 rounded-lg p-5 m-2 text-center">
        <p class="text-sm font-medium text-white mb-1">Quick Analysis</p>
        <p class="text-gray-300 text-sm leading-relaxed">
          {{ weatherSummary }}
        </p>
      </div>

      <div class="mt-6 bg-gray-800/50 p-4 rounded-lg border border-gray-700 m-2">
        <h3 class="text-sm text-gray-400 uppercase font-semibold mb-2">Suggested Activity</h3>
        <p class="text-lg font-bold text-white">{{ activitySuggestion.title }}</p>
        <p class="text-sm text-gray-300 mt-1">{{ activitySuggestion.activity }}</p>

        <div class="mt-3 bg-gray-900/60 rounded-lg border border-gray-800 p-3">
          <h4 class="text-xs uppercase text-gray-400 font-semibold mb-2">
            Recommended Preparations
          </h4>
          <ul class="list-disc list-inside text-xs text-gray-400 text-left space-y-1">
            <li v-for="(item, i) in activitySuggestion.preparations" :key="i">{{ item }}</li>
          </ul>
        </div>

        <p class="text-xs text-gray-500 mt-2 italic">{{ activitySuggestion.tips }}</p>
      </div>

      <div class="grid grid-cols-2 gap-3 mt-4">
        <div v-for="(item, i) in weatherData" :key="i" class="bg-gray-800/40 rounded-lg p-3">
          <p class="text-xs text-gray-400 mb-1">{{ item.name }}</p>
          <p class="text-lg font-semibold text-white">{{ item.value }}</p>
        </div>
      </div>

      <div class="flex gap-2 mt-6">
        <button
          @click="generatePDF"
          class="relative flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-gray-100 border hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-300 hover:text-white text-sm font-medium transition-colors duration-200"
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
    </template>
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

const loading = ref(false)
const dataLoaded = ref(false)
const hasLocation = ref(false)

const temperature = ref('0')
const tMin = ref('0')
const tMax = ref('0')
const humidity = ref('0')
const wind = ref('0')
const pressure = ref('0')
const rain = ref('0')

const displayName = computed(
  () => props.location?.geojson?.properties?.display_name || 'Selected Location',
)

const weatherData = computed(() => [
  { name: 'Average Temp', value: `${temperature.value}°C` },
  { name: 'Min / Max', value: `${tMin.value}°C / ${tMax.value}°C` },
  { name: 'Humidity', value: `${humidity.value}%` },
  { name: 'Wind', value: `${wind.value} m/s` },
  { name: 'Pressure', value: `${pressure.value} kPa` },
  // { name: 'Precipitation', value: `${rain.value} mm` },
])

watch(
  () => [props.location, props.selectedDate],
  ([loc, date]) => {
    if (loc?.lat && loc?.lon) {
      hasLocation.value = true
      fetchWeather(loc, date)
    } else {
      hasLocation.value = false
      loading.value = false
      dataLoaded.value = true
      temperature.value =
        tMin.value =
        tMax.value =
        humidity.value =
        wind.value =
        pressure.value =
        rain.value =
          '0'
    }
  },
  { deep: true },
)

function isPastOrTodayUTC(date) {
  const today = new Date()
  const dUTC = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()))
  const tUTC = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()))
  return dUTC.getTime() <= tUTC.getTime()
}

async function fetchWeather(loc, date) {
  loading.value = true
  dataLoaded.value = false

  const d = new Date(date)
  const y = d.getUTCFullYear()
  const m = String(d.getUTCMonth() + 1).padStart(2, '0')
  const day = String(d.getUTCDate()).padStart(2, '0')
  const dateStr = `${y}${m}${day}`

  try {
    if (isPastOrTodayUTC(d)) {
      const { data } = await axios.get('https://spaceappschallenge-r59t.onrender.com/merra2/power/daily', {
        params: { lat: loc.lat, lon: loc.lon, start: dateStr, end: dateStr },
      })

      const p = data.parameters
      temperature.value = Object.values(p.T2M || {})[0]?.toFixed(1) ?? '0'
      tMin.value = Object.values(p.T2M_MIN || {})[0]?.toFixed(1) ?? '0'
      tMax.value = Object.values(p.T2M_MAX || {})[0]?.toFixed(1) ?? '0'
      humidity.value = Object.values(p.RH2M || {})[0]?.toFixed(0) ?? '0'
      const u = Object.values(p.U2M || {})[0]
      const v = Object.values(p.V2M || {})[0]
      wind.value = (u != null && v != null ? Math.sqrt(u * u + v * v) : 0).toFixed(1)
      pressure.value = Object.values(p.PS || {})[0]?.toFixed(1) ?? '0'
      rain.value = Object.values(p.PRECTOTCORR || {})[0]?.toFixed(1) ?? '0'
      dataLoaded.value = true
    } else {
      const { data: p } = await axios.get('https://spaceappschallenge-r59t.onrender.com/algo/daily/predict', {
        params: {
          lat: loc.lat,
          lon: loc.lon,
          day,
          month: m,
          base_years: 10,
          future_year: y,
          window_days: 3,
        },
      })
      const safe = (v) => (v != null && !Number.isNaN(Number(v)) ? Number(v) : null)
      temperature.value = safe(p.T_moyenne)?.toFixed(1) ?? '0'
      tMin.value = safe(p.Tmin_ajustee ?? p.Tmin_base)?.toFixed(1) ?? '0'
      tMax.value = safe(p.Tmax_ajustee ?? p.Tmax_base)?.toFixed(1) ?? '0'
      humidity.value = safe(p.humidite_moyenne)?.toFixed(0) ?? '0'
      wind.value = safe(p.vent_moyen_m_s)?.toFixed(1) ?? '0'
      pressure.value = safe(p.pression_moy_kPa)?.toFixed(1) ?? '0'
      try {
        const { data: r } = await axios.get('https://spaceappschallenge-r59t.onrender.com/weather/rainfall', {
          params: { lat: loc.lat, lon: loc.lon, start: dateStr, end: dateStr },
        })
        const obj = r?.data || {}
        rain.value = obj[dateStr] != null ? Number(obj[dateStr]).toFixed(1) : '0'
      } catch {
        rain.value = '0'
      }
      dataLoaded.value = true
    }
  } catch {
    temperature.value =
      tMin.value =
      tMax.value =
      humidity.value =
      wind.value =
      pressure.value =
      rain.value =
        '0'
    dataLoaded.value = false
  } finally {
    loading.value = false
  }
}

const weatherSummary = computed(() => {
  const t = Number(temperature.value)
  const h = Number(humidity.value)
  const w = Number(wind.value)
  const r = Number(rain.value)
  if (isNaN(t) || isNaN(h) || isNaN(w)) return 'Analysis in progress...'

  let summary = ''
  if (t < 0) summary += 'Severe cold'
  else if (t < 10) summary += 'Cold weather'
  else if (t < 20) summary += 'Cool'
  else if (t < 28) summary += 'Pleasant'
  else summary += 'Hot'

  if (r > 5) summary += ', possible rain'
  if (h > 80) summary += ', high humidity'
  if (w > 10) summary += ', windy'
  return summary + '.'
})

const activitySuggestion = computed(() => {
  const t = Number(temperature.value)
  const r = Number(rain.value)
  const w = Number(wind.value)

  if (r > 5)
    return {
      title: 'Rainy day',
      activity: 'Perfect to stay warm — movie, reading or relaxing.',
      tips: 'Bring an umbrella',
      preparations: ['Umbrella', 'Waterproof shoes', 'Hot drink', 'Avoid long trips'],
    }
  if (t <= 0)
    return {
      title: 'Cold weather',
      activity: 'Skiing, skating, or cozy evening at home.',
      tips: 'Dress warmly',
      preparations: ['Gloves', 'Warm clothes', 'Watch for icy roads'],
    }
  if (t > 25 && r < 2)
    return {
      title: 'Beautiful day',
      activity: 'Perfect for outdoor activities or BBQ.',
      tips: 'Use sunscreen',
      preparations: ['Sunscreen', 'Water bottle', 'Sunglasses', 'Light clothes'],
    }
  if (w > 25)
    return {
      title: 'Strong wind',
      activity: 'Better to do indoor activities.',
      tips: 'Avoid cycling trips',
      preparations: ['Windbreaker jacket', 'Secure outdoor objects', 'Avoid mountain trips'],
    }
  return {
    title: 'Mild weather',
    activity: 'Great for walking or city exploring.',
    tips: 'Enjoy fresh air',
    preparations: ['Light jacket', 'Comfortable shoes', 'Plan a chill outing'],
  }
})

function generatePDF() {
  const doc = new jsPDF()
  const d = new Date(props.selectedDate)

  const primary = [243, 244, 246]
  const accent = [156, 163, 175]
  const background = [0, 0, 0]
  const backgroundSecondary = [17, 24, 39]
  const border = [31, 41, 55]
  const borderLight = [55, 65, 81]
  const textGray = [209, 213, 219]
  const textSubtle = [156, 163, 175]

  doc.setFillColor(...background)
  doc.rect(0, 0, 210, 297, 'F')

  doc.setFont('helvetica', 'bold')
  doc.setFontSize(22)
  doc.setTextColor(...primary)
  doc.text('NASA Weather Report', 20, 22)

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  doc.setTextColor(...textSubtle)
  doc.text(
    `Generated: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`,
    20,
    29,
  )

  doc.setDrawColor(...border)
  doc.setLineWidth(0.4)
  doc.line(20, 33, 190, 33)

  let y = 45
  doc.setTextColor(...textGray)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(13)
  doc.text('General Information', 20, y)

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
    y,
  )

  y += 10
  doc.setDrawColor(...borderLight)
  doc.line(20, y, 190, y)

  y += 10
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...textGray)
  doc.setFontSize(13)
  doc.text('Weather Summary', 20, y)

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

  y += 20
  const weatherData = [
    ['Average Temp', `${temperature.value} °C`],
    ['Min / Max', `${tMin.value} °C / ${tMax.value} °C`],
    ['Humidity', `${humidity.value} %`],
    ['Wind Speed', `${wind.value} m/s`],
    ['Pressure', `${pressure.value} kPa`],
    ['Precipitation', `${rain.value} mm`],
  ]

  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...textGray)
  doc.text('Key Weather Data', 20, y)
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
  doc.text('Suggested Activity', 20, y)

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
  doc.text('Preparations Checklist:', 20, y)

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
  doc.text('Data: NASA POWER, NLDAS2, Open-Meteo', 20, y)
  doc.text('© 2025 SpaceApps – made by Les GOLMONS :)', 190, y, { align: 'right' })

  const filename = `weather_report_${d.toISOString().split('T')[0]}_${displayName.value.replace(/[^a-zA-Z0-9]/g, '_')}.pdf`
  doc.save(filename)
}

function resetView() {
  emit('reset-view')
}
</script>
