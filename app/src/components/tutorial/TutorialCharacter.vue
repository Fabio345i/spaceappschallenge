<script setup>
import { ref, onMounted, watch } from 'vue'
import lottie from 'lottie-web'
import animationData from '@/assets/animation/nasa-robot.json'

const props = defineProps({
  step: {
    type: Number,
    default: 0
  }
})

const animationContainer = ref(null)
let animationInstance = null

const positions = [
  { bottom: '50%', right: '50%', transform: 'translate(50%, 50%)' },
  { bottom: '380px', right: 'calc(100% - 420px)', transform: 'none' },
  { bottom: '280px', right: 'calc(100% - 420px)', transform: 'none' },
  { bottom: '180px', right: 'calc(100% - 420px)', transform: 'none' },
  { bottom: '50%', right: '40%', transform: 'translateY(50%)' }
]

onMounted(() => {
  if (animationContainer.value) {
    animationInstance = lottie.loadAnimation({
      container: animationContainer.value,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      animationData: animationData
    })
  }
})
</script>

<template>
  <div 
    ref="animationContainer" 
    class="fixed w-24 h-24 z-[100] pointer-events-none transition-all duration-700 ease-in-out"
    :style="positions[step] || positions[0]"
  ></div>
</template>