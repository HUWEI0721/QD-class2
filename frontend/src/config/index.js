// 应用配置
// 在构建时，Vite会将环境变量注入到代码中
const getApiBaseUrl = () => {
  // 优先使用构建时的环境变量
  const envApiUrl = import.meta.env.VITE_API_BASE_URL
  const fallbackUrl = 'https://qd-class2-production.up.railway.app/api'
  
  console.log('🔧 API URL 配置:')
  console.log('环境变量值:', envApiUrl)
  console.log('备用URL:', fallbackUrl)
  console.log('最终使用:', envApiUrl || fallbackUrl)
  
  return envApiUrl || fallbackUrl
}

const config = {
  // API 基础URL
  apiBaseUrl: getApiBaseUrl(),
  
  // 应用信息
  appTitle: import.meta.env.VITE_APP_TITLE || '班级建设网站',
  appVersion: '1.0.0',
  
  // 环境信息
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
  
  // 默认配置
  pagination: {
    pageSize: 20,
    pageSizes: [10, 20, 50, 100]
  },
  
  // 文件上传配置
  upload: {
    maxSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/mov']
  }
}

export default config
