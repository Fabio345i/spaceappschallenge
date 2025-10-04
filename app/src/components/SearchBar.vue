<script setup>
import { ref } from 'vue'
import debounce from 'lodash.debounce'

const query = ref('')
const suggestions = ref([])
const emit = defineEmits(['location-selected'])

const fetchSuggestions = debounce(async () => {
  if (!query.value) {
    suggestions.value = []
    return
  }
  const url = `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&polygon_geojson=1&q=${encodeURIComponent(query.value)}&limit=5`
  const res = await fetch(url, { headers: { 'User-Agent': 'cesium-app-hackathon' } })
  const data = await res.json()
  suggestions.value = data
}, 300)

function selectPlace(place) {
  const lat = parseFloat(place.lat)
  const lon = parseFloat(place.lon)
  const polygon = place.geojson
  const osmId = place.osm_id
  const osmType = place.osm_type
  const prefix =
    osmType?.toLowerCase().startsWith('r')
      ? 'R'
      : osmType?.toLowerCase().startsWith('w')
      ? 'W'
      : 'N'

  emit('location-selected', { lat, lon, geojson: polygon, osm_id: prefix + osmId })
  query.value = place.display_name
  suggestions.value = []
}
</script>

<template>
  <div class="search-bar">
    <input
      v-model="query"
      @input="fetchSuggestions"
      @keyup.enter="suggestions.length && selectPlace(suggestions[0])"
      placeholder="Entrez une ville ou montagne"
    />
    <ul v-if="suggestions.length" class="suggestions">
      <li
        v-for="place in suggestions"
        :key="place.place_id"
        @click="selectPlace(place)"
      >
        {{ place.display_name }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.search-bar {
  position: relative;
  top: 10px;
  left: 10px;
  z-index: 10;
  background: white;
  border-radius: 6px;
  width: 300px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}
input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 6px 6px 0 0;
  font-size: 14px;
}
.suggestions {
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-top: none;
}
.suggestions li {
  padding: 6px 8px;
  cursor: pointer;
  background: white;
  color: black;
}
.suggestions li:hover {
  background: #f0f0f0;
}
</style>