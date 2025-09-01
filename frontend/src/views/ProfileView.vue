<template>
  <div class="profile-container">
    <!-- 个人资料头部 -->
    <div class="profile-header">
      <div class="header-bg"></div>
      <div class="profile-main">
        <div class="avatar-section">
          <div class="avatar-wrapper">
            <el-avatar 
              :size="120" 
              :src="userInfo.avatar_url" 
              class="profile-avatar"
            >
              {{ userInfo.full_name?.charAt(0) }}
            </el-avatar>
            <el-upload
              ref="avatarUpload"
              :action="uploadUrl"
              :headers="uploadHeaders"
              :show-file-list="false"
              :before-upload="beforeAvatarUpload"
              :on-success="handleAvatarSuccess"
              :on-error="handleUploadError"
              accept="image/*"
              class="avatar-upload"
            >
              <el-button circle size="large" class="upload-btn">
                <el-icon><Camera /></el-icon>
              </el-button>
            </el-upload>
          </div>
        </div>
        
        <div class="profile-info">
          <h1 class="user-name">{{ userInfo.full_name }}</h1>
          <div class="user-meta">
            <el-tag :type="getRoleType(userInfo.role)" size="large" class="role-tag">
              {{ getRoleText(userInfo.role) }}
            </el-tag>
            <span class="join-date">
              <el-icon><Calendar /></el-icon>
              {{ formatDate(userInfo.created_at) }} 加入
            </span>
          </div>
          
          <!-- 统计信息 -->
          <div class="stats-row">
            <div class="stat-item">
              <div class="stat-number">{{ userStats.activities || 0 }}</div>
              <div class="stat-label">参与活动</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-number">{{ userStats.photos || 0 }}</div>
              <div class="stat-label">上传照片</div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <div class="stat-number">{{ userStats.comments || 0 }}</div>
              <div class="stat-label">发表评论</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 个人信息表单 -->
    <div class="profile-content">
      <el-row :gutter="24">
        <!-- 基本信息 -->
        <el-col :lg="14" :md="24">
          <el-card class="info-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <h3><el-icon><User /></el-icon>基本信息</h3>
                <el-button 
                  type="primary" 
                  :loading="saving"
                  @click="saveProfile"
                >
                  <el-icon><Check /></el-icon>
                  保存更改
                </el-button>
              </div>
            </template>
            
            <el-form
              ref="profileFormRef"
              :model="profileForm"
              :rules="profileRules"
              label-width="100px"
              class="profile-form"
            >
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="真实姓名" prop="full_name">
                    <el-input
                      v-model="profileForm.full_name"
                      placeholder="请输入真实姓名"
                      :prefix-icon="User"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="用户名" prop="username">
                    <el-input
                      v-model="profileForm.username"
                      placeholder="请输入用户名"
                      :prefix-icon="Avatar"
                      disabled
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="邮箱地址" prop="email">
                    <el-input
                      v-model="profileForm.email"
                      placeholder="请输入邮箱地址"
                      :prefix-icon="Message"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="手机号码" prop="phone">
                    <el-input
                      v-model="profileForm.phone"
                      placeholder="请输入手机号码"
                      :prefix-icon="Phone"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="性别" prop="gender">
                    <el-select v-model="profileForm.gender" placeholder="请选择性别">
                      <el-option label="男" value="male" />
                      <el-option label="女" value="female" />
                      <el-option label="保密" value="other" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="出生日期" prop="birthday">
                    <el-date-picker
                      v-model="profileForm.birthday"
                      type="date"
                      placeholder="请选择出生日期"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="个人简介" prop="bio">
                <el-input
                  v-model="profileForm.bio"
                  type="textarea"
                  :rows="4"
                  placeholder="介绍一下自己吧..."
                  maxlength="200"
                  show-word-limit
                />
              </el-form-item>

              <el-form-item label="兴趣爱好" prop="interests">
                <el-input
                  v-model="profileForm.interests"
                  placeholder="请输入兴趣爱好，用逗号分隔"
                  :prefix-icon="Star"
                />
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <!-- 侧边栏信息 -->
        <el-col :lg="10" :md="24">
          <!-- 联系信息 -->
          <el-card class="contact-card" shadow="hover">
            <template #header>
              <h3><el-icon><MessageBox /></el-icon>联系方式</h3>
            </template>
            <div class="contact-list">
              <div class="contact-item">
                <el-icon class="contact-icon"><Message /></el-icon>
                <div class="contact-content">
                  <div class="contact-label">邮箱</div>
                  <div class="contact-value">{{ userInfo.email || '未设置' }}</div>
                </div>
              </div>
              <div class="contact-item">
                <el-icon class="contact-icon"><Phone /></el-icon>
                <div class="contact-content">
                  <div class="contact-label">手机</div>
                  <div class="contact-value">{{ profileForm.phone || '未设置' }}</div>
                </div>
              </div>
              <div class="contact-item">
                <el-icon class="contact-icon"><Location /></el-icon>
                <div class="contact-content">
                  <div class="contact-label">地址</div>
                  <div class="contact-value">{{ profileForm.address || '未设置' }}</div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 账户安全 -->
          <el-card class="security-card" shadow="hover">
            <template #header>
              <h3><el-icon><Lock /></el-icon>账户安全</h3>
            </template>
            <div class="security-list">
              <div class="security-item">
                <div class="security-info">
                  <div class="security-title">修改密码</div>
                  <div class="security-desc">定期更换密码以保护账户安全</div>
                </div>
                <el-button type="primary" plain @click="showPasswordDialog = true">
                  修改
                </el-button>
              </div>
              <div class="security-item">
                <div class="security-info">
                  <div class="security-title">登录记录</div>
                  <div class="security-desc">查看最近的登录活动</div>
                </div>
                <el-button type="primary" plain>
                  查看
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showPasswordDialog"
      title="修改密码"
      width="400px"
      :before-close="handlePasswordDialogClose"
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
      >
        <el-form-item label="当前密码" prop="current_password">
          <el-input
            v-model="passwordForm.current_password"
            type="password"
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="passwordForm.new_password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input
            v-model="passwordForm.confirm_password"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" :loading="changingPassword" @click="changePassword">
          确认修改
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  User, Avatar, Message, Phone, Calendar, Camera, Check, 
  MessageBox, Lock, Location, Star 
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/api'
import dayjs from 'dayjs'
import config from '@/config'

const authStore = useAuthStore()

// 响应式数据
const userInfo = ref({ ...authStore.user })
const userStats = ref({
  activities: 0,
  photos: 0,
  comments: 0
})

const saving = ref(false)
const showPasswordDialog = ref(false)
const changingPassword = ref(false)

// 表单引用
const profileFormRef = ref()
const passwordFormRef = ref()
const avatarUpload = ref()

// 个人资料表单
const profileForm = reactive({
  full_name: '',
  username: '',
  email: '',
  phone: '',
  gender: '',
  birthday: '',
  bio: '',
  interests: '',
  address: ''
})

// 密码表单
const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// 表单验证规则
const profileRules = {
  full_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度应在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

const passwordRules = {
  current_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 计算属性
const uploadUrl = computed(() => `${config.apiBaseUrl}/users/avatar`)
const uploadHeaders = computed(() => ({
  'Authorization': `Bearer ${authStore.token}`
}))

// 工具函数
const getRoleType = (role) => {
  const typeMap = {
    'admin': 'danger',
    'teacher': 'warning',
    'student': 'success'
  }
  return typeMap[role] || 'info'
}

const getRoleText = (role) => {
  const textMap = {
    'admin': '管理员',
    'teacher': '教师',
    'student': '学生'
  }
  return textMap[role] || '用户'
}

const formatDate = (date) => {
  return date ? dayjs(date).format('YYYY年MM月DD日') : '未知'
}

// 头像上传相关
const beforeAvatarUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

const handleAvatarSuccess = (response) => {
  if (response.avatar_url) {
    userInfo.value.avatar_url = response.avatar_url
    authStore.user.avatar_url = response.avatar_url
    ElMessage.success('头像更新成功!')
  }
}

const handleUploadError = (error) => {
  console.error('头像上传失败:', error)
  ElMessage.error('头像上传失败，请重试')
}

// 保存个人资料
const saveProfile = async () => {
  try {
    await profileFormRef.value.validate()
    saving.value = true
    
    const response = await api.users.updateProfile(profileForm)
    
    // 更新本地用户信息
    Object.assign(userInfo.value, response.data)
    Object.assign(authStore.user, response.data)
    
    ElMessage.success('个人资料更新成功!')
  } catch (error) {
    console.error('更新个人资料失败:', error)
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('更新失败，请重试')
    }
  } finally {
    saving.value = false
  }
}

// 修改密码
const changePassword = async () => {
  try {
    await passwordFormRef.value.validate()
    changingPassword.value = true
    
    await api.users.changePassword(passwordForm)
    
    ElMessage.success('密码修改成功，请重新登录')
    showPasswordDialog.value = false
    
    // 清空密码表单
    Object.assign(passwordForm, {
      current_password: '',
      new_password: '',
      confirm_password: ''
    })
    
    // 延迟退出登录
    setTimeout(() => {
      authStore.logout()
    }, 1500)
  } catch (error) {
    console.error('修改密码失败:', error)
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('修改失败，请重试')
    }
  } finally {
    changingPassword.value = false
  }
}

