<template>
  <div class="px-4 py-3">
    <div class="flex items-center justify-between mb-2">
      <h2 class="text-sm font-medium text-white">
        Hourly Forecast - {{ formattedDate }}
      </h2>
    </div>
    
    <div v-if="hourlyData.length" class="flex overflow-x-auto space-x-2 pb-2">
      <div 
        v-for="hour in hourlyData" 
        :key="hour.time"
        class="flex-shrink-0 w-16 p-2 rounded bg-gray-900 border border-gray-800 text-center hover:border-gray-700"
      >
        <p class="text-xs text-gray-500 mb-1">{{ hour.time }}</p>
        <p class="text-base font-semibold text-white">{{ hour.temp }}°</p>
        <p class="text-xs text-gray-500 mt-1">{{ hour.condition }}</p>
        <p v-if="hour.rainChance > 0" class="text-xs text-blue-400 mt-1">{{ hour.rainChance }}%</p>
      </div>
    </div>
    
    <div v-else class="text-center py-4 text-gray-600 text-xs">
      Loading forecast data...
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  selectedDate: {
    type: Date,
    required: true
  },
  location: {
    type: String,
    default: 'Paris, France'
  }
})

const hourlyData = ref([])

const formattedDate = computed(() => {
  return props.selectedDate.toLocaleDateString('en-US', {
    weekday: 'short', 
    month: 'short',
    day: 'numeric'
  })
})

const fetchHourlyForecast = async (date, location) => {
  const data = []
  const startHour = 8
  const conditions = [
    { tempRange: [18, 25], cond: 'Clear' },
    { tempRange: [15, 22], cond: 'Cloudy' },
    { tempRange: [10, 16], cond: 'Rain' },
    { tempRange: [12, 18], cond: 'Overcast' }
  ]
  
  for (let i = 0; i < 16; i++) {
    const currentCondition = conditions[Math.floor(Math.random() * conditions.length)]
    const temp = Math.floor(Math.random() * (currentCondition.tempRange[1] - currentCondition.tempRange[0] + 1)) + currentCondition.tempRange[0]
    
    data.push({
      time: `${String((startHour + i) % 24).padStart(2, '0')}:00`,
      temp: temp,
      condition: currentCondition.cond,
      rainChance: currentCondition.cond === 'Rain' ? Math.floor(Math.random() * 50) + 50 : 0
    })
  }
  
  await new Promise(resolve => setTimeout(resolve, 300))
  hourlyData.value = data
}

fetchHourlyForecast(props.selectedDate, props.location)

watch(() => props.selectedDate, (newDate) => {
  hourlyData.value = []
  fetchHourlyForecast(newDate, props.location)
}, { immediate: false })
</script>

<style scoped>
.overflow-x-auto::-webkit-scrollbar {
  height: 4px;
}
.overflow-x-auto::-webkit-scrollbar-track {
  background: #1f2937;
}
.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 2px;
}
</style>