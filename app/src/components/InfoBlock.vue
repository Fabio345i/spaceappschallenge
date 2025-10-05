<template>
  <div class="bg-gray-800/70 rounded-md p-2">
    <p class="text-xs text-gray-400 mb-1">{{ label }}</p>
    <p class="text-sm font-medium text-gray-100">{{ value }}</p>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: String
})
</script>
