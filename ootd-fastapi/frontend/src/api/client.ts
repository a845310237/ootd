import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      console.log('🔒 Authentication failed - clearing credentials')
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')

      // Only redirect if not already on login/register pages
      const currentPath = window.location.pathname
      if (currentPath !== '/login' && currentPath !== '/register') {
        window.location.href = '/login'
      }
    } else if (error.response?.status === 403) {
      console.log('🚫 Access forbidden - insufficient permissions')
    }
    return Promise.reject(error)
  }
)

export default apiClient

// API types
export interface User {
  id: string
  email: string
  name?: string
  height?: number
  weight?: number
  body_type?: string
  skin_tone?: string
  avatar?: string
  created_at: string
  updated_at: string
}

export interface Clothing {
  id: string
  user_id: string
  name: string
  category: string
  color: string[]
  style: string[]
  season: string[]
  brand?: string
  size?: string
  material?: string
  image_url: string
  created_at: string
  updated_at: string
}

export interface Outfit {
  id: string
  user_id: string
  name: string
  style: string
  occasion?: string
  season?: string
  ai_generated: boolean
  result_url?: string
  prompt?: string
  reasoning?: string
  tips?: string[]
  created_at: string
  updated_at: string
  items?: OutfitItem[]
}

export interface OutfitItem {
  id: string
  clothing_id: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}
