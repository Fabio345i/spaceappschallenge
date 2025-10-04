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
      placeholder="Search for a location..."
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
  width: 100%;
}

input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #374151;
  border-radius: 8px;
  font-size: 14px;
  background: #1f2937;
  color: #f3f4f6;
  transition: all 0.2s ease;
}

input::placeholder {
  color: #6b7280;
}

input:focus {
  outline: none;
  border-color: #4b5563;
  background: #111827;
}

.suggestions {
  list-style: none;
  margin: 0;
  padding: 0;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #374151;
  border-top: none;
  background: #1f2937;
  border-radius: 0 0 8px 8px;
  margin-top: -8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.suggestions li {
  padding: 10px 16px;
  cursor: pointer;
  color: #d1d5db;
  font-size: 13px;
  transition: background 0.15s ease;
  border-bottom: 1px solid #374151;
}

.suggestions li:last-child {
  border-bottom: none;
}

.suggestions li:hover {
  background: #374151;
  color: #ffffff;
}

.suggestions::-webkit-scrollbar {
  width: 6px;
}

.suggestions::-webkit-scrollbar-track {
  background: #1f2937;
}

.suggestions::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 3px;
}

.suggestions::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style>