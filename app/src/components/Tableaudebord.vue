<template>
  <div
    class="w-full bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-lg transition-all duration-300 hover:shadow-sky-500/20"
  >
    <!-- HEADER -->
    <header class="text-center mb-6 animate-fade-in">
      <h1
        class="text-3xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-sky-400 via-indigo-400 to-violet-500 drop-shadow-lg"
      >
        🌌 Données Météo
      </h1>
      <p class="text-gray-400 text-sm mt-2">
        Analyse atmosphérique intelligente — Données satellites
        <span class="text-sky-400 font-medium">NASA</span>
      </p>
    </header>

    <!-- TABLEAU DE DONNÉES -->
    <transition name="fade">
      <div v-if="dataLoaded" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <!-- Affichage du lieu sélectionné -->
        <div class="sm:col-span-2 text-center mb-4">
          <h2 class="text-xl font-semibold text-sky-400">
            Lieu sélectionné : {{ props.location?.geojson?.properties?.display_name || 'Coordonnées reçues' }}
          </h2>
          <p class="text-gray-500 text-xs">
            Coordonnées : {{ props.location?.lat.toFixed(4) }} / {{ props.location?.lon.toFixed(4) }}
          </p>
        </div>

        <div
          v-for="(item, i) in weatherData"
          :key="i"
          class="bg-white/10 border border-white/20 rounded-xl p-4 flex flex-col items-center justify-center text-center shadow-inner hover:bg-white/15 transition-all"
        >
          <div class="text-3xl mb-1" v-html="item.icon"></div>
          <h3 class="text-gray-300 text-sm uppercase tracking-wider">
            {{ item.name }}
          </h3>
          <p
            class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-sky-400 to-indigo-400"
          >
            {{ item.value }}
          </p>
          <p class="text-gray-400 text-xs">{{ item.unit }}</p>
        </div>
      </div>

      <!-- MESSAGE PAR DÉFAUT -->
      <div
        v-else
        class="text-center py-8 text-gray-400 italic flex flex-col items-center gap-2"
      >
        <div class="text-4xl animate-bounce">🌍</div>
        <p>Veuillez utiliser la barre de recherche pour sélectionner un lieu.</p>
      </div>
    </transition>

    <!-- FOOTER -->
    <footer class="mt-6 text-gray-500 text-xs text-center border-t border-white/10 pt-3">
      Données fournies par
      <span class="text-sky-400 font-medium">NASA GES DISC</span> et
      <span class="text-indigo-400 font-medium">Open-Meteo API</span>.
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"; // <-- AJOUTEZ 'watch' ici

// Définition de la propriété 'location'
const props = defineProps({
  location: {
    type: Object,
    default: null,
  },
});

// --- État des données ---
const temperature = ref("--");
const precipitation = ref("--");
const windSpeed = ref("--");
const airQuality = ref("--");
const dataLoaded = ref(false);

const weatherData = computed(() => [
  { name: "Température", value: `${temperature.value} °C`, unit: "°C", icon: "🌡️" },
  { name: "Précipitations", value: `${precipitation.value} mm`, unit: "mm", icon: "🌧️" },
  { name: "Vent", value: `${windSpeed.value} m/s`, unit: "m/s", icon: "🌬️" },
  { name: "Qualité de l’air", value: airQuality.value, unit: "AQI", icon: "🌫️" },
]);

// --- AJOUT CLÉ : Surveiller la prop 'location' et appeler fetchWeather ---
watch(
  () => props.location,
  (newLocation) => {
    if (newLocation && newLocation.lat && newLocation.lon) {
      console.log("Localisation reçue. Démarrage de fetchWeather:", newLocation);
      fetchWeather(); // L'appel de fetchWeather se fait ici.
    } else {
      dataLoaded.value = false;
    }
  },
  { deep: true }
);

// --- Logique de chargement des données ---
function fetchWeather() {
  // L'objet 'location' est accessible via 'props.location'
  if (!props.location) return; 

  // RETIRER LE DOUBLE defineProps INUTILE ET ERRONÉ:
  /*
  const props = defineProps({
    location: {
      type: Object,
      default: null
    }
  })
  */
  
  // Utilisez props.location.lat et props.location.lon pour votre appel API réel ici

  // Logique actuelle (données aléatoires)
  temperature.value = (Math.random() * 30).toFixed(1);
  precipitation.value = (Math.random() * 10).toFixed(1);
  windSpeed.value = (Math.random() * 15).toFixed(1);
  airQuality.value = ["Bonne", "Moyenne", "Mauvaise"][Math.floor(Math.random() * 3)];

  dataLoaded.value = true;
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.animate-fade-in {
  animation: fadeIn 1.2s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
