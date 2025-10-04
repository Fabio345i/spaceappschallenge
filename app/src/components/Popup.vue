<script setup>
import { onMounted, ref } from "vue"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

const map = ref(null)

onMounted(() => {
  map.value = L.map("map").setView([46.8, -71.2], 10)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
  }).addTo(map.value)

  const marker = L.marker([46.8, -71.2]).addTo(map.value)

  const popupContent = `
    <div class="p-4 bg-white rounded-xl shadow-xl w-60 text-gray-800">
      <h3 class="text-lg font-semibold mb-2">Québec</h3>
      <p class="text-sm text-gray-600 mb-2">
        Ville historique au bord du fleuve Saint-Laurent 🌊
      </p>
      <button class="px-3 py-1 text-sm rounded-lg bg-sky-500 text-white hover:bg-sky-600 transition">
        En savoir plus
      </button>
    </div>
  `

  marker.bindPopup(popupContent, {
    maxWidth: 250,
    className: "custom-leaflet-popup"
  })
})
</script>

<template>
  <div id="map" class="w-full h-[500px] rounded-xl overflow-hidden"></div>
</template>

<style>
/* Optionnel : pour virer le style par défaut de Leaflet */
.leaflet-popup-content-wrapper {
  border-radius: 1rem !important;
  padding: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}
.leaflet-popup-tip {
  background: white !important;
}
</style>
