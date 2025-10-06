<template class="overflow-x-hidden font-mono">
  <div class="min-h-screen bg-black text-gray-100 flex flex-col">

    <section class="relative py-20 border-b border-gray-800 text-center">
      <h1 class="text-4xl md:text-5xl font-extrabold mb-4 text-white tracking-tight">
        WeatherMelon NASA Weather Intelligence
      </h1>
      <p class="max-w-3xl mx-auto text-gray-400 text-lg leading-relaxed">
        Built for explorers, scientists, and the simply curious this project transforms satellite data
        into visual, meaningful weather insights you can actually feel.
      </p>

      <div class="mt-10 flex justify-center">
        <a href="https://power.larc.nasa.gov/" target="_blank"
          class="relative flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-gray-100 border hover:bg-gray-700 border border-gray-700 rounded-lg text-gray-300 hover:text-white text-sm font-medium transition-colors duration-200">

          Learn more about NASA POWER API
        </a>
      </div>
    </section>

    <section class="max-w-5xl mx-auto px-6 py-16 space-y-12">
      <div class="bg-gray-900/60 p-6 rounded-xl border border-gray-800 hover:bg-gray-900/80 transition">
        <h2 class="text-2xl font-bold text-white mb-3">The Story</h2>
        <p class="text-gray-300 leading-relaxed">
          This project was born from the <span class=" font-semibold">NASA Space Apps Challenge 2025</span>.
          The goal is to bridge the gap between raw satellite data and real human understanding.
          We wanted a tool that doesn't just *show numbers* but it explains them, visualizes them,
          and helps people with suggesting random ideas & planning their day, wherever they are on Earth.
        </p>
      </div>

      <div class="bg-gray-900/60 p-6 rounded-xl border border-gray-800 hover:bg-gray-900/80 transition">
        <h2 class="text-2xl font-bold text-white mb-3">How We Calculate Weather Insights</h2>
        <p class="text-gray-300 leading-relaxed">
          All data originates from <span class="text-blue-400 font-semibold">NASA POWER</span> —
          a global climate database capturing decades of observations from space.
          We analyze the following parameters for every selected coordinate:
        </p>

        <ul class="list-disc list-inside  text-gray-400 mt-4 space-y-1">
          <li><strong>T2M</strong> : average air temperature (2 meters above ground)</li>
          <li><strong>RH2M</strong> : relative humidity</li>
          <li><strong>U2M & V2M</strong> : wind vector components combined to estimate speed</li>
          <li><strong>PS</strong> : surface air pressure</li>
          <li><strong>PRECTOTCORR</strong> : corrected precipitation totals</li>
        </ul>

        <p class="text-gray-400 mt-4 italic">
          A 10-year average is used to smooth out anomalies, giving a cleaner climate baseline
          for both historical and predictive analysis.
        </p>
      </div>

      <div class="bg-gray-900/60 p-6 rounded-xl border border-gray-800 hover:bg-gray-900/80 transition">
        <h2 class="text-2xl font-bold text-white mb-3">Data Storage & Privacy</h2>
        <p class="text-gray-300 leading-relaxed">
          No personal data is stored — ever. Every request is processed live using NASA’s open data APIs.
          Cached results are temporary and used only to speed up future requests.
        </p>
        <p class="text-gray-400 mt-3">
          If you’re logged in, your favorite locations are securely stored in your profile,
          so you can revisit and compare them at any time.
          Reports can be downloaded as <strong>PDF</strong> summaries for personal use or research.
        </p>
      </div>

      <div class="bg-gray-900/60 p-6 rounded-xl border border-gray-800 hover:bg-gray-900/80 transition">
        <h2 class="text-2xl font-bold text-white mb-3">Tech Stack</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
          <div v-for="tech in techs" :key="tech.name"
            class="bg-gray-800/40 border border-gray-700 rounded-lg p-3 text-center hover:bg-gray-800/70 transition">
            <p class="font-semibold text-gray-100">{{ tech.name }}</p>
            <p class="text-xs text-gray-500">{{ tech.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class=" backdrop-blur-sm border-t border-gray-800 py-16 px-6">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-3xl font-bold text-white mb-8 text-center">Frequently Asked Questions</h2>

        <div v-for="(item, index) in faq" :key="index" class="mb-6 border-b border-gray-800 pb-4">
          <button @click="toggle(index)"
            class="w-full flex justify-between items-center text-left text-gray-100 hover:text-white transition">
            <span class="text-lg font-semibold">{{ item.q }}</span>
            <svg :class="{ 'rotate-180': openIndex === index }" class="w-5 h-5 text-gray-400 transition-transform"
              fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <transition name="fade">
            <p v-if="openIndex === index" class="text-gray-400 mt-3 text-sm leading-relaxed">
              {{ item.a }}
            </p>
          </transition>
        </div>
      </div>
    </section>

    <footer class="py-6 border-t border-gray-800 text-center text-gray-500 text-sm">
      <p>
        © 2025 WeatherMelon
      </p>
      <p class="text-gray-600 mt-1">Space Apps Challenge |

        <a href="/https://github.com/Fabio345i/spaceappschallenge.git" class="text-gray-500 hover:underline">Github Open
          Source</a>

      </p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue"

const openIndex = ref(null)
const toggle = (i) => (openIndex.value = openIndex.value === i ? null : i)

const techs = [
  { name: "FastAPI", desc: "Python backend for NASA data aggregation" },
  { name: "Vue 3 + Vite", desc: "Reactive, modular, and lightning-fast frontend" },
  { name: "CesiumJS", desc: "3D Earth visualization with satellite precision" },
  { name: "NASA POWER", desc: "Primary source of climate variables" },
  { name: "Open-Meteo", desc: "Forecast refinement and live conditions" },
  { name: "jsPDF", desc: "Generate detailed weather reports locally" },
]

const faq = [
  {
    q: "How do you calculate the data?",
    a: "We process raw satellite parameters from NASA POWER using Python statistical models. Each value — temperature, wind, pressure, humidity — is normalized across 20+ years of observations to extract a climate pattern rather than a single reading.",
  },
  {
    q: "Can I save or download my reports?",
    a: "Yes. You can export your entire weather report as a high-quality PDF directly from the dashboard. Favorite locations are linked to your user account for easy access.",
  },
  {
    q: "How often are the datasets updated?",
    a: "NASA POWER updates its datasets daily, with a typical 24-hour delay from satellite observation to public availability.",
  },
  {
    q: "What happens when I change the date?",
    a: "The system recalculates values dynamically. For past dates, it loads historical means. For future dates, it predicts conditions based on long-term temperature and humidity trends.",
  },
  {
    q: "Are predictions reliable?",
    a: "Predictions are not perfect but statistically sound — we use a rolling historical window and variance analysis to infer upcoming conditions for the same calendar date.",
  },
]
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

button:focus {
  outline: none;
}
</style>
