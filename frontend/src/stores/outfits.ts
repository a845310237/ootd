import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient, { type Outfit, type OutfitItem } from '@/api/client'

export interface OutfitRequirements {
  style: string
  occasion: string
  season: string
}

export interface GenerateOutfitRequest extends OutfitRequirements {}

export interface GeneratedOutfit {
  selected_items: OutfitItem[]
  reasoning: string
  tips: string[]
  requirements: OutfitRequirements
}

export const useOutfitsStore = defineStore('outfits', () => {
  // State
  const items = ref<Outfit[]>([])
  const currentOutfit = ref<Outfit | null>(null)
  const generatedOutfit = ref<GeneratedOutfit | null>(null)
  const loading = ref(false)

  // Getters
  const aiGeneratedOutfits = computed(() =>
    items.value.filter(outfit => outfit.aiGenerated)
  )

  const manualOutfits = computed(() =>
    items.value.filter(outfit => !outfit.aiGenerated)
  )

  // Actions
  async function fetchOutfits() {
    loading.value = true
    try {
      const response = await apiClient.get<{ items: Outfit[]; count: number }>('/outfits')
      items.value = response.data.items
      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '获取搭配列表失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function fetchOutfit(id: string) {
    loading.value = true
    try {
      const response = await apiClient.get<Outfit>(`/outfits/${id}`)
      currentOutfit.value = response.data
      return { success: true, data: response.data }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '获取搭配详情失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function createOutfit(data: {
    name: string
    style: string
    occasion?: string
    season?: string
    itemIds: string[]
  }) {
    loading.value = true
    try {
      const response = await apiClient.post<Outfit>('/outfits/create', data)
      items.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '创建搭配失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function generateOutfit(requirements: GenerateOutfitRequest) {
    loading.value = true
    try {
      const response = await apiClient.post<GeneratedOutfit>('/outfits/generate', requirements)
      generatedOutfit.value = response.data
      return { success: true, data: response.data }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '生成搭配失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function saveGeneratedOutfit(data: {
    name: string
    style: string
    occasion?: string
    season?: string
    itemIds: string[]
    reasoning?: string
    tips?: string[]
  }) {
    loading.value = true
    try {
      const response = await apiClient.post<Outfit>('/outfits/save', data)
      items.value.unshift(response.data)
      generatedOutfit.value = null
      return { success: true, data: response.data }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '保存搭配失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function deleteOutfit(id: string) {
    loading.value = true
    try {
      await apiClient.delete(`/outfits/${id}`)
      items.value = items.value.filter(outfit => outfit.id !== id)
      if (currentOutfit.value?.id === id) {
        currentOutfit.value = null
      }
      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '删除搭配失败'
      }
    } finally {
      loading.value = false
    }
  }

  function clearGeneratedOutfit() {
    generatedOutfit.value = null
  }

  return {
    // State
    items,
    currentOutfit,
    generatedOutfit,
    loading,
    // Getters
    aiGeneratedOutfits,
    manualOutfits,
    // Actions
    fetchOutfits,
    fetchOutfit,
    createOutfit,
    generateOutfit,
    saveGeneratedOutfit,
    deleteOutfit,
    clearGeneratedOutfit
  }
})
