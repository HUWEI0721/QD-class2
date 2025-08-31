import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 配置axios基础URL
const API_BASE_URL = 'http://localhost:8000/api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  // 设置认证头
  const setAuthHeader = () => {
    if (token.value) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    } else {
      delete axios.defaults.headers.common['Authorization']
    }
  }

  // 初始化认证状态
  const initializeAuth = async () => {
    if (token.value) {
      setAuthHeader()
      try {
        const response = await axios.get(`${API_BASE_URL}/auth/me`)
        user.value = response.data
        return true
      } catch (error) {
        console.error('Token验证失败:', error)
        // token无效，清除认证状态
        logout()
        return false
      }
    }
    return false
  }

  // 登录
  const login = async (credentials) => {
    loading.value = true
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials)
      const { access_token, user: userData } = response.data
      
      token.value = access_token
      user.value = userData
      
      localStorage.setItem('token', access_token)
      setAuthHeader()
      
      ElMessage.success('登录成功！')
      return true
    } catch (error) {
      const message = error.response?.data?.detail || '登录失败，请检查用户名和密码'
      ElMessage.error(message)
      return false
    } finally {
      loading.value = false
    }
  }

  // 注册
  const register = async (userData) => {
    loading.value = true
    try {
      await axios.post(`${API_BASE_URL}/auth/register`, userData)
      ElMessage.success('注册成功！请登录')
      return true
    } catch (error) {
      const message = error.response?.data?.detail || '注册失败，请重试'
      ElMessage.error(message)
      return false
    } finally {
      loading.value = false
    }
  }

  // 登出
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    ElMessage.success('已退出登录')
  }

  // 更新用户信息
  const updateProfile = async (profileData) => {
    loading.value = true
    try {
      const response = await axios.put(`${API_BASE_URL}/users/me`, profileData)
      user.value = response.data
      ElMessage.success('个人信息更新成功！')
      return true
    } catch (error) {
      const message = error.response?.data?.detail || '更新失败，请重试'
      ElMessage.error(message)
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    updateProfile,
    initializeAuth
  }
})
