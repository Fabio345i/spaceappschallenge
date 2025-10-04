<template>
  <div
    class="min-h-screen from-slate-900 via-slate-800 to-slate-900 text-white flex flex-col items-center justify-center p-6"
  >
    <!-- HEADER -->
    <header class="text-center mb-14 animate-fade-in">
      <h1
        class="text-5xl font-extrabold tracking-tight bg-clip-text text-transparent  from-sky-400 via-indigo-400 to-violet-500 drop-shadow-xl"
      >
        🌌 Tableau de bord météo NASA
      </h1>
      <p class="text-gray-400 mt-3 text-lg">
        Analyse atmosphérique intelligente — Données satellites & modèles
        <span class="text-sky-400">NASA</span>
      </p>
    </header>

    <!-- CONTAINER -->
    
<section
  class="w-full max-w-6xl bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-10 shadow-[0_0_40px_-10px_rgba(56,189,248,0.25)] transition-all duration-300 hover:shadow-[0_0_60px_-8px_rgba(56,189,248,0.4)] hover:scale-[1.01]"
>

      <!-- SEARCH BAR -->
      <div
        class="flex flex-col sm:flex-row items-center justify-between gap-4 mb-10"
      >
        <input
          v-model="location"
          type="text"
          placeholder="🔍 Entrez un lieu (ex: Québec, Canada)"
          class="bg-white/10 border border-white/20 text-white placeholder-gray-400 rounded-2xl px-5 py-3 w-full sm:w-2/3 focus:outline-none focus:ring-2 focus:ring-sky-400 transition-all"
        />
        <button
          @click="fetchWeather"
          class=" from-sky-500 to-indigo-600 text-white font-semibold px-8 py-3 rounded-2xl shadow-md hover:shadow-sky-500/30 hover:scale-105 active:scale-95 transition-all duration-200"
        >
          Rechercher
        </button>
      </div>

      <!-- DATA GRID -->
      <transition name="fade">
        <div
          v-if="dataLoaded"
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          <div
            v-for="(item, i) in weatherData"
            :key="i"
            class="bg-white/10 border border-white/20 rounded-2xl p-5 flex flex-col items-center justify-center text-center shadow-inner hover:bg-white/15 transition-all"
          >
            <div class="text-4xl mb-2" v-html="item.icon"></div>
            <h3 class="text-gray-300 text-sm uppercase tracking-wider">
              {{ item.name }}
            </h3>
            <p
              class="text-2xl font-bold bg-clip-text text-transparent  from-sky-400 to-indigo-400"
            >
              {{ item.value }}
            </p>
            <p class="text-gray-400 text-sm">{{ item.unit }}</p>
          </div>
        </div>

        <!-- EMPTY STATE -->
        <div
          v-else
          class="text-center py-16 text-gray-400 italic flex flex-col items-center gap-2"
        >
          <div class="text-5xl animate-bounce">🌍</div>
          <p>Entrez un lieu pour afficher les conditions météorologiques.</p>
        </div>
      </transition>
    </section>

    <!-- FOOTER -->
    <footer class="mt-12 text-gray-500 text-sm text-center">
      Données fournies par
      <span class="text-sky-400 font-medium">NASA GES DISC</span> et
      <span class="text-indigo-400 font-medium">Open-Meteo API</span>.
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"

const location = ref("")
const temperature = ref("--")
const precipitation = ref("--")
const windSpeed = ref("--")
const airQuality = ref("--")
const dataLoaded = ref(false)

const weatherData = computed(() => [
  {
    name: "Température",
    value: `${temperature.value} °C`,
    unit: "°C",
    icon: "🌡️",
  },
  {
    name: "Précipitations",
    value: `${precipitation.value} mm`,
    unit: "mm",
    icon: "🌧️",
  },
  {
    name: "Vent",
    value: `${windSpeed.value} m/s`,
    unit: "m/s",
    icon: "🌬️",
  },
  {
    name: "Qualité de l’air",
    value: airQuality.value,
    unit: "AQI",
    icon: "🌫️",
  },
])

function fetchWeather() {
  if (!location.value) return alert("Veuillez entrer un lieu")

  // Simulation (à remplacer par ton API réelle)
  temperature.value = (Math.random() * 30).toFixed(1)
  precipitation.value = (Math.random() * 10).toFixed(1)
  windSpeed.value = (Math.random() * 15).toFixed(1)
  airQuality.value = ["Bonne", "Moyenne", "Mauvaise"][
    Math.floor(Math.random() * 3)
  ]

  dataLoaded.value = true
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.animate-fade-in {
  animation: fadeIn 1.2s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
