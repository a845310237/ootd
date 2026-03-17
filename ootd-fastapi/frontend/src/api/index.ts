import apiClient, { type User, type Clothing, type Outfit, type TokenResponse } from './client'

// Auth API
export const authApi = {
  register: (data: { email: string; password: string; name?: string }) =>
    apiClient.post<User>('/auth/register', data),

  login: (data: { email: string; password: string }) => {
    const formData = new FormData()
    formData.append('username', data.email)
    formData.append('password', data.password)
    return apiClient.post<TokenResponse>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },

  logout: () => apiClient.post('/auth/logout')
}

// User API
export const userApi = {
  getMe: () => apiClient.get<User>('/users/me'),
  updateMe: (data: Partial<User>) => apiClient.put<User>('/users/me', data)
}

// Clothing API
export const clothingApi = {
  getList: (params?: { category?: string; search?: string }) =>
    apiClient.get<Clothing[]>('/clothing', { params }),

  getDetail: (id: string) =>
    apiClient.get<Clothing>(`/clothing/${id}`),

  create: (data: Partial<Clothing>) =>
    apiClient.post<Clothing>('/clothing', data),

  update: (id: string, data: Partial<Clothing>) =>
    apiClient.put<Clothing>(`/clothing/${id}`, data),

  delete: (id: string) =>
    apiClient.delete(`/clothing/${id}`)
}

// Outfit API
export const outfitApi = {
  getList: () =>
    apiClient.get<Outfit[]>('/outfits'),

  getDetail: (id: string) =>
    apiClient.get<Outfit>(`/outfits/${id}`),

  create: (data: { name: string; style: string; occasion?: string; season?: string; clothing_ids: string[] }) =>
    apiClient.post<Outfit>('/outfits/create', data),

  generate: (data: { style: string; occasion: string; season: string; reference_image?: string; custom_description?: string }) =>
    apiClient.post<Outfit>('/outfits/generate', data),

  delete: (id: string) =>
    apiClient.delete(`/outfits/${id}`)
}

// Upload API
export const uploadApi = {
  uploadImage: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post<{ url: string; size: number; type: string }>('/upload/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  uploadAvatar: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post<{ url: string; size: number; type: string }>('/upload/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
