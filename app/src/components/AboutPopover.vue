<template>
  <transition name="fade-zoom">
    <div
      v-if="visible"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      @click.self="close"
    >
      <div
        class="bg-gray-900 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] mx-4 p-6 text-gray-100 relative overflow-y-auto custom-scroll"
      >
        <!-- Bouton fermeture -->
        <button
          @click="close"
          class="absolute top-3 right-3 text-gray-400 hover:text-white transition"
        >
          ✕
        </button>

        <!-- Contenu -->
        <section class="relative text-center mb-10">
          <h1 class="text-4xl md:text-5xl font-extrabold mb-4 text-white tracking-tight">
            WeatherMellon NASA Weather Intelligence
          </h1>
          <p class="max-w-3xl mx-auto text-gray-400 text-lg leading-relaxed">
            Built for explorers, scientists, and the simply curious — this project transforms
            satellite data into visual, meaningful weather insights you can actually feel.
          </p>

          <div class="mt-10 flex justify-center">
            <a
              href="https://power.larc.nasa.gov/"
              target="_blank"
              class="relative flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-gray-100 border hover:bg-gray-700 border border-gray-700 text-gray-300 hover:text-white text-sm font-medium transition-colors duration-200"
            >
              Learn more about NASA POWER API
            </a>
          </div>
        </section>

        <!-- Sections -->
        <section class="space-y-12">
          <div
            class="bg-gray-900/60 p-6 rounded-xl border border-gray-800 hover:bg-gray-900/80 transition"
          >
            <h2 class="text-2xl font-bold text-white mb-3">The Story</h2>
            <p class="text-gray-300 leading-relaxed">
              This project was born from the
              <span class="font-semibold">NASA Space Apps Challenge 2025</span>. The goal is to
              bridge the gap between raw satellite data and real human understanding. We wanted a
              tool that doesn't just <em>show numbers</em> but explains them, visualizes them, and
              helps people plan their day, wherever they are on Earth.
            </p>
          </div>

          <div
            class="bg-gray-900/60 p-6 rounded-xl border border-gray-800 hover:bg-gray-900/80 transition"
          >
            <h2 class="text-2xl font-bold text-white mb-3">How We Calculate Weather Insights</h2>
            <p class="text-gray-300 leading-relaxed">
              All data originates from
              <span class="text-blue-400 font-semibold">NASA POWER</span> — a global climate
              database capturing decades of observations from space. We analyze:
            </p>

            <ul class="list-disc list-inside text-gray-400 mt-4 space-y-1">
              <li><strong>T2M</strong> : average air temperature (2 m above ground)</li>
              <li><strong>RH2M</strong> : relative humidity</li>
              <li><strong>U2M & V2M</strong> : wind vector components (speed & direction)</li>
              <li><strong>PS</strong> : surface air pressure</li>
              <li><strong>PRECTOTCORR</strong> : corrected precipitation totals</li>
            </ul>

            <p class="text-gray-400 mt-4 italic">
              A 10-year average smooths anomalies, giving a cleaner climate baseline for both
              historical and predictive analysis.
            </p>
          </div>

          <div
            class="bg-gray-900/60 p-6 rounded-xl border border-gray-800 hover:bg-gray-900/80 transition"
          >
            <h2 class="text-2xl font-bold text-white mb-3">Data Storage & Privacy</h2>
            <p class="text-gray-300 leading-relaxed">
              No personal data is permanently stored. Every request is processed live using NASA’s
              open data APIs. Cached results are temporary and only used to speed up future
              requests.
            </p>
            <p class="text-gray-400 mt-3">
              If you’re logged in, your favorite locations are stored in your profile for easy
              access. Reports can be downloaded as <strong>PDF</strong> summaries.
            </p>
          </div>

          <div
            class="bg-gray-900/60 p-6 rounded-xl border border-gray-800 hover:bg-gray-900/80 transition"
          >
            <h2 class="text-2xl font-bold text-white mb-3">Tech Stack</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
              <div
                v-for="tech in techs"
                :key="tech.name"
                class="bg-gray-800/40 border border-gray-700 rounded-lg p-3 text-center hover:bg-gray-800/70 transition"
              >
                <p class="font-semibold text-gray-100">{{ tech.name }}</p>
                <p class="text-xs text-gray-500">{{ tech.desc }}</p>
              </div>
            </div>
          </div>

          <div class="backdrop-blur-sm border-t border-gray-800 pt-10">
            <h2 class="text-3xl font-bold text-white mb-8 text-center">
              Frequently Asked Questions
            </h2>

            <div
              v-for="(item, index) in faq"
              :key="index"
              class="mb-6 border-b border-gray-800 pb-4"
            >
              <button
                @click="toggle(index)"
                class="w-full flex justify-between items-center text-left text-gray-100 hover:text-white transition"
              >
                <span class="text-lg font-semibold">{{ item.q }}</span>
                <svg
                  :class="{ 'rotate-180': openIndex === index }"
                  class="w-5 h-5 text-gray-400 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
              <transition name="fade">
                <p
                  v-if="openIndex === index"
                  class="text-gray-400 mt-3 text-sm leading-relaxed"
                >
                  {{ item.a }}
                </p>
              </transition>
            </div>
          </div>
        </section>

        <footer class="pt-10 mt-6 border-t border-gray-800 text-center text-gray-500 text-sm">
          <p>© 2025 WeatherMellon</p>
          <p class="text-gray-600 mt-1">
            Space Apps Challenge |
            <a
              href="https://github.com/Fabio345i/spaceappschallenge"
              target="_blank"
              class="text-gray-500 hover:underline"
              >GitHub Open Source</a
            >
          </p>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const props = defineProps({ visible: Boolean })
