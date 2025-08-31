<template>
  <div class="api-test-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>🔍 API连接测试</span>
        </div>
      </template>
      
      <div class="test-section">
        <h3>当前配置</h3>
        <p><strong>API Base URL:</strong> {{ apiBaseUrl }}</p>
        <p><strong>环境:</strong> {{ isDev ? '开发环境' : '生产环境' }}</p>
      </div>

      <div class="test-section">
        <h3>连接测试</h3>
        <el-space direction="vertical" fill style="width: 100%">
          
          <!-- 基础连接测试 -->
          <el-button @click="testBasicConnection" :loading="loading.basic" type="primary">
            测试基础连接 (fetch)
          </el-button>
          <div v-if="results.basic" class="test-result">
            <pre>{{ results.basic }}</pre>
          </div>

          <!-- Axios测试 -->
          <el-button @click="testAxiosConnection" :loading="loading.axios" type="success">
            测试Axios连接
          </el-button>
          <div v-if="results.axios" class="test-result">
            <pre>{{ results.axios }}</pre>
          </div>

          <!-- API客户端测试 -->
          <el-button @click="testApiClient" :loading="loading.api" type="warning">
            测试API客户端
          </el-button>
          <div v-if="results.api" class="test-result">
            <pre>{{ results.api }}</pre>
          </div>

          <!-- 登录测试 -->
          <el-button @click="testLogin" :loading="loading.login" type="danger">
            测试登录API
          </el-button>
          <div v-if="results.login" class="test-result">
            <pre>{{ results.login }}</pre>
          </div>

        </el-space>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import config from '@/config'
import { api } from '@/api'
import axios from 'axios'

const apiBaseUrl = ref(config.apiBaseUrl)
const isDev = ref(config.isDevelopment)

const loading = ref({
  basic: false,
  axios: false,
  api: false,
  login: false
})

const results = ref({
  basic: null,
  axios: null,
  api: null,
  login: null
})

// 基础fetch测试
const testBasicConnection = async () => {
  loading.value.basic = true
  try {
    console.log('🔍 测试基础连接:', `${apiBaseUrl.value.replace('/api', '')}/health`)
    
    const response = await fetch(`${apiBaseUrl.value.replace('/api', '')}/health`)
    const data = await response.json()
    
    results.value.basic = {
      status: 'SUCCESS',
      url: `${apiBaseUrl.value.replace('/api', '')}/health`,
      response: data,
      headers: Object.fromEntries(response.headers.entries())
    }
    
    ElMessage.success('基础连接测试成功')
  } catch (error) {
    console.error('基础连接测试失败:', error)
    results.value.basic = {
      status: 'ERROR',
      error: error.message,
      stack: error.stack
    }
    ElMessage.error('基础连接测试失败')
  } finally {
    loading.value.basic = false
  }
}

// Axios测试
const testAxiosConnection = async () => {
  loading.value.axios = true
  try {
    console.log('🔍 测试Axios连接:', `${apiBaseUrl.value}/health`)
    
    const response = await axios.get(`${apiBaseUrl.value}/health`)
    
    results.value.axios = {
      status: 'SUCCESS',
      url: `${apiBaseUrl.value}/health`,
      data: response.data,
      status_code: response.status,
      headers: response.headers
    }
    
    ElMessage.success('Axios连接测试成功')
  } catch (error) {
    console.error('Axios连接测试失败:', error)
    results.value.axios = {
      status: 'ERROR',
      error: error.message,
      response: error.response?.data,
      status_code: error.response?.status
    }
    ElMessage.error('Axios连接测试失败')
  } finally {
    loading.value.axios = false
  }
}

// API客户端测试
const testApiClient = async () => {
  loading.value.api = true
  try {
    console.log('🔍 测试API客户端 - 测试不需要认证的端点')
    
    // 测试基础API端点，不需要认证
    const response = await axios.get(`${apiBaseUrl.value}/health`)
    
    results.value.api = {
      status: 'SUCCESS',
      method: 'GET',
      url: `${apiBaseUrl.value}/health`,
      data: response.data
    }
    
    ElMessage.success('API客户端测试成功')
  } catch (error) {
    console.error('API客户端测试失败:', error)
    results.value.api = {
      status: 'ERROR',
      error: error.message,
      response: error.response?.data,
      status_code: error.response?.status
    }
    ElMessage.error('API客户端测试失败')
  } finally {
    loading.value.api = false
  }
}

// 登录测试
const testLogin = async () => {
  loading.value.login = true
  try {
    console.log('🔍 测试登录API')
    
    const response = await api.auth.login({
      username: 'admin',
      password: '123456'
    })
    
    results.value.login = {
      status: 'SUCCESS',
      data: response.data
    }
    
    ElMessage.success('登录测试成功')
  } catch (error) {
    console.error('登录测试失败:', error)
    results.value.login = {
      status: 'ERROR',
      error: error.message,
      response: error.response?.data,
      status_code: error.response?.status
    }
    ElMessage.error('登录测试失败')
  } finally {
    loading.value.login = false
  }
}

onMounted(() => {
  console.log('🔧 API测试页面已加载')
  console.log('📍 API Base URL:', apiBaseUrl.value)
  console.log('🌍 环境:', isDev.value ? '开发' : '生产')
})
</script>

<style scoped>
.api-test-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.test-section {
  margin-bottom: 30px;
}

.test-result {
  margin-top: 10px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.test-result pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
