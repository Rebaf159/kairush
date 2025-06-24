import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Views
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import DashboardView from '@/views/DashboardView.vue'
import CreationView from '@/views/CreationView.vue'
import CharacterSelectionView from '@/views/CharacterSelectionView.vue'
import ChatView from '@/views/ChatView.vue'
import ProfileView from '@/views/ProfileView.vue'

// Layouts
import AuthLayout from '@/layouts/AuthLayout.vue'
import AppLayout from '@/layouts/AppLayout.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { requiresGuest: true }
  },
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'Login',
        component: LoginView,
        meta: { requiresGuest: true }
      },
      {
        path: 'register',
        name: 'Register',
        component: RegisterView,
        meta: { requiresGuest: true }
      }
    ]
  },
  {
    path: '/app',
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: DashboardView
      },
      {
        path: 'create',
        name: 'Creation',
        component: CreationView
      },
      {
        path: 'characters',
        name: 'Characters',
        component: CharacterSelectionView
      },
      {
        path: 'chat/:id',
        name: 'Chat',
        component: ChatView,
        props: true
      },
      {
        path: 'profile',
        name: 'Profile',
        component: ProfileView
      },
      {
        path: '',
        redirect: '/app/dashboard'
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Kimlik doğrulama gerektiren rotalar
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/auth/login')
    return
  }
  
  // Misafir kullanıcılar için rotalar (giriş yapmış kullanıcılar erişemez)
  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    next('/app/dashboard')
    return
  }
  
  next()
})

export default router