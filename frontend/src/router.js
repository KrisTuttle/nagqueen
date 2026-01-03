import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth.js'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('./views/Landing.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./views/Login.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('./views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reminders/new',
    name: 'NewReminder',
    component: () => import('./views/ReminderForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reminders/:id/edit',
    name: 'EditReminder',
    component: () => import('./views/ReminderForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('./views/Admin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/dashboard')
  } else if ((to.path === '/login' || to.path === '/') && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
