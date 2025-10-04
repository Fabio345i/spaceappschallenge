// 🚀 src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 🧩 Lazy loading du composant principal
const Tableaudebord = () => import('@/components/Tableaudebord.vue')

// 🛰️ Configuration du routeur
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'tableaudebord',
      component: Tableaudebord,
      meta: {
        title: 'Tableau de bord | NASA Météo',
        transition: 'fade',
      },
    },
    // 🔁 Redirection automatique pour toute route inconnue
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

// 🧠 Mise à jour automatique du titre de la page
router.afterEach((to) => {
  document.title = to.meta.title || 'NASA Dashboard'
})

export default router
