<script setup>
import { onMounted, ref } from 'vue'
import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'

const driverObj = ref(null)

const tutorialSteps = [
  {
    popover: {
      title: 'Welcome to NASA Weather',
      description: 'Your advanced weather prediction system. Let\'s explore together by making your first prediction.',
    }
  },
  {
    element: '.search-bar input',
    popover: {
      title: 'Search for Berlin',
      description: 'Please type exactly: Berlin, Germany',
      side: 'bottom',
      align: 'start',
      showButtons: false
    }
  }
]

function startTutorial() {
  if (driverObj.value) {
    driverObj.value.destroy()
  }

  const searchInput = document.querySelector('.search-bar input')
  
  // Bloquer Enter DIRECTEMENT sur l'input
  const blockEnter = (e) => {
    if (e.key === 'Enter') {
      const value = searchInput.value.toLowerCase()
      if (!(value.includes('berlin') && value.includes('germany'))) {
        e.preventDefault()
        e.stopPropagation()
        e.stopImmediatePropagation()
        return false
      }
    }
  }
  
  // Bloquer TOUS les événements Enter sur le document
  const globalBlocker = (e) => {
    if (e.key === 'Enter' && document.activeElement === searchInput) {
      const value = searchInput.value.toLowerCase()
      if (!(value.includes('berlin') && value.includes('germany'))) {
        e.preventDefault()
        e.stopPropagation()
        e.stopImmediatePropagation()
        return false
      }
    }
  }
  
  if (searchInput) {
    searchInput.addEventListener('keydown', blockEnter, true)
    searchInput.addEventListener('keypress', blockEnter, true)
    searchInput.addEventListener('keyup', blockEnter, true)
  }
  
  document.addEventListener('keydown', globalBlocker, true)
  document.addEventListener('keypress', globalBlocker, true)

  driverObj.value = driver({
    showProgress: true,
    steps: tutorialSteps,
    nextBtnText: 'Next',
    prevBtnText: 'Back',
    doneBtnText: 'Done',
    allowClose: false,
    onDestroyStarted: () => {
      // Nettoyer TOUS les listeners
      if (searchInput) {
        searchInput.removeEventListener('keydown', blockEnter, true)
        searchInput.removeEventListener('keypress', blockEnter, true)
        searchInput.removeEventListener('keyup', blockEnter, true)
      }
      document.removeEventListener('keydown', globalBlocker, true)
      document.removeEventListener('keypress', globalBlocker, true)
      
      localStorage.setItem('nasa-weather-tutorial-seen', 'true')
      if (driverObj.value) {
        driverObj.value.destroy()
      }
    },
    onNextClick: (element, step, options) => {
      const currentStepIndex = options.state.activeIndex
      
      if (currentStepIndex === 1) {
        const value = searchInput?.value.toLowerCase() || ''
        if (value.includes('berlin') && value.includes('germany')) {
          driverObj.value.destroy()
        }
        return
      }
      
      driverObj.value.moveNext()
    }
  })
  
  driverObj.value.drive()
  
  // Observer pour fermer automatiquement
  if (searchInput) {
    const inputHandler = (e) => {
      const value = e.target.value.toLowerCase()
      if (value.includes('berlin') && value.includes('germany')) {
        setTimeout(() => {
          if (driverObj.value) {
            driverObj.value.destroy()
          }
        }, 500)
      }
    }
    
    searchInput.addEventListener('input', inputHandler)
  }
}

onMounted(() => {
  const seen = localStorage.getItem('nasa-weather-tutorial-seen')
  if (!seen) {
    setTimeout(() => {
      startTutorial()
    }, 2000)
  }
})

defineExpose({
  startTutorial
})
</script>

<template>
  <div></div>
</template>

<style>
.driver-popover {
  background: #1f2937 !important;
  color: #f3f4f6 !important;
  border: 1px solid #4b5563 !important;
  border-radius: 8px !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8) !important;
  padding: 0 !important;
  min-width: 320px !important;
  z-index: 10001 !important;
}

.driver-popover-title {
  color: #ffffff !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  padding: 20px 20px 8px 20px !important;
  margin: 0 !important;
  display: block !important;
  line-height: 1.4 !important;
}

.driver-popover-description {
  color: #9ca3af !important;
  font-size: 14px !important;
  line-height: 1.6 !important;
  padding: 0 20px 80px 20px !important;
  margin: 0 !important;
  display: block !important;
}

.driver-popover-footer {
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  border-top: 1px solid #1f2937 !important;
  padding: 12px 20px !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  background-color: #0a0a0a !important;
  border-radius: 0 0 8px 8px !important;
}

.driver-popover-progress-text {
  color: #6b7280 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}

.driver-popover-next-btn,
.driver-popover-prev-btn {
  background: #1f2937 !important;
  color: #f3f4f6 !important;
  border: 1px solid #374151 !important;
  padding: 8px 16px !important;
  border-radius: 6px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  transition: all 0.2s !important;
  box-shadow: none !important;
  cursor: pointer !important;
}

.driver-popover-next-btn:hover,
.driver-popover-prev-btn:hover {
  background: #374151 !important;
  border-color: #4b5563 !important;
}

.driver-popover-close-btn {
  display: none !important;
}

.driver-active-element {
  border-radius: 8px !important;
  box-shadow: 0 0 0 5px rgba(59, 130, 246, 0.8), 0 0 20px rgba(59, 130, 246, 0.4) !important;
  position: relative !important;
  z-index: 10000 !important;
}

.driver-overlay {
  background: rgba(0, 0, 0, 0.3) !important;
}
</style>