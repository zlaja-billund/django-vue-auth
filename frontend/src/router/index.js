import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

import HomeView from '../views/HomeView.vue'
import Login from '@/views/auth/Login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      meta: {
        requiresAuth: true,
      },
      component: HomeView
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
  ]
})

router.beforeEach(async (to, from, next) => {

  const auth = useAuthStore();

  if(to.meta.requiresAuth) {
    if (!auth.accessKey) {
      next({ name: 'Login' })
    }
    else {
      next();
    }
  } else {
    // This redirect to home all public pages that not require authentication. If user is logged in. E.g you can't access page login if you are logged in.
    if(auth.accessKey)
    {
      next({name: 'Home'});
    }
    else {
      next();
    }
  }
  
})

export default router
