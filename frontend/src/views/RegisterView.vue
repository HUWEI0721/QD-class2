<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>创建账号</h2>
        <p>加入我们的班级大家庭</p>
      </div>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
        label-position="top"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="请输入用户名"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="真实姓名" prop="full_name">
              <el-input
                v-model="registerForm.full_name"
                placeholder="请输入真实姓名"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            type="email"
            placeholder="请输入邮箱地址"
          />
        </el-form-item>
        
        <el-form-item label="学号" prop="student_id">
          <el-input
            v-model="registerForm.student_id"
            placeholder="请输入学号（可选）"
          />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="请输入密码"
                show-password
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                show-password
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input
                v-model="registerForm.phone"
                placeholder="请输入手机号（可选）"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="QQ号" prop="qq">
              <el-input
                v-model="registerForm.qq"
                placeholder="请输入QQ号（可选）"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="微信号" prop="wechat">
              <el-input
                v-model="registerForm.wechat"
                placeholder="请输入微信号（可选）"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="宿舍" prop="dormitory">
              <el-input
                v-model="registerForm.dormitory"
                placeholder="请输入宿舍号（可选）"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="家乡" prop="hometown">
          <el-input
            v-model="registerForm.hometown"
            placeholder="请输入家乡（可选）"
          />
        </el-form-item>
        
        <el-form-item label="个人简介" prop="bio">
          <el-input
            v-model="registerForm.bio"
            type="textarea"
            :rows="3"
            placeholder="介绍一下自己吧（可选）"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="register-button"
            :loading="authStore.loading"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="register-footer">
        <span>已有账号？</span>
        <router-link to="/login" class="login-link">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const registerFormRef = ref()

// 注册表单数据
const registerForm = reactive({
  username: '',
  email: '',
  full_name: '',
  student_id: '',
  password: '',
  confirmPassword: '',
  phone: '',
  qq: '',
  wechat: '',
  dormitory: '',
  hometown: '',
  bio: ''
})

// 确认密码验证器
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      // 移除确认密码字段
      const { confirmPassword, ...userData } = registerForm
      
      const success = await authStore.register(userData)
      if (success) {
        router.push('/login')
      }
    }
  })
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 800px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-height: 90vh;
  overflow-y: auto;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
}

.register-header p {
  margin: 0;
  color: #7f8c8d;
  font-size: 14px;
}

.register-form {
  margin-bottom: 20px;
}

.register-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 500;
}

.register-footer {
  text-align: center;
  font-size: 14px;
  color: #7f8c8d;
}

.login-link {
  color: #409eff;
  text-decoration: none;
  margin-left: 4px;
}

.login-link:hover {
  color: #66b1ff;
}

:deep(.el-form-item__label) {
  color: #606266;
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-textarea__inner) {
  border-radius: 8px;
}
</style>
