<script setup>
import { onMounted, ref } from 'vue'
import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'

const driverObj = ref(null)
const phase = ref('search')
let predictionLaunched = false

function setPhase(p) {
  phase.value = p
  document.body.classList.toggle('tutorial-calendar', p === 'calendar')
  document.body.classList.toggle('tutorial-running', p === 'search' || p === 'calendar')
}

function runPrediction() {
  if (predictionLaunched) return
  predictionLaunched = true

  const form = document.querySelector('.search-bar form')
  if (form) {
    try {
      form.requestSubmit ? form.requestSubmit() : form.submit()
      return
    } catch {}
  }

  const searchBtn =
    document.querySelector('.search-bar [type="submit"]') ||
    document.querySelector('.search-bar [data-action="search"]') ||
    document.querySelector('.search-bar button.search') ||
    document.querySelector('.search-bar button[aria-label*="search" i]')

  if (searchBtn) {
    searchBtn.click()
    return
  }

  const input = document.querySelector('.search-bar input')
  if (input) {
    const down = new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true })
    const press = new KeyboardEvent('keypress', { key: 'Enter', bubbles: true, cancelable: true })
    const up = new KeyboardEvent('keyup', { key: 'Enter', bubbles: true, cancelable: true })
    input.dispatchEvent(down)
    input.dispatchEvent(press)
    input.dispatchEvent(up)
  }
}

