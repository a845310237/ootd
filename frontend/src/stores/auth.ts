import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient, { type User, type LoginRequest, type RegisterRequest, type LoginResponse } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<User | null>(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const currentUser = computed(() => user.value)

  // Actions
  async function login(credentials: LoginRequest) {
    loading.value = true
    try {
      const response = await apiClient.post<LoginResponse>('/auth/login', credentials)
      const { access_token, user: userData } = response.data

      // Store token and user
      token.value = access_token
      user.value = userData
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('user', JSON.stringify(userData))

      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '登录失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function register(data: RegisterRequest) {
    loading.value = true
    try {
      const response = await apiClient.post<User>('/auth/register', data)
      user.value = response.data
      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '注册失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await apiClient.post('/auth/logout')
    } catch (error) {
      // Ignore logout errors
    } finally {
      // Clear local state
      token.value = null
      user.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return

    try {
      const response = await apiClient.get<User>('/auth/me')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (error) {
      // Token might be invalid, clear auth state
      await logout()
    }
  }

  return {
    // State
    token,
    user,
    loading,
    // Getters
    isAuthenticated,
    currentUser,
    // Actions
    login,
    register,
    logout,
    fetchCurrentUser
  }
})
