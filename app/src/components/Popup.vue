<template>
  <transition name="fade-slide">
    <div
      v-if="visible"
      class="absolute top-4 right-4 z-50 w-80 rounded-2xl shadow-2xl border backdrop-blur-xl overflow-hidden max-h-[calc(100%-2rem)] overflow-y-auto"
      :style="{
        background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(31, 41, 55, 0.95) 100%)',
        borderColor: 'rgba(99, 102, 241, 0.3)',
        color: '#F3F4F6',
        boxShadow: '0 25px 50px -12px rgba(99, 102, 241, 0.25), 0 0 0 1px rgba(99, 102, 241, 0.1)'
      }"
    >
      <div class="absolute inset-0 bg-gradient-to-br from-indigo-500/10 via-transparent to-purple-500/10 pointer-events-none"></div>
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-400/50 to-transparent"></div>
      
      <div class="relative flex justify-between items-start p-4 border-b border-gray-700/50">
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></div>
          <h3 class="font-bold text-base bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
            {{ title }}
          </h3>
        </div>
        <button
          class="relative group text-gray-400 hover:text-white transition-all duration-300"
          @click="$emit('close')"
        >
          <div class="absolute inset-0 bg-indigo-500/20 rounded-full scale-0 group-hover:scale-100 transition-transform duration-300"></div>
          <span class="relative block w-6 h-6 flex items-center justify-center">✕</span>
        </button>
      </div>

      <div class="relative p-4 border-b border-gray-700/50">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-xs">⛰️</div>
          <div>
            <h4 class="font-semibold text-sm text-white">Climat au Sommet</h4>
            <p class="text-xs text-gray-400">{{ displayData.altitude_sommet }}m d'altitude</p>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div class="bg-gray-800/50 rounded-lg p-2">
            <p class="text-xs text-gray-400 mb-1">Température</p>
            <p class="text-base font-bold text-blue-400">{{ displayData.temperature_sommet }}°C</p>
          </div>
          <div class="bg-gray-800/50 rounded-lg p-2">
            <p class="text-xs text-gray-400 mb-1">Vent</p>
            <p class="text-base font-bold text-cyan-400">{{ displayData.vent_sommet }} km/h</p>
          </div>
          <div class="bg-gray-800/50 rounded-lg p-2 col-span-2">
            <p class="text-xs text-gray-400 mb-1">Précipitations</p>
            <p class="text-base font-bold text-indigo-400">{{ displayData.precipitation_sommet }} mm</p>
          </div>
        </div>
      </div>

      <div class="relative p-4">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-xs">🏔️</div>
          <div>
            <h4 class="font-semibold text-sm text-white">Climat à la Base</h4>
            <p class="text-xs text-gray-400">{{ displayData.altitude_base }}m d'altitude</p>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2">
          <div class="bg-gray-800/50 rounded-lg p-2">
            <p class="text-xs text-gray-400 mb-1">Température</p>
            <p class="text-base font-bold text-orange-400">{{ displayData.temperature_base }}°C</p>
          </div>
          <div class="bg-gray-800/50 rounded-lg p-2">
            <p class="text-xs text-gray-400 mb-1">Humidité</p>
            <p class="text-base font-bold text-teal-400">{{ displayData.humiditer_base }}%</p>
          </div>
          <div class="bg-gray-800/50 rounded-lg p-2">
            <p class="text-xs text-gray-400 mb-1">Vent</p>
            <p class="text-base font-bold text-cyan-400">{{ displayData.vent_base }} km/h</p>
          </div>
          <div class="bg-gray-800/50 rounded-lg p-2">
            <p class="text-xs text-gray-400 mb-1">Précipitations</p>
            <p class="text-base font-bold text-indigo-400">{{ displayData.precipitation_base }} mm</p>
          </div>
        </div>
      </div>

      <!-- Recommandation / Commentaire -->
      <div class="relative p-4 border-t border-gray-700/50 bg-gradient-to-br from-gray-800/30 to-gray-900/30">
        <div class="flex items-start gap-2">
          <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center text-xs flex-shrink-0">💡</div>
          <div>
            <h4 class="font-semibold text-sm text-white mb-1">Recommandation</h4>
            <p class="text-xs text-gray-300 leading-relaxed">
              {{ displayRecommandation }}
            </p>
          </div>
        </div>
      </div>
      
      <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 opacity-50"></div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  visible: Boolean,
  title: String,
  description: String,
  climatData: {
    type: Object,
    default: null
  },
  recommandation: {
    type: String,
    default: null
  }
});

defineEmits(["close"]);

// Données de test temporaires (en attendant le backend)
const fakeClimatData = {
  altitude_base: 265,
  altitude_sommet: 875,
  temperature_base: 15,
  humiditer_base: 65,
  vent_base: 12,
  precipitation_base: 0,
  temperature_sommet: 8,
  vent_sommet: 28,
  precipitation_sommet: 2
};

// Recommandation de test (en attendant le backend)
const fakeRecommandation = "✅ Conditions favorables pour l'ascension. Les températures sont douces et le vent modéré. Attention aux précipitations légères au sommet. Équipement recommandé : veste imperméable et bonnet.";

// Utiliser les données de test si aucune donnée réelle n'est fournie
const displayData = computed(() => props.climatData || fakeClimatData);
const displayRecommandation = computed(() => props.recommandation || fakeRecommandation);
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>