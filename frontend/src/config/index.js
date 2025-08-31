// 应用配置
const config = {
  // API 基础URL - 开发环境使用Railway，生产环境使用环境变量
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'https://qd-class2-production.up.railway.app/api',
  
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
