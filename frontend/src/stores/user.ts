import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient, { type User } from '@/api/client'

export const useUserStore = defineStore('user', () => {
  // State
  const profile = ref<User | null>(null)
  const loading = ref(false)

  // Actions
  async function fetchProfile() {
    loading.value = true
    try {
      const response = await apiClient.get<User>('/user/profile')
      profile.value = response.data
      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '获取用户信息失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(data: Partial<User>) {
    loading.value = true
    try {
      const response = await apiClient.put<User>('/user/profile', data)
      profile.value = response.data
      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '更新用户信息失败'
      }
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    profile,
    loading,
    // Actions
    fetchProfile,
    updateProfile
  }
})
