import axios, { AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor - add JWT token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get token from localStorage
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError<any>) => {
    if (error.response) {
      const { status, data } = error.response

      // Handle 401 Unauthorized - redirect to login
      if (status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        router.push('/auth/login')
        ElMessage.error('请先登录')
        return Promise.reject(error)
      }

      // Handle other errors
      const message = data?.error || data?.message || '请求失败'
      ElMessage.error(message)
    } else if (error.request) {
      ElMessage.error('网络错误，请检查网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }

    return Promise.reject(error)
  }
)

export default apiClient

// API response types
export interface ApiResponse<T = any> {
  data?: T
  error?: string
  message?: string
}

// User types
export interface User {
  id: string
  email: string
  name?: string
  height?: number
  weight?: number
  bodyType?: string
  skinTone?: string
  avatar?: string
}

// Clothing types
export interface Clothing {
  id: string
  name: string
  category: string
  color: string[]
  style: string[]
  season: string[]
  brand?: string
  size?: string
  material?: string
  imageUrl: string
  userId: string
  createdAt?: string
  updatedAt?: string
}

// Outfit types
export interface Outfit {
  id: string
  userId: string
  name: string
  style: string
  occasion?: string
  season?: string
  aiGenerated: boolean
  resultUrl?: string
  prompt?: string
  reasoning?: string
  tips?: string[]
  items?: OutfitItem[]
  createdAt?: string
  updatedAt?: string
}

export interface OutfitItem {
  id: string
  name: string
  category: string
  color: string[]
  style: string[]
  season: string[]
  imageUrl: string
}

// Auth types
export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  user: User
}

export interface RegisterRequest {
  email: string
  password: string
  name?: string
  height?: number
  weight?: number
  bodyType?: string
  skinTone?: string
}
