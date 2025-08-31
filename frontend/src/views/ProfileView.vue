<template>
  <div class="profile-view">
    <div class="profile-header">
      <h2 class="page-title">个人资料</h2>
    </div>

    <el-row :gutter="24">
      <!-- 个人信息卡片 -->
      <el-col :lg="8" :md="24">
        <el-card class="profile-card">
          <div class="profile-info">
            <div class="avatar-section">
              <el-avatar :size="100" :src="userInfo.avatar_url" class="profile-avatar">
                {{ userInfo.full_name?.charAt(0) }}
              </el-avatar>
              <el-button size="small" class="avatar-upload" @click="uploadAvatar">
                <el-icon><Camera /></el-icon>
                更换头像
              </el-button>
            </div>
            
            <div class="basic-info">
              <h3 class="username">{{ userInfo.full_name }}</h3>
              <p class="role-tag">
                <el-tag :type="getRoleType(userInfo.role)">
                  {{ getRoleText(userInfo.role) }}
                </el-tag>
              </p>
              <p class="join-date">
                <el-icon><Calendar /></el-icon>
                {{ formatDate(userInfo.created_at) }} 加入
              </p>
            </div>
            
            <div class="profile-stats">
              <div class="stat-item">
                <div class="stat-number">{{ userStats.activities }}</div>
                <div class="stat-label">参与活动</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ userStats.photos }}</div>
                <div class="stat-label">上传照片</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ userStats.comments }}</div>
                <div class="stat-label">发表评论</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 快捷操作 -->
        <el-card class="quick-actions-card">
          <template #header>
            <span class="card-title">快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button class="action-button" @click="changePassword">
              <el-icon><Lock /></el-icon>
              修改密码
            </el-button>
            <el-button class="action-button" @click="exportData">
              <el-icon><Download /></el-icon>
              导出数据
            </el-button>
            <el-button class="action-button" @click="privacySettings">
              <el-icon><Setting /></el-icon>
              隐私设置
            </el-button>
          </div>
        </el-card>
      </el-col>

      <!-- 详细信息编辑 -->
      <el-col :lg="16" :md="24">
        <el-card class="edit-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">详细信息</span>
              <el-button
                v-if="!editing"
                type="primary"
                size="small"
                @click="startEdit"
              >
                <el-icon><Edit /></el-icon>
                编辑资料
              </el-button>
              <div v-else class="edit-actions">
                <el-button size="small" @click="cancelEdit">取消</el-button>
                <el-button
                  type="primary"
                  size="small"
                  :loading="saving"
                  @click="saveProfile"
                >
                  保存
                </el-button>
              </div>
            </div>
          </template>

          <el-form
            ref="profileFormRef"
            :model="editForm"
            :rules="profileRules"
            label-width="100px"
            :disabled="!editing"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="真实姓名" prop="full_name">
                  <el-input v-model="editForm.full_name" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="学号" prop="student_id">
                  <el-input v-model="editForm.student_id" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="邮箱地址" prop="email">
              <el-input v-model="editForm.email" disabled />
            </el-form-item>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="手机号码" prop="phone">
                  <el-input v-model="editForm.phone" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="QQ号码" prop="qq">
                  <el-input v-model="editForm.qq" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="微信号" prop="wechat">
                  <el-input v-model="editForm.wechat" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="宿舍号" prop="dormitory">
                  <el-input v-model="editForm.dormitory" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="家乡地址" prop="hometown">
              <el-input v-model="editForm.hometown" />
            </el-form-item>

            <el-form-item label="个人简介" prop="bio">
              <el-input
                v-model="editForm.bio"
                type="textarea"
                :rows="4"
                placeholder="介绍一下自己..."
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 活动记录 -->
        <el-card class="activity-history">
          <template #header>
            <span class="card-title">最近活动</span>
          </template>
          
          <div class="activity-timeline">
            <el-timeline>
              <el-timeline-item
                v-for="activity in recentActivities"
                :key="activity.id"
                :timestamp="formatDate(activity.created_at)"
                placement="top"
              >
                <div class="timeline-content">
                  <h4>{{ activity.title }}</h4>
                  <p>{{ activity.description }}</p>
                  <el-tag size="small">{{ activity.type }}</el-tag>
                </div>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 修改密码弹窗 -->
    <el-dialog
      v-model="passwordDialogVisible"
      title="修改密码"
      width="400px"
      destroy-on-close
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="80px"
      >
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input
            v-model="passwordForm.currentPassword"
            type="password"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            show-password
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="passwordDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="changingPassword" @click="submitPasswordChange">
            确认修改
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/api'
import dayjs from 'dayjs'

const authStore = useAuthStore()

// 响应式数据
const editing = ref(false)
const saving = ref(false)
const passwordDialogVisible = ref(false)
const changingPassword = ref(false)
const profileFormRef = ref()
const passwordFormRef = ref()

// 用户信息
const userInfo = ref({})

// 编辑表单
const editForm = reactive({
  full_name: '',
  student_id: '',
  email: '',
  phone: '',
  qq: '',
  wechat: '',
  dormitory: '',
  hometown: '',
  bio: ''
})

// 密码修改表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 用户统计
const userStats = reactive({
  activities: 5,
  photos: 12,
  comments: 8
})

// 最近活动
const recentActivities = ref([])

// 表单验证规则
const profileRules = {
  full_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 方法
const formatDate = (date) => {
  return dayjs(date).format('YYYY年MM月DD日')
}

const getRoleType = (role) => {
  const roleMap = {
    admin: 'danger',
    teacher: 'warning',
    student: 'primary'
  }
  return roleMap[role] || 'info'
}

const getRoleText = (role) => {
  const roleMap = {
    admin: '管理员',
    teacher: '教师',
    student: '学生'
  }
  return roleMap[role] || '未知'
}

const startEdit = () => {
  editing.value = true
  // 复制当前数据到编辑表单
  Object.keys(editForm).forEach(key => {
    editForm[key] = userInfo.value[key] || ''
  })
}

const cancelEdit = () => {
  editing.value = false
  // 重置表单
  Object.keys(editForm).forEach(key => {
    editForm[key] = ''
  })
}

const saveProfile = async () => {
  if (!profileFormRef.value) return

  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        const response = await api.users.updateProfile(editForm)
        
        // 更新本地用户信息
        userInfo.value = response.data
        authStore.user = response.data
        
        editing.value = false
        ElMessage.success('个人资料更新成功')
      } catch (error) {
        console.error('更新失败:', error)
        ElMessage.error('更新失败，请重试')
      } finally {
        saving.value = false
      }
    }
  })
}

const uploadAvatar = () => {
  ElMessage.info('头像上传功能开发中...')
}

const changePassword = () => {
  passwordForm.currentPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  passwordDialogVisible.value = true
}

const submitPasswordChange = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      changingPassword.value = true
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        passwordDialogVisible.value = false
        ElMessage.success('密码修改成功')
      } catch (error) {
        ElMessage.error('密码修改失败，请重试')
      } finally {
        changingPassword.value = false
      }
    }
  })
}

const exportData = () => {
  ElMessage.info('数据导出功能开发中...')
}

const privacySettings = () => {
  ElMessage.info('隐私设置功能开发中...')
}

const loadUserData = async () => {
  try {
    // 获取最新的用户信息
    const response = await api.users.getById(authStore.user.id)
    userInfo.value = response.data
    
    // 可以在这里加载用户统计数据和最近活动
    // 由于这些API还没有实现，暂时保持现有的模拟数据
  } catch (error) {
    console.error('加载用户数据失败:', error)
    // 如果API调用失败，使用authStore中的用户信息作为备用
    if (authStore.user) {
      userInfo.value = { ...authStore.user }
    }
  }
}

onMounted(() => {
  // 如果有登录用户信息，加载详细数据
  if (authStore.user) {
    loadUserData()
  }
})
</script>

<style scoped>
.profile-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  margin-bottom: 24px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
}

.profile-card {
  margin-bottom: 20px;
}

.profile-info {
  text-align: center;
}

.avatar-section {
  margin-bottom: 20px;
}

.profile-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  font-size: 36px;
  margin-bottom: 12px;
}

.avatar-upload {
  display: block;
  margin: 0 auto;
}

.basic-info {
  margin-bottom: 24px;
}

.username {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
}

.role-tag {
  margin: 0 0 12px 0;
}

.join-date {
  margin: 0;
  font-size: 14px;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #409eff;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
}

.quick-actions-card {
  margin-bottom: 20px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-button {
  justify-content: flex-start;
  width: 100%;
}

.edit-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.activity-history {
  margin-bottom: 20px;
}

.activity-timeline {
  max-height: 400px;
  overflow-y: auto;
}

.timeline-content h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #2c3e50;
}

.timeline-content p {
  margin: 0 0 8px 0;
  font-size: 13px;
  color: #7f8c8d;
  line-height: 1.4;
}

.dialog-footer {
  text-align: right;
}

@media (max-width: 768px) {
  .profile-stats {
    flex-direction: column;
    gap: 16px;
  }
  
  .quick-actions {
    flex-direction: column;
  }
}
</style>
