<script setup>
import { ref } from 'vue'
// Assurez-vous que ces chemins d'accès sont corrects
import SearchBar from '@/components/SearchBar.vue'
import GlobeCesium from '@/components/GlobeCesium.vue'
import Tableaudebord from '@/components/Tableaudebord.vue'
import { RouterLink } from 'vue-router' // Importé pour garantir l'accessibilité

// L'état 'target' sert de pont de données entre les composants
const target = ref(null)
</script>

<template>
  <!-- Conteneur principal: remplissage complet de la fenêtre et flexbox vertical -->
  <div class="flex flex-col h-screen w-full bg-gray-900 text-white">
<!--      -->

    <!-- 2. Conteneur principal du contenu: Vue et Tableau de bord -->
    <!-- AJOUT de 'pt-16' pour compenser la hauteur de la barre de navigation fixe -->
    <main class="flex-1 flex min-h-0 relative pt-16"> 
      
      <!-- Colonne du Tableau de Bord (Taille fixe) -->
      <!-- Utilisez un z-index élevé pour qu'il reste au-dessus du globe -->
      <div class="relative z-10 p-4 w-full sm:w-96 flex-shrink-0">
        <!-- SearchBar est placée au-dessus du tableau de bord pour une meilleure ergonomie -->
        <SearchBar @location-selected="target = $event" class="mb-4" />
        
        <!-- Le Tableau de bord doit avoir une hauteur limitée pour le défilement si nécessaire -->
        <Tableaudebord :location="target" class="overflow-y-auto max-h-full" />
      </div>

      <!-- Colonne du Globe (Prend l'espace restant) -->
      <div class="flex-1 min-w-0 relative">
        <!-- Le globe prend tout l'espace disponible -->
        <GlobeCesium :target="target" />
      </div>
      
    </main>
  </div>
</template>

<style scoped>
/* Pour s'assurer que l'application prend toute la hauteur de la fenêtre */
.h-screen {
  height: 100vh;
}

/* Styles pour les liens RouterLink non-actifs, si nécessaire */
</style>
