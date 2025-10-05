<script setup>
import { onMounted, ref } from 'vue'
import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'
import TutorialCharacter from './TutorialCharacter.vue'

const characterStep = ref(0)
const showCharacter = ref(false)

const tutorialSteps = [
  {
    popover: {
      title: 'Welcome to NASA Weather!',
      description: 'Let me show you around. This application uses real NASA satellite data to track weather patterns worldwide.',
    }
  },
  {
    element: '.search-bar input',
    popover: {
      title: 'Search Location',
      description: 'Enter any city, region, or coordinates to view detailed weather data from NASA satellites.',
      side: 'bottom',
      align: 'start'
    }
  },
  {
    element: '.bg-gray-900.border.border-gray-800.rounded-md.p-3',
    popover: {
      title: 'Select Forecast Date',
      description: 'Choose a date to view historical weather data or future forecasts.',
      side: 'right',
      align: 'start'
    }
  },
  {
    element: 'aside > div > div:nth-child(3)',
    popover: {
      title: 'Weather Summary',
      description: 'View current conditions including temperature, precipitation, wind speed, and air quality.',
      side: 'right',
      align: 'center'
    }
  },
  {
    element: '.w-full.h-full.bg-gray-900.border.border-gray-800',
    popover: {
      title: 'Interactive 3D Globe',
      description: 'Explore Earth in real-time. The globe automatically zooms to your selected location.',
      side: 'left',
      align: 'center'
    }
  }
]

function startTutorial() {
  showCharacter.value = true
  characterStep.value = 0
  
  const driverObj = driver({
    showProgress: true,
    steps: tutorialSteps,
    nextBtnText: 'Next',
    prevBtnText: 'Previous',
    doneBtnText: 'Got it!',
    onNextClick: () => {
      characterStep.value++
      driverObj.moveNext()
    },
    onPrevClick: () => {
      characterStep.value--
      driverObj.movePrevious()
    },
    onDestroyStarted: () => {
      localStorage.setItem('nasa-weather-tutorial-seen', 'true')
      showCharacter.value = false
      driverObj.destroy()
    }
  })
  
  driverObj.drive()
}

onMounted(() => {
  const seen = localStorage.getItem('nasa-weather-tutorial-seen')
  if (!seen) {
    setTimeout(() => {
      startTutorial()
    }, 1500)
  }
})

defineExpose({
  startTutorial
})
</script>

<template>
  <div>
    <TutorialCharacter v-if="showCharacter" :step="characterStep" />
  </div>
</template>

<style>
.driver-popover {
  background: #1f2937 !important;
  color: #f3f4f6 !important;
  border: 1px solid #374151 !important;
  border-radius: 10px !important;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4) !important;
  padding: 0 !important;
  min-height: 150px !important;
}

.driver-popover-title {
  color: #ffffff !important;
  font-size: 0.875rem !important;
  font-weight: 600 !important;
  padding: 1rem 2.5rem 0.5rem 1rem !important;
  margin: 0 !important;
  display: block !important;
}

.driver-popover-description {
  color: #d1d5db !important;
  font-size: 0.75rem !important;
  line-height: 1.5 !important;
  padding: 0 1rem 4rem 1rem !important;
  margin: 0 !important;
  display: block !important;
}

.driver-popover-footer {
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  border-top: 1px solid #374151 !important;
  padding: 0.75rem 1rem !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  background-color: #111827 !important;
  border-radius: 0 0 10px 10px !important;
}

.driver-popover-progress-text {
  color: #9ca3af !important;
  font-size: 0.75rem !important;
}

.driver-popover-next-btn,
.driver-popover-prev-btn {
  background: #374151 !important;
  color: #f3f4f6 !important;
  border: none !important;
  padding: 0.5rem 1rem !important;
  border-radius: 0.375rem !important;
  font-size: 0.75rem !important;
  font-weight: 500 !important;
  transition: all 0.2s !important;
  box-shadow: none !important;
}

.driver-popover-next-btn:hover,
.driver-popover-prev-btn:hover {
  background: #4b5563 !important;
}

.driver-popover-close-btn {
  position: absolute !important;
  top: 1rem !important;
  right: 1rem !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  color: #9ca3af !important;
  font-size: 1.25rem !important;
  width: 20px !important;
  height: 20px !important;
  line-height: 1 !important;
}

.driver-popover-close-btn:hover {
  color: #ffffff !important;
  background: transparent !important;
}

.driver-active-element {
  border-radius: 0.5rem !important;
}
</style>