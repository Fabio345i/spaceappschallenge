<template>
  <transition name="fade-slide">
    <div
      v-if="visible"
      class="popup-container"
      :style="{ left: position.x + 'px', top: position.y + 'px' }"
      @mousedown.self="bringToFront"
    >
      <!-- Header -->
      <div class="popup-header" @mousedown="startDrag">
        <h3 class="text-base font-semibold text-white truncate">{{ title }}</h3>
        <button
          class="text-gray-400 hover:text-white transition"
          @click="$emit('close')"
        >✕</button>
      </div>

      <!-- Summit -->
      <section class="popup-section">
        <h4 class="section-title">Summit Climate</h4>
        <p class="section-subtitle">{{ displayData.altitude_sommet }} m elevation</p>
        <div class="grid grid-cols-2 gap-3">
          <InfoBlock label="Temperature" :value="displayData.temperature_sommet + '°C'" />
          <InfoBlock label="Wind" :value="displayData.vent_sommet + ' km/h'" />
          <InfoBlock label="Precipitation" :value="displayData.precipitation_sommet + ' mm'" />
        </div>
      </section>

      <!-- Base -->
      <section class="popup-section">
        <h4 class="section-title">Base Climate</h4>
        <p class="section-subtitle">{{ displayData.altitude_base }} m elevation</p>
        <div class="grid grid-cols-2 gap-3">
          <InfoBlock label="Temperature" :value="displayData.temperature_base + '°C'" />
          <InfoBlock label="Humidity" :value="displayData.humiditer_base + '%'" />
          <InfoBlock label="Wind" :value="displayData.vent_base + ' km/h'" />
          <InfoBlock label="Precipitation" :value="displayData.precipitation_base + ' mm'" />
        </div>
      </section>

      <!-- Recommendation -->
      <section class="popup-section border-t border-gray-700 mt-4 pt-3">
        <h4 class="section-title">Recommendation</h4>
        <p class="text-xs text-gray-300 leading-relaxed">
          {{ displayRecommandation }}
        </p>
      </section>
    </div>
  </transition>
</template>

<script setup>
import { computed, ref, onBeforeUnmount } from 'vue'
import InfoBlock from './InfoBlock.vue'

const props = defineProps({
  visible: Boolean,
  title: String,
  climatData: Object,
  recommandation: String
})

defineEmits(['close'])

const fakeClimatData = {
  altitude_base: 265,
  altitude_sommet: 875,
  temperature_base: 15,
  humiditer_base: 65,
  vent_base: 12,
  precipitation_base: 0,
  temperature_sommet: 8,
  vent_sommet: 8,
  precipitation_sommet: 2
}

const fakeRecommandation = 'Conditions look stable. Light wind, mild temps. Light precipitation at summit — dress accordingly.'

const displayData = computed(() => props.climatData || fakeClimatData)
const displayRecommandation = computed(() => props.recommandation || fakeRecommandation)

const position = ref({ x: 200, y: 100 })
let offset = { x: 0, y: 0 }
let isDragging = false

function startDrag(e) {
  isDragging = true
  offset.x = e.clientX - position.value.x
  offset.y = e.clientY - position.value.y
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

function onDrag(e) {
  if (!isDragging) return
  position.value = {
    x: e.clientX - offset.x,
    y: e.clientY - offset.y
  }
}

function stopDrag() {
  isDragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

function bringToFront() {
  // If you support multiple popups, set a higher z-index
}

onBeforeUnmount(() => stopDrag())
</script>

<style scoped>
.popup-container {
  position: absolute;
  width: 360px;
  background-color: #1f2937;
  border-radius: 10px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
  color: #f9fafb;
  z-index: 9999;
  user-select: none;
}

.popup-header {
  background-color: #111827;
  border-bottom: 1px solid #374151;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: move;
}

.popup-section {
  padding: 1rem;
}

.section-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #e5e7eb;
  margin-bottom: 0.25rem;
}

.section-subtitle {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 0.5rem;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
