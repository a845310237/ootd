import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  // Landing page
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: false }
  },
  // Authentication routes
  {
    path: '/auth',
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('@/views/auth/LoginView.vue'),
        meta: { requiresAuth: false }
      },
      {
        path: 'register',
        name: 'register',
        component: () => import('@/views/auth/RegisterView.vue'),
        meta: { requiresAuth: false }
      }
    ]
  },
  // Dashboard routes (protected)
  {
    path: '/dashboard',
    redirect: '/dashboard/wardrobe',
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/wardrobe',
    name: 'wardrobe',
    component: () => import('@/views/dashboard/wardrobe/WardrobeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/wardrobe/add',
    name: 'add-clothing',
    component: () => import('@/views/dashboard/wardrobe/AddClothingView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/wardrobe/edit/:id',
    name: 'edit-clothing',
    component: () => import('@/views/dashboard/wardrobe/EditClothingView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/outfits',
    name: 'outfits',
    component: () => import('@/views/dashboard/outfits/OutfitsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/outfits/generate',
    name: 'generate-outfit',
    component: () => import('@/views/dashboard/outfits/GenerateOutfitView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/outfits/diy',
    name: 'diy-outfit',
    component: () => import('@/views/dashboard/outfits/DIYOutfitView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/outfits/:id',
    name: 'outfit-detail',
    component: () => import('@/views/dashboard/outfits/OutfitDetailView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/profile',
    name: 'profile',
    component: () => import('@/views/dashboard/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  // 404 Not Found
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth !== false

  if (requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login if trying to access protected route
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
  } else if (!requiresAuth && authStore.isAuthenticated && to.name === 'login') {
    // Redirect to dashboard if already logged in and trying to access login
    next({ name: 'wardrobe' })
  } else {
    next()
  }
})

export default router
