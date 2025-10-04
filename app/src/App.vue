<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-gray-100">
    
    <!-- NAVBAR -->
    <header class="flex justify-between items-center px-8 py-4 border-b border-white/10 bg-white/5 backdrop-blur-md shadow-lg">
      <h1 class="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-indigo-400">
        🌌 NASA Météo
      </h1>

      <nav class="flex gap-6 text-sm font-medium">
        <RouterLink 
          to="/" 
          class="transition text-gray-300 hover:text-sky-400"
          active-class="text-sky-400 font-semibold"
        >
          Accueil
        </RouterLink>

        <RouterLink 
          to="/about" 
          class="transition text-gray-300 hover:text-indigo-400"
          active-class="text-indigo-400 font-semibold"
        >
          À propos
        </RouterLink>
      </nav>
    </header>

    <!-- PAGE CONTENT -->
    <main class="flex-1 p-6">
      <transition name="fade" mode="out-in">
        <RouterView />
      </transition>
    </main>

    <!-- FOOTER -->
    <footer class="text-center text-gray-500 text-sm py-4 border-t border-white/10 bg-white/5 backdrop-blur-md">
      Données fournies par 
      <span class="text-sky-400">NASA GES DISC</span> & 
      <span class="text-indigo-400">Open-Meteo API</span>.
    </footer>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
