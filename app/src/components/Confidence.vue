<script setup>
import { computed } from 'vue'

const props = defineProps({
  isFuturePrediction: { type: Boolean, required: true },
  confiance: { type: Number, required: true }
})

const couleurConfiance = computed(() => {
  if (props.confiance > 75) return '#22c55e'
  if (props.confiance > 50) return '#facc15'
  return '#ef4444'
})
</script>

<template>
  <div class="absolute inset-0 opacity-10 pointer-events-none"></div>

  <p class="text-xs font-semibold tracking-wide uppercase mb-1 text-gray-300">
    {{ props.isFuturePrediction ? 'Confiance de la prédiction' : 'Données confirmées' }}
  </p>

  <div class="text-2xl mb-3" :class="props.isFuturePrediction ? '' : 'text-green-400'">
    {{ props.isFuturePrediction ? props.confiance + '%' : '100%' }}
  </div>

  <div class="w-full bg-[#101828] rounded-full h-4 ">
    <div
      :style="{
        width: props.confiance + '%',
        background: couleurConfiance
      }"
      class="h-4 rounded-full transition-all duration-700 shadow-[0_0_10px_var(--tw-shadow-color)]"
    ></div>
  </div>

  <p class="mt-2 text-xs text-gray-400">
    {{ props.isFuturePrediction
      ? 'Plus la date est éloignée, moins la précision est garantie'
      : 'Ces données proviennent de l’historique réel' }}
  </p>
</template>