const emit = defineEmits(['close'])

function close() {
  emit('close')
}

// Échap pour fermer
function onKeydown(e) {
  if (e.key === 'Escape') close()
}

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))

const openIndex = ref(null)
const toggle = (i) => (openIndex.value = openIndex.value === i ? null : i)

const techs = [
  { name: 'FastAPI', desc: 'Python backend for NASA data aggregation' },
  { name: 'Vue 3 + Vite', desc: 'Reactive and fast frontend' },
  { name: 'CesiumJS', desc: '3D Earth visualization' },
  { name: 'NASA POWER', desc: 'Main climate database' },
  { name: 'Open-Meteo', desc: 'Forecast refinement' },
  { name: 'jsPDF', desc: 'Local PDF weather reports' }
]

const faq = [
  {
    q: 'How do you calculate the data?',
    a: 'We process raw NASA POWER parameters using Python models. Temperature, wind, humidity are normalized over 20+ years to show trends instead of single readings.'
  },
  {
    q: 'Can I save or download my reports?',
    a: 'Yes — you can export reports as PDF and keep favorite locations in your account.'
  },
  {
    q: 'How often are the datasets updated?',
    a: 'NASA POWER updates daily, with ~24h delay from satellite observation to public data.'
  },
  {
    q: 'What happens when I change the date?',
    a: 'Past dates show historical means, future dates use statistical prediction models.'
  },
  {
    q: 'Are predictions reliable?',
    a: 'They’re not perfect but use rolling historical windows and variance analysis to estimate likely conditions.'
  }
]
</script>

<style scoped>
.fade-zoom-enter-active,
.fade-zoom-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-zoom-enter-from,
.fade-zoom-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Scrollbar custom */
.custom-scroll::-webkit-scrollbar {
  width: 8px;
}
.custom-scroll::-webkit-scrollbar-thumb {
  background-color: rgba(100, 100, 100, 0.5);
  border-radius: 4px;
}
.custom-scroll::-webkit-scrollbar-thumb:hover {
  background-color: rgba(150, 150, 150, 0.7);
}
.custom-scroll::-webkit-scrollbar-track {
  background: transparent;
}
</style>
