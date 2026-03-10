import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient, { type Clothing } from '@/api/client'

export const useWardrobeStore = defineStore('wardrobe', () => {
  // State
  const items = ref<Clothing[]>([])
  const loading = ref(false)
  const currentCategory = ref<string | null>(null)

  // Getters
  const categories = computed(() => {
    const uniqueCategories = new Set(items.value.map(item => item.category))
    return Array.from(uniqueCategories)
  })

  const filteredItems = computed(() => {
    if (!currentCategory.value) return items.value
    return items.value.filter(item => item.category === currentCategory.value)
  })

  const itemsByCategory = computed(() => {
    const grouped: Record<string, Clothing[]> = {}
    items.value.forEach(item => {
      if (!grouped[item.category]) {
        grouped[item.category] = []
      }
      grouped[item.category].push(item)
    })
    return grouped
  })

  // Actions
  async function fetchItems(category?: string) {
    loading.value = true
    try {
      const params = category ? { category } : {}
      const response = await apiClient.get<{ items: Clothing[]; count: number }>('/wardrobe', { params })
      items.value = response.data.items
      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '获取衣物列表失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function addItem(data: Partial<Clothing>) {
    loading.value = true
    try {
      const response = await apiClient.post<Clothing>('/wardrobe', data)
      items.value.unshift(response.data)
      return { success: true, data: response.data }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '添加衣物失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function updateItem(id: string, data: Partial<Clothing>) {
    loading.value = true
    try {
      const response = await apiClient.put<Clothing>(`/wardrobe/${id}`, data)
      const index = items.value.findIndex(item => item.id === id)
      if (index !== -1) {
        items.value[index] = response.data
      }
      return { success: true, data: response.data }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '更新衣物失败'
      }
    } finally {
      loading.value = false
    }
  }

  async function deleteItem(id: string) {
    loading.value = true
    try {
      await apiClient.delete(`/wardrobe/${id}`)
      items.value = items.value.filter(item => item.id !== id)
      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || '删除衣物失败'
      }
    } finally {
      loading.value = false
    }
  }

  function setCategory(category: string | null) {
    currentCategory.value = category
  }

  function getItemById(id: string) {
    return items.value.find(item => item.id === id)
  }

  return {
    // State
    items,
    loading,
    currentCategory,
    // Getters
    categories,
    filteredItems,
    itemsByCategory,
    // Actions
    fetchItems,
    addItem,
    updateItem,
    deleteItem,
    setCategory,
    getItemById
  }
})
