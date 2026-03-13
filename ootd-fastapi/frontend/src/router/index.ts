import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/RegisterView.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    redirect: '/dashboard/wardrobe',
    children: [
      {
        path: 'wardrobe',
        name: 'Wardrobe',
        component: () => import('@/views/dashboard/WardrobeView.vue')
      },
      {
        path: 'wardrobe/add',
        name: 'AddClothing',
        component: () => import('@/views/dashboard/AddClothingView.vue')
      },
      {
        path: 'outfits',
        name: 'Outfits',
        component: () => import('@/views/dashboard/OutfitsView.vue')
      },
      {
        path: 'outfits/generate',
        name: 'GenerateOutfit',
        component: () => import('@/views/dashboard/GenerateOutfitView.vue')
      },
      {
        path: 'outfits/create',
        name: 'CreateOutfit',
        component: () => import('@/views/dashboard/CreateOutfitView.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/dashboard/ProfileView.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
