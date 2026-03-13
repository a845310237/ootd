import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/api/client'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  // Initialize from localStorage
  function init() {
    isLoading.value = true
    const savedToken = localStorage.getItem('access_token')
    const savedUser = localStorage.getItem('user')

    if (savedToken && savedUser) {
      token.value = savedToken
      try {
        user.value = JSON.parse(savedUser)
        console.log('✅ Auth restored from localStorage:', user.value?.email)
      } catch {
        console.error('❌ Failed to parse saved user data')
        clearAuth()
      }
    } else {
      console.log('ℹ️ No saved auth found')
    }
    isLoading.value = false
  }

  // Clear authentication data
  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  // Login
  async function login(email: string, password: string) {
    try {
      isLoading.value = true
      const response = await authApi.login({ email, password })
      token.value = response.data.access_token
      user.value = response.data.user

      // Save to localStorage
      localStorage.setItem('access_token', response.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.user))

      console.log('✅ Login successful:', user.value?.email)
      return true
    } catch (error) {
      console.error('❌ Login failed:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Register
  async function register(email: string, password: string, name?: string) {
    try {
      isLoading.value = true
      await authApi.register({ email, password, name })
      console.log('✅ Registration successful')
      return true
    } catch (error) {
      console.error('❌ Registration failed:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Logout
  function logout() {
    console.log('👋 Logging out:', user.value?.email)
    clearAuth()
  }

  // Update user data
  function updateUser(updatedUser: User) {
    user.value = updatedUser
    localStorage.setItem('user', JSON.stringify(updatedUser))
  }

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    init,
    login,
    register,
    logout,
    updateUser
  }
})