const tutorialSteps = [
  {
    popover: {
      title: 'Welcome to NASA Weather',
      description: 'Your advanced weather prediction system. Let\'s make your first prediction together.',
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
  },
  {
    element: 'input[type="text"][readonly]',
    popover: {
      title: 'Future Date Selected',
      description: 'We automatically selected a future date for prediction. This demonstrates our forecasting capabilities!',
      side: 'right',
      align: 'start'
    }
  },
  {
    popover: {
      title: 'Ready to Launch',
      description: 'Perfect. We will now launch the prediction for Berlin on a future date. Click "Done" to proceed.',
    }
  }
]

function startTutorial() {
  if (driverObj.value) driverObj.value.destroy()
  predictionLaunched = false

  const searchInput = document.querySelector('.search-bar input')
  setPhase('search')

  const blockEnter = (e) => {
    if (e.key === 'Enter') {
      const value = (searchInput?.value || '').toLowerCase()
      if (!(value.includes('berlin') && value.includes('germany'))) {
        e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation()
        return false
      }
    }
  }

  const globalBlocker = (e) => {
    if (e.key === 'Enter' && document.activeElement === searchInput) {
      const value = (searchInput?.value || '').toLowerCase()
      if (!(value.includes('berlin') && value.includes('germany'))) {
        e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation()
        return false
      }
    }
  }

  const stopSuggestPropagation = (e) => {
    const v = (searchInput?.value || '').toLowerCase()
    const isTarget = v.includes('berlin') && v.includes('germany')
    if (!isTarget) e.stopImmediatePropagation()
  }

  if (searchInput) {
    searchInput.setAttribute('autocomplete', 'off')
    searchInput.setAttribute('autocapitalize', 'off')
    searchInput.setAttribute('autocorrect', 'off')
    searchInput.setAttribute('spellcheck', 'false')

    searchInput.addEventListener('keydown', blockEnter, true)
    searchInput.addEventListener('keypress', blockEnter, true)
    searchInput.addEventListener('keyup', blockEnter, true)
    searchInput.addEventListener('input', stopSuggestPropagation, true)
    searchInput.addEventListener('keyup', stopSuggestPropagation, true)
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
      runPrediction()

      if (searchInput) {
        searchInput.removeEventListener('keydown', blockEnter, true)
        searchInput.removeEventListener('keypress', blockEnter, true)
        searchInput.removeEventListener('keyup', blockEnter, true)
        searchInput.removeEventListener('input', stopSuggestPropagation, true)
        searchInput.removeEventListener('keyup', stopSuggestPropagation, true)
      }
      document.removeEventListener('keydown', globalBlocker, true)
      document.removeEventListener('keypress', globalBlocker, true)
      setPhase('done')

      localStorage.setItem('nasa-weather-tutorial-seen', 'true')
      if (driverObj.value) driverObj.value.destroy()

      setTimeout(() => {
        const finalDriver = driver({
          showProgress: false,
          steps: [
            {
              popover: {
                title: 'Prediction Complete!',
                description: 'Your weather forecast has been generated. Explore the results and discover our advanced prediction capabilities.',
              }
            },
            {
              element: '.px-4.py-2',
              popover: {
                title: 'Prediction Complete!',
                description: 'Here you can see the hourly precipitation predictions for Berlin.',
                side: 'bottom',
                align: 'start'
              }
            },
            {
              element: '.bg-gray-900.border.border-gray-800.rounded-lg.p-4',
              popover: {
                title: 'Hourly Forecast',
                description: 'Detailed hourly precipitation data to help you plan your day effectively.',
                side: 'left',
                align: 'start'
              }
            },
            {
              element: '.relative.flex.items-center.gap-2.px-5.py-2\\.5',
              popover: {
                title: 'Download Report',
                description: 'Generate and download a comprehensive PDF report with all weather predictions and recommendations.',
                side: 'top',
                align: 'start'
              }
            },
            {
              popover: {
                title: 'There you go!',
                description: 'You are all set to explore WeatherMellon. Feel free to restart this tutorial anytime from the tutorial navbar menu.',
              }
            }
          ],
          doneBtnText: 'Got it',
          allowClose: true,
          onDestroyStarted: () => {
            if (finalDriver) finalDriver.destroy()
          }
        })
        finalDriver.drive()
      }, 3000)
    },

    onNextClick: (element, step, options) => {
      const currentStepIndex = options.state.activeIndex

      if (currentStepIndex === 1) {
        const value = (searchInput?.value || '').toLowerCase()
        if (value.includes('berlin') && value.includes('germany')) {
          setPhase('calendar')
          driverObj.value.moveNext()
        }
        return
      }

      driverObj.value.moveNext()
    }
  })

  driverObj.value.drive()

  if (searchInput) {
    const inputHandler = (e) => {
      const value = e.target.value.toLowerCase()
      if (value.includes('berlin') && value.includes('germany')) {
        setTimeout(() => {
          if (!driverObj.value) return
          setPhase('calendar')

          const monthsToAdvance = 12 * 12 // 12 ans
          const dateInput = document.querySelector('input[type="text"][readonly]')
          if (dateInput) {
            dateInput.click()
            setTimeout(() => {
              const nextButtons = document.querySelectorAll('button')
              const nextButton = Array.from(nextButtons).find(btn => {
                const svg = btn.querySelector('svg path[d*="M9 5l7 7-7 7"]')
                return svg !== null
              })
              if (nextButton) {
                for (let i = 0; i < monthsToAdvance; i++) nextButton.click()
                setTimeout(() => {
                  const dayButtons = document.querySelectorAll('button.aspect-square')
                  const day15 = Array.from(dayButtons).find(btn =>
                    btn.textContent.trim() === '15' &&
                    !btn.classList.contains('text-gray-500')
                  )
                  if (day15) {
                    day15.click()
                    setTimeout(() => {
                      driverObj.value.moveNext()
                    }, 200)
                  }
                }, 200)
              }
            }, 300)
          }
        }, 500)
      }
    }
    searchInput.addEventListener('input', inputHandler)
  }
}

onMounted(() => {
  const seen = localStorage.getItem('nasa-weather-tutorial-seen')
  if (!seen) setTimeout(startTutorial, 2000)
})

defineExpose({ startTutorial })
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
.driver-popover-progress-text { color: #6b7280 !important; font-size: 13px !important; font-weight: 500 !important; }
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
.driver-popover-prev-btn:hover { background: #374151 !important; border-color: #4b5563 !important; }
.driver-popover-close-btn { display: none !important; }
.driver-active-element {
  border-radius: 8px !important;
  box-shadow: 0 0 0 5px rgba(59, 130, 246, 0.8), 0 0 20px rgba(59, 130, 246, 0.4) !important;
  position: relative !important;
  z-index: 10000 !important;
}
.driver-overlay { background: rgba(0, 0, 0, 0.3) !important; }

.tutorial-running .search-bar [role="listbox"],
.tutorial-running .search-bar .suggestions,
.tutorial-running .search-bar .autocomplete-panel,
.tutorial-running .search-bar .autocomplete,
.tutorial-running .pac-container, /* Google Places */
.tutorial-running .mapboxgl-ctrl-geocoder--suggestions, /* Mapbox */
.tutorial-running .osmgeocoder-suggestions {
  display: none !important;
  visibility: hidden !important;
  pointer-events: none !important;
}
</style>