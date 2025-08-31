import axios from 'axios'
import { ElMessage } from 'element-plus'
import config from '@/config'

// API 基础配置
const API_BASE_URL = config.apiBaseUrl

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加认证头
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    if (error.response?.status === 401) {
      // 未授权，清除本地存储并跳转到登录页
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
      
      // 只有在不是登录页面时才跳转
      if (window.location.pathname !== '/login') {
        ElMessage.error('登录已过期，请重新登录')
        window.location.href = '/login'
      }
    } else if (error.response?.status === 403) {
      ElMessage.error('权限不足')
    } else if (error.response?.status === 404) {
      ElMessage.error('请求的资源不存在')
    } else if (error.response?.status >= 500) {
      ElMessage.error('服务器错误，请稍后重试')
    } else {
      ElMessage.error(error.response?.data?.detail || '请求失败')
    }
    return Promise.reject(error)
  }
)

// API 接口定义
export const api = {
  // 认证相关
  auth: {
    login: (credentials) => apiClient.post('/auth/login', credentials),
    register: (userData) => apiClient.post('/auth/register', userData),
    getCurrentUser: () => apiClient.get('/auth/me'),
    logout: () => apiClient.post('/auth/logout')
  },

  // 用户相关
  users: {
    getAll: (params = {}) => apiClient.get('/users/', { params }),
    getById: (id) => apiClient.get(`/users/${id}`),
    updateProfile: (data) => apiClient.put('/users/me', data),
    getStats: () => apiClient.get('/users/stats/summary')
  },

  // 活动相关
  activities: {
    getAll: (params = {}) => apiClient.get('/activities/', { params }),
    getById: (id) => apiClient.get(`/activities/${id}`),
    create: (data) => apiClient.post('/activities/', data),
    update: (id, data) => apiClient.put(`/activities/${id}`, data),
    delete: (id) => apiClient.delete(`/activities/${id}`),
    getStats: () => apiClient.get('/activities/stats/summary')
  },

  // 媒体文件相关
  media: {
    getAll: (params = {}) => apiClient.get('/media/', { params }),
    getById: (id) => apiClient.get(`/media/${id}`),
    upload: (formData) => apiClient.post('/media/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
    delete: (id) => apiClient.delete(`/media/${id}`),
    getStats: () => apiClient.get('/media/stats/summary')
  },

  // 评论相关
  comments: {
    getByMediaId: (mediaId, params = {}) => apiClient.get(`/comments/media/${mediaId}`, { params }),
    getById: (id) => apiClient.get(`/comments/${id}`),
    create: (data) => apiClient.post('/comments/', data),
    delete: (id) => apiClient.delete(`/comments/${id}`)
  },

  // 通知相关
  notifications: {
    getAll: (params = {}) => apiClient.get('/notifications/', { params }),
    markAsRead: (id) => apiClient.put(`/notifications/${id}/read`),
    markAllAsRead: () => apiClient.put('/notifications/mark-all-read'),
    delete: (id) => apiClient.delete(`/notifications/${id}`),
    getStats: () => apiClient.get('/notifications/stats')
  }
}

export default apiClient
