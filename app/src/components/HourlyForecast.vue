<template>
  <div class="hourly-forecast-container bg-gray-900/95 backdrop-blur-sm border border-gray-800 rounded-lg p-4">
    
    <h2 class="text-xl font-semibold text-white mb-4 border-b border-gray-700 pb-2">
      Prévisions Horaires pour le {{ formattedDate }}
    </h2>
    
    <div v-if="hourlyData.length" class="flex overflow-x-auto space-x-4 pb-2">
      
      <div 
        v-for="hour in hourlyData" 
        :key="hour.time"
        class="flex-shrink-0 w-24 p-3 rounded-lg text-center transition-colors 
               bg-gray-800 hover:bg-gray-700 border border-gray-700"
      >
        <p class="text-sm font-bold text-blue-400 mb-1">{{ hour.time }}</p>
        
        <span class="text-3xl mb-1 block">{{ hour.icon }}</span>
        
        <p class="text-lg font-extrabold text-white">{{ hour.temp }}°C</p>
        
        <p class="text-xs text-gray-400 mt-1 truncate">{{ hour.condition }}</p>

        <p v-if="hour.rainChance > 0" class="text-xs text-green-400 mt-1">
          💧 {{ hour.rainChance }}%
        </p>
      </div>
      
    </div>
    
    <div v-else class="text-center py-8 text-gray-500">
      Chargement des données ou aucune donnée disponible pour cette date.
    </div>

  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  selectedDate: {
    type: Date,
    required: true
  },
  /** ici on call fast-api */
  location: {
    type: String,
    default: 'Paris, France'
  }
});

const hourlyData = ref([]);

const formattedDate = computed(() => {
  return props.selectedDate.toLocaleDateString('fr-FR', {
    weekday: 'long', 
    day: 'numeric', 
    month: 'long'
  });
});

//simulation d'appel API (Axios.get)
const fetchHourlyForecast = async (date, location) => {
  // --- SIMULATION D'APPEL API ICI ---
  
  
  console.log(`Fetching weather for ${location} on ${date.toDateString()}...`);
  
  
  const data = [];
  const startHour = 8;
  //generated icons and temps
  const conditions = [
    { icon: '☀️', tempRange: [18, 25], cond: 'Ensoleillé' },
    { icon: '🌤️', tempRange: [15, 22], cond: 'Peu nuageux' },
    { icon: '🌧️', tempRange: [10, 16], cond: 'Pluie faible' },
    { icon: '☁️', tempRange: [12, 18], cond: 'Nuageux' }
  ];
  
  for (let i = 0; i < 16; i++) { 
    const currentCondition = conditions[Math.floor(Math.random() * conditions.length)];
    const temp = Math.floor(
      Math.random() * (currentCondition.tempRange[1] - currentCondition.tempRange[0] + 1)
    ) + currentCondition.tempRange[0];
    
    data.push({
      time: `${(startHour + i) % 24}:00`,
      temp: temp,
      condition: currentCondition.cond,
      icon: currentCondition.icon,
      rainChance: currentCondition.icon === '🌧️' ? Math.floor(Math.random() * 50) + 50 : 0
    });
  }
  
  await new Promise(resolve => setTimeout(resolve, 500)); 
  
  hourlyData.value = data;
};

fetchHourlyForecast(props.selectedDate, props.location);

// 2. Surveille les changements de la date sélectionnée avec calendar + loadind date
watch(() => props.selectedDate, (newDate) => {
  hourlyData.value = []; 
  fetchHourlyForecast(newDate, props.location);
}, { immediate: false }); 

</script>

<style scoped>
.overflow-x-auto::-webkit-scrollbar {
  display: none;
}
.overflow-x-auto {
  -ms-overflow-style: none; 
  scrollbar-width: none; 
}
</style>