// 调试工具
export const debugConfig = () => {
  console.log('🔍 环境变量调试信息:')
  console.log('NODE_ENV:', import.meta.env.NODE_ENV)
  console.log('MODE:', import.meta.env.MODE)
  console.log('DEV:', import.meta.env.DEV)
  console.log('PROD:', import.meta.env.PROD)
  console.log('VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)
  console.log('所有环境变量:', import.meta.env)
  
  // 检查配置文件
  import('../config/index.js').then(config => {
    console.log('📋 配置文件内容:')
    console.log('apiBaseUrl:', config.default.apiBaseUrl)
    console.log('完整配置:', config.default)
  })
}
