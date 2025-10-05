<template>
  <div class="p-6 bg-gray-900 text-gray-100 min-h-screen">
    <h2 class="text-3xl font-bold mb-8 text-center">🌦️ Données de précipitations NASA</h2>

    <div class="flex flex-wrap justify-center gap-4 mb-8">
      <input v-model="startDate" type="date" class="input-field" />
      <input v-model="endDate" type="date" class="input-field" />
      <input v-model="latitude" type="number" step="0.1" class="input-field w-32" placeholder="Latitude" />
      <input v-model="longitude" type="number" step="0.1" class="input-field w-32" placeholder="Longitude" />
      <button @click="fetchRainData" class="btn-primary">
        Charger les données
      </button>

    </div>
          <!-- <pre class="text-sm text-gray-300 mt-4">{{ weatherData }}</pre> -->
          
<div v-if="!loading && weatherData.length > 0" class="overflow-x-auto mt-6">
  <table class="min-w-full border border-gray-700 rounded-lg overflow-hidden">
    <thead class="bg-gray-800 text-gray-200">
      <tr>
        <th class="px-4 py-2 text-left">Date</th>
        <th class="px-4 py-2 text-right">🌧️Précipitations (mm)</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(item, index) in weatherData"
        :key="index"
        class="hover:bg-gray-800/60 border-b border-gray-700"
      >
        <td class="px-4 py-2">{{ formatDate(item.time) }}</td>
<td
  class="px-4 py-2 text-right font-semibold"
  :class="{
    'text-blue-400': item.data < 1,
    'text-blue-500': item.data >= 1 && item.data < 5,
    'text-blue-300': item.data >= 5
  }"
>
  {{ item.data.toFixed(3) }}
</td>
      </tr>
    </tbody>
  </table>
</div>



    <div v-if="loading" class="flex justify-center items-center py-10">
      <div class="loader"></div>
      <span class="ml-3 text-gray-300">Chargement des données...</span>
    </div>

    <div v-else-if="error" class="text-red-500 text-center">{{ error }}</div>

    <div v-if="!loading && weatherData.length > 0" class="space-y-10">
      <div class="overflow-x-auto">
        <table class="min-w-full border border-gray-700 rounded-lg overflow-hidden">
          <thead class="bg-gray-800 text-gray-200">
            <tr>
              <th class="px-4 py-2 text-left">Date</th>
              <th class="px-4 py-2 text-right">Précipitations (mm)</th>
            </tr>
          </thead>
         <tbody>
  <ul>
    <li v-for="(item, i) in weatherData" :key="i">
      {{ item.time }} — {{ item.data }}
    </li>
  </ul>
</tbody>

        </table>
      </div>

      <div class="h-[400px] bg-gray-800/40 rounded-lg p-4 shadow-md">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart :data="weatherData">
            <CartesianGrid stroke="#444" strokeDasharray="3 3" />
            <XAxis dataKey="time" stroke="#aaa" />
            <YAxis stroke="#aaa" />
            <Tooltip
              :contentStyle="{ backgroundColor: '#1f2937', borderColor: '#374151' }"
              labelStyle="color: #f3f4f6"
            />
            <Legend />
            <Line type="monotone" dataKey="data" stroke="#3b82f6" strokeWidth="3" dot />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts"

const startDate = ref("2023-09-01")
const endDate = ref("2023-09-10")
const latitude = ref(46.8)
const longitude = ref(-71.2)
const weatherData = ref([])
const loading = ref(false)
const error = ref("")

const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString("fr-CA")

const fetchRainData = async () => {
  loading.value = true
  error.value = ""
  weatherData.value = []

  try {
    const res = await axios.get(
      `http://127.0.0.1:8000/weather/rainfall?start_date=${startDate.value}&end_date=${endDate.value}&latitude=${latitude.value}&longitude=${longitude.value}`
    )
    console.log("✅ Données brutes reçues :", res.data) // <--- ajoute ça
weatherData.value = res.data.data
    console.log("✅ Données NASA :", weatherData.value)
  } catch (err) {
    error.value = "Impossible de charger les données météo."
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@reference "tailwindcss";

.input-field {
  @apply bg-gray-800 p-2 rounded text-gray-100 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500;
}

.btn-primary {
  @apply px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition duration-200;
}

.loader {
  width: 32px;
  height: 32px;
  border: 4px solid #1e40af;
  border-top: 4px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
