import { useAuthStore } from '@/stores/Auth'

export function requireAuth(to, from, next) {
  const auth = useAuthStore()

  if (!auth.isAuthenticated) {
    return next('/login')
  }

  next()
}

export function requireAdmin(to, from, next) {
  const auth = useAuthStore()

  if (!auth.isAuthenticated) {
    return next('/login')
  }

  if (!auth.isAdmin) {
    return next('/') // ou page 403
  }

  next()
}