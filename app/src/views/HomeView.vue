<script setup>
import { ref } from 'vue'
import SearchBar from '@/components/SearchBar.vue'
import GlobeCesium from '@/components/GlobeCesium.vue'
import Tableaudebord from '../components/Tableaudebord.vue'
const target = ref(null)
</script>

<template>



  <main>
      <SearchBar @location-selected="target = $event" />
  <GlobeCesium :target="target" />

    <Tableaudebord />
  </main>
</template>
