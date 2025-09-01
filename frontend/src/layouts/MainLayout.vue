<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="260px" class="sidebar">
      <div class="logo">
        <div class="logo-icon">🎓</div>
        <div class="logo-text">
          <h2>班级建设</h2>
          <p>Class Community</p>
        </div>
      </div>
      
      <el-menu
        :default-active="$route.path"
        class="sidebar-menu"
        router
        background-color="transparent"
        text-color="rgba(255, 255, 255, 0.8)"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/" class="menu-item">
          <el-icon class="menu-icon"><House /></el-icon>
          <span>首页概览</span>
        </el-menu-item>
        
        <el-menu-item index="/classmates" class="menu-item">
          <el-icon class="menu-icon"><User /></el-icon>
          <span>班级同学</span>
        </el-menu-item>
        
        <el-menu-item index="/activities" class="menu-item">
          <el-icon class="menu-icon"><Calendar /></el-icon>
          <span>班级活动</span>
        </el-menu-item>
        
        <el-menu-item index="/photos" class="menu-item">
          <el-icon class="menu-icon"><Picture /></el-icon>
          <span>照片视频</span>
        </el-menu-item>
        
        <el-menu-item index="/profile" class="menu-item">
          <el-icon class="menu-icon"><Setting /></el-icon>
          <span>个人设置</span>
        </el-menu-item>
      </el-menu>
      
      <!-- 侧边栏底部用户信息 -->
      <div class="sidebar-footer">
        <div class="user-card">
          <el-avatar :src="authStore.user?.avatar_url" size="small" class="footer-avatar">
            {{ authStore.user?.full_name?.charAt(0) }}
          </el-avatar>
          <div class="user-text">
            <div class="user-name">{{ authStore.user?.full_name }}</div>
            <div class="user-role">{{ getRoleText(authStore.user?.role) }}</div>
          </div>
        </div>
      </div>
    </el-aside>

    <!-- 主内容区域 -->
    <el-container>
      <!-- 头部 -->
      <el-header class="header">
        <div class="header-content">
          <div class="header-left">
            <div class="page-title">
              <h1>{{ getPageTitle() }}</h1>
              <p class="page-subtitle">{{ getPageSubtitle() }}</p>
            </div>
          </div>
          
          <div class="header-right">
            <!-- 通知图标 -->
            <el-badge :value="3" class="notification-badge">
              <el-button size="large" circle>
                <el-icon><Bell /></el-icon>
              </el-button>
            </el-badge>
            
            <!-- 用户下拉菜单 -->
            <el-dropdown @command="handleCommand" class="user-dropdown-wrapper">
              <div class="user-profile">
                <el-avatar :src="authStore.user?.avatar_url" class="header-avatar">
                  {{ authStore.user?.full_name?.charAt(0) }}
                </el-avatar>
                <div class="user-info-text">
                  <div class="user-name">{{ authStore.user?.full_name }}</div>
                  <div class="user-role">{{ getRoleText(authStore.user?.role) }}</div>
                </div>
                <el-icon class="dropdown-arrow"><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    个人资料
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>
                    系统设置
                  </el-dropdown-item>
                  <el-dropdown-item command="logout" divided>
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>

      <!-- 主内容 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import { ArrowDown, Bell, User, Setting, SwitchButton } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

// 获取页面标题
const getPageTitle = () => {
  const titleMap = {
    '/': '首页概览',
    '/classmates': '班级同学',
    '/activities': '班级活动',
    '/photos': '照片视频',
    '/profile': '个人设置'
  }
  return titleMap[route.path] || '班级建设网站'
}

// 获取页面副标题
const getPageSubtitle = () => {
  const subtitleMap = {
    '/': '欢迎回来，查看最新动态和统计信息',
    '/classmates': '查看和管理班级成员信息',
    '/activities': '组织和参与班级活动',
    '/photos': '分享和浏览班级精彩瞬间',
    '/profile': '管理您的个人信息和偏好设置'
  }
  return subtitleMap[route.path] || '现代化的班级管理平台'
}

// 获取角色文本
const getRoleText = (role) => {
  const roleMap = {
    'admin': '管理员',
    'teacher': '教师',
    'student': '学生'
  }
  return roleMap[role] || '用户'
}

// 处理用户下拉菜单命令
const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中...')
      break
    case 'logout':
      authStore.logout()
      ElMessage.success('已成功退出登录')
      router.push('/login')
      break
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 侧边栏样式 */
.sidebar {
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  color: white;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.logo {
  padding: 24px 20px;
  text-align: center;
  background: rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.logo-icon {
  font-size: 32px;
  line-height: 1;
}

.logo-text h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.2;
}

.logo-text p {
  margin: 4px 0 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 400;
}

.sidebar-menu {
  border: none;
  padding: 20px 0;
}

.menu-item {
  margin: 4px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  transform: translateX(4px);
}

.menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.menu-icon {
  margin-right: 12px;
  font-size: 18px;
}

.sidebar-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-avatar {
  flex-shrink: 0;
}

.user-text {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

/* 头部样式 */
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  padding: 0 32px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.04);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-left {
  flex: 1;
}

.page-title h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1.2;
}

.page-subtitle {
  margin: 4px 0 0;
  font-size: 14px;
  color: #7f8c8d;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.notification-badge {
  position: relative;
}

.notification-badge .el-button {
  background: rgba(102, 126, 234, 0.1);
  border: none;
  color: #667eea;
  transition: all 0.3s ease;
}

.notification-badge .el-button:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

.user-dropdown-wrapper {
  cursor: pointer;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.8);
}

.user-profile:hover {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.header-avatar {
  flex-shrink: 0;
}

.user-info-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-info-text .user-name {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.2;
}

.user-info-text .user-role {
  font-size: 12px;
  color: #7f8c8d;
  margin-top: 2px;
}

.dropdown-arrow {
  color: #bdc3c7;
  transition: transform 0.3s ease;
}

.user-profile:hover .dropdown-arrow {
  transform: rotate(180deg);
}

/* 主内容样式 */
.main-content {
  background: #f8fafc;
  padding: 32px;
  overflow-y: auto;
  position: relative;
}

.main-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  pointer-events: none;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    width: 200px !important;
  }
  
  .logo-text h2 {
    font-size: 16px;
  }
  
  .page-title h1 {
    font-size: 24px;
  }
  
  .header-right {
    gap: 12px;
  }
  
  .main-content {
    padding: 20px;
  }
}

/* 下拉菜单样式 */
:deep(.el-dropdown-menu) {
  border-radius: 12px;
  border: none;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.12);
  padding: 8px;
}

:deep(.el-dropdown-menu__item) {
  border-radius: 8px;
  margin: 2px 0;
  padding: 12px 16px;
  transition: all 0.3s ease;
}

:deep(.el-dropdown-menu__item:hover) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

:deep(.el-dropdown-menu__item .el-icon) {
  margin-right: 8px;
}
</style>