const handlePasswordDialogClose = () => {
  // 清空表单
  passwordFormRef.value?.resetFields()
  Object.assign(passwordForm, {
    current_password: '',
    new_password: '',
    confirm_password: ''
  })
}

// 初始化数据
const initData = async () => {
  try {
    // 获取用户详细信息
    const userResponse = await api.users.getById(authStore.user.id)
    userInfo.value = userResponse.data
    
    // 填充表单数据
    Object.assign(profileForm, {
      full_name: userInfo.value.full_name || '',
      username: userInfo.value.username || '',
      email: userInfo.value.email || '',
      phone: userInfo.value.phone || '',
      gender: userInfo.value.gender || '',
      birthday: userInfo.value.birthday || '',
      bio: userInfo.value.bio || '',
      interests: userInfo.value.interests || '',
      address: userInfo.value.address || ''
    })
    
    // 获取用户统计信息
    const statsResponse = await api.users.getStats()
    userStats.value = statsResponse.data
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  }
}

onMounted(() => {
  initData()
})
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 个人资料头部 */
.profile-header {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.header-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="0.5" fill="rgba(255,255,255,0.1)"/><circle cx="10" cy="50" r="0.5" fill="rgba(255,255,255,0.1)"/><circle cx="90" cy="30" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.profile-main {
  position: relative;
  padding: 40px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.avatar-section {
  position: relative;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
}

.profile-avatar {
  border: 4px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  font-size: 48px;
  font-weight: 600;
}

.avatar-upload {
  position: absolute;
  bottom: 0;
  right: 0;
}

.upload-btn {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: none;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  color: #667eea;
  transition: all 0.3s ease;
}

.upload-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.profile-info {
  flex: 1;
  color: white;
}

.user-name {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 12px;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.role-tag {
  font-weight: 600;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.join-date {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

.stats-row {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: white;
  line-height: 1;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 4px;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.3);
}

/* 主要内容区域 */
.profile-content {
  position: relative;
  z-index: 1;
}

.info-card,
.contact-card,
.security-card {
  margin-bottom: 24px;
  border: none;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.info-card:hover,
.contact-card:hover,
.security-card:hover {
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

.profile-form {
  padding-top: 20px;
}

.profile-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #5a6c7d;
}

.profile-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  border: 1px solid #e1e8ed;
  transition: all 0.3s ease;
}

.profile-form :deep(.el-input__wrapper:hover) {
  border-color: #667eea;
}

.profile-form :deep(.el-input__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* 联系方式卡片 */
.contact-list {
  space-y: 16px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.contact-item:hover {
  background: #e8f4fd;
  transform: translateX(4px);
}

.contact-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  font-size: 18px;
}

.contact-content {
  flex: 1;
}

.contact-label {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 4px;
}

.contact-value {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

/* 安全设置卡片 */
.security-list {
  space-y: 16px;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.security-item:hover {
  background: #e8f4fd;
}

.security-info {
  flex: 1;
}

.security-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.security-desc {
  font-size: 14px;
  color: #7f8c8d;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-main {
    flex-direction: column;
    text-align: center;
    padding: 24px 20px;
  }
  
  .user-name {
    font-size: 28px;
  }
  
  .stats-row {
    justify-content: center;
  }
  
  .profile-content {
    padding: 0 16px;
  }
}

/* 对话框样式 */
:deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 24px;
}

:deep(.el-dialog__title) {
  color: white;
  font-weight: 600;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 24px;
  background: #f8fafc;
}
</style>