<template>
  <transition name="fade">
    <div
      v-if="visible"
      class="popover-overlay"
      @click.self="close"
    >
      <div class="popover-container">
        <!-- Bouton fermeture -->
        <button
          @click="close"
          class="close-btn"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <!-- Header -->
        <div class="header">
          <div class="icon-wrapper">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1>About WeatherMellon</h1>
          <p class="subtitle">Earth Observation System - NASA Weather Intelligence</p>
        </div>

        <!-- Contenu -->
        <section class="content-section">
          <p class="intro-text">
            Built for explorers, scientists, and the simply curious — this project transforms
            satellite data into visual, meaningful weather insights you can actually feel.
          </p>

          <div class="mt-6 flex justify-center">
            <a
              href="https://power.larc.nasa.gov/"
              target="_blank"
              class="link-button"
            >
              Learn more about NASA POWER API
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </a>
          </div>
        </section>

        <!-- Sections -->
        <section class="sections">
          <div class="section-card">
            <h2 class="section-title">The Story</h2>
            <p class="section-text">
              This project was born from the
              <span class="highlight">NASA Space Apps Challenge 2025</span>. The goal is to
              bridge the gap between raw satellite data and real human understanding. We wanted a
              tool that doesn't just <em>show numbers</em> but explains them, visualizes them, and
              helps people plan their day, wherever they are on Earth.
            </p>
          </div>

          <div class="section-card">
            <h2 class="section-title">How We Calculate Weather Insights</h2>
            <p class="section-text mb-4">
              All data originates from
              <span class="highlight">NASA POWER</span> — a global climate
              database capturing decades of observations from space. We analyze:
            </p>

            <ul class="data-list">
              <li><strong>T2M</strong> : average air temperature (2 m above ground)</li>
              <li><strong>RH2M</strong> : relative humidity</li>
              <li><strong>U2M & V2M</strong> : wind vector components (speed & direction)</li>
              <li><strong>PS</strong> : surface air pressure</li>
              <li><strong>PRECTOTCORR</strong> : corrected precipitation totals</li>
            </ul>

            <div class="note-box">
              <p class="note-text">
                <strong>Note:</strong> A 10-year average smooths anomalies, giving a cleaner climate baseline for both
                historical and predictive analysis.
              </p>
            </div>
          </div>

          <div
            class="section-card"
          >
            <h2 class="section-title">Data Storage & Privacy</h2>
            <p class="section-text">
              No personal data is permanently stored. Every request is processed live using NASA’s
              open data APIs. Cached results are temporary and only used to speed up future
              requests.
            </p>
            <p class="section-text mt-3">
              If you’re logged in, your favorite locations are stored in your profile for easy
              access. Reports can be downloaded as <strong>PDF</strong> summaries.
            </p>
          </div>

          <div class="section-card">
            <h2 class="section-title">Tech Stack</h2>
            <div class="tech-grid">
              <div
                v-for="tech in techs"
                :key="tech.name"
                class="tech-item"
              >
                <p class="tech-name">{{ tech.name }}</p>
                <p class="tech-desc">{{ tech.desc }}</p>
              </div>
            </div>
          </div>

          <div class="faq-section">
            <h2 class="faq-title">Frequently Asked Questions</h2>

            <div
              v-for="(item, index) in faq"
              :key="index"
              class="faq-item"
            >
              <button
                @click="toggle(index)"
                class="faq-button"
              >
                <span class="faq-question">{{ item.q }}</span>
                <svg
                  :class="{ 'rotate-180': openIndex === index }"
                  class="faq-arrow"
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
                  class="faq-answer"
                >
                  {{ item.a }}
                </p>
              </transition>
            </div>
          </div>
        </section>

        <footer class="footer">
          <p>© 2025 WeatherMellon</p>
          <p class="footer-link">
            Space Apps Challenge |
            <a
              href="https://github.com/Fabio345i/spaceappschallenge"
              target="_blank"
              class="footer-link-text"
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
.popover-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(4px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.popover-container {
  position: relative;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  background: #030712;
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 40px 32px 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
  overflow-y: auto;
}

.popover-container::-webkit-scrollbar {
  width: 8px;
}
.popover-container::-webkit-scrollbar-thumb {
  background-color: rgba(100, 100, 100, 0.5);
  border-radius: 4px;
}
.popover-container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(150, 150, 150, 0.7);
}
.popover-container::-webkit-scrollbar-track {
  background: transparent;
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: transparent;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #fff;
  background: #1f2937;
}

.header {
  text-align: center;
  margin-bottom: 32px;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 14px;
  margin-bottom: 16px;
}

.icon {
  width: 28px;
  height: 28px;
  stroke: #f3f4f6;
}

h1 {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 6px;
}

.subtitle {
  color: #6b7280;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.content-section {
  margin-bottom: 32px;
}

.intro-text {
  color: #9ca3af;
  font-size: 14px;
  line-height: 1.6;
  text-align: center;
}

.link-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #1f2937;
  color: #fff;
  border: 1px solid #374151;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.link-button:hover {
  background: #374151;
  border-color: #4b5563;
}

.sections {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-card {
  background: #000;
  border: 1px solid #1f2937;
  border-radius: 12px;
  padding: 24px;
  transition: border-color 0.2s;
}

.section-card:hover {
  border-color: #374151;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 12px;
}

.section-text {
  color: #d1d5db;
  font-size: 14px;
  line-height: 1.6;
}

.highlight {
  color: #9ca3af;
  font-weight: 600;
}

.data-list {
  list-style: none;
  padding: 0;
  margin: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.data-list li {
  color: #d1d5db;
  font-size: 14px;
  padding-left: 20px;
  position: relative;
}

.data-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #6b7280;
}

.data-list strong {
  color: #fff;
  font-weight: 600;
}

.note-box {
  margin-top: 16px;
  padding: 12px 16px;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 8px;
}

.note-text {
  color: #9ca3af;
  font-size: 13px;
  line-height: 1.5;
}

.note-text strong {
  color: #d1d5db;
  font-weight: 600;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.tech-item {
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: all 0.2s;
}

.tech-item:hover {
  border-color: #4b5563;
  background: #111827;
}

.tech-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.tech-desc {
  font-size: 12px;
  color: #9ca3af;
  line-height: 1.4;
}

.faq-section {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #1f2937;
}

.faq-title {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 24px;
  text-align: center;
}

.faq-item {
  margin-bottom: 16px;
  border-bottom: 1px solid #1f2937;
  padding-bottom: 16px;
}

.faq-button {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: left;
  background: none;
  border: none;
  color: #f3f4f6;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.faq-button:hover {
  color: #fff;
}

.faq-question {
  font-size: 16px;
  font-weight: 600;
  flex: 1;
}

.faq-arrow {
  width: 20px;
  height: 20px;
  color: #6b7280;
  transition: transform 0.2s;
  flex-shrink: 0;
  margin-left: 12px;
}

.faq-answer {
  color: #9ca3af;
  font-size: 14px;
  line-height: 1.6;
  margin-top: 12px;
  padding-left: 0;
}

.footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #1f2937;
  text-align: center;
}

.footer p {
  color: #6b7280;
  font-size: 13px;
  margin: 4px 0;
}

.footer-link {
  margin-top: 8px;
}

.footer-link-text {
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link-text:hover {
  color: #fff;
  text-decoration: underline;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active .popover-container {
  animation: slideUp 0.3s ease;
}

.fade-leave-active .popover-container {
  animation: slideDown 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideDown {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(20px);
    opacity: 0;
  }
}
</style>
