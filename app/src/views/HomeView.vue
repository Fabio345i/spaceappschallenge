<script setup>
import { ref } from 'vue'
import SearchBar from '@/components/SearchBar.vue'
import GlobeCesium from '@/components/GlobeCesium.vue'

const target = ref(null)
</script>

<template>
  <SearchBar @location-selected="target = $event" />
  <GlobeCesium :target="target" />
</template>
