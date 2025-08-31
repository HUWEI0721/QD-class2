<template>
  <div class="classmates-view">
    <div class="header-actions">
      <h2 class="page-title">班级同学</h2>
      <div class="search-and-filter">
        <el-input
          v-model="searchQuery"
          placeholder="搜索同学姓名、学号或宿舍..."
          style="width: 300px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="selectedDormitory" placeholder="筛选宿舍" clearable style="width: 150px">
          <el-option
            v-for="dorm in dormitories"
            :key="dorm"
            :label="dorm"
            :value="dorm"
          />
        </el-select>
      </div>
    </div>

    <!-- 班级统计 -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ totalStudents }}</div>
              <div class="stat-label">总人数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon male">
              <el-icon><Male /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ maleCount }}</div>
              <div class="stat-label">男生</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon female">
              <el-icon><Female /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ femaleCount }}</div>
              <div class="stat-label">女生</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><House /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ dormitoryCount }}</div>
              <div class="stat-label">宿舍数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 同学列表 -->
    <el-card class="classmates-card">
      <div class="classmates-grid">
        <div
          v-for="student in filteredStudents"
          :key="student.id"
          class="student-card"
          @click="showStudentDetail(student)"
        >
          <div class="student-avatar">
            <el-avatar
              :size="60"
              :src="student.avatar_url"
              class="avatar"
            >
              {{ student.full_name.charAt(0) }}
            </el-avatar>
            <div class="online-status" :class="{ online: student.is_online }"></div>
          </div>
          
          <div class="student-info">
            <h3 class="student-name">{{ student.full_name }}</h3>
            <p class="student-id">学号：{{ student.student_id || '未填写' }}</p>
            <p class="student-dormitory">宿舍：{{ student.dormitory || '未填写' }}</p>
            
            <div class="student-tags">
              <el-tag v-if="student.role === 'admin'" type="danger" size="small">管理员</el-tag>
              <el-tag v-if="student.role === 'teacher'" type="warning" size="small">老师</el-tag>
              <el-tag v-if="student.hometown" size="small">{{ student.hometown }}</el-tag>
            </div>
            
            <div class="contact-icons">
              <el-tooltip content="QQ" placement="top" v-if="student.qq">
                <el-icon class="contact-icon qq"><ChatRound /></el-icon>
              </el-tooltip>
              <el-tooltip content="微信" placement="top" v-if="student.wechat">
                <el-icon class="contact-icon wechat"><ChatSquare /></el-icon>
              </el-tooltip>
              <el-tooltip content="手机" placement="top" v-if="student.phone">
                <el-icon class="contact-icon phone"><Phone /></el-icon>
              </el-tooltip>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="filteredStudents.length === 0" class="empty-state">
        <el-empty description="没有找到匹配的同学" />
      </div>
    </el-card>

    <!-- 学生详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedStudent?.full_name + ' 的详细信息'"
      width="500px"
      destroy-on-close
    >
      <div v-if="selectedStudent" class="student-detail">
        <div class="detail-avatar">
          <el-avatar :size="80" :src="selectedStudent.avatar_url">
            {{ selectedStudent.full_name.charAt(0) }}
          </el-avatar>
        </div>
        
        <div class="detail-info">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="姓名">
              {{ selectedStudent.full_name }}
            </el-descriptions-item>
            <el-descriptions-item label="学号">
              {{ selectedStudent.student_id || '未填写' }}
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              {{ selectedStudent.email }}
            </el-descriptions-item>
            <el-descriptions-item label="手机">
              {{ selectedStudent.phone || '未填写' }}
            </el-descriptions-item>
            <el-descriptions-item label="QQ">
              {{ selectedStudent.qq || '未填写' }}
            </el-descriptions-item>
            <el-descriptions-item label="微信">
              {{ selectedStudent.wechat || '未填写' }}
            </el-descriptions-item>
            <el-descriptions-item label="宿舍">
              {{ selectedStudent.dormitory || '未填写' }}
            </el-descriptions-item>
            <el-descriptions-item label="家乡">
              {{ selectedStudent.hometown || '未填写' }}
            </el-descriptions-item>
            <el-descriptions-item label="个人简介">
              {{ selectedStudent.bio || '这个人很懒，什么都没留下...' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/api'

// 响应式数据
const searchQuery = ref('')
const selectedDormitory = ref('')
const detailDialogVisible = ref(false)
const selectedStudent = ref(null)
const students = ref([])
const loading = ref(false)

// 计算属性
const filteredStudents = computed(() => {
  let filtered = students.value

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(student =>
      student.full_name.toLowerCase().includes(query) ||
      (student.student_id && student.student_id.toLowerCase().includes(query)) ||
      (student.dormitory && student.dormitory.toLowerCase().includes(query))
    )
  }

  // 宿舍过滤
  if (selectedDormitory.value) {
    filtered = filtered.filter(student => student.dormitory === selectedDormitory.value)
  }

  return filtered
})

const totalStudents = computed(() => students.value.length)
const maleCount = computed(() => Math.floor(totalStudents.value * 0.6)) // 模拟数据
const femaleCount = computed(() => totalStudents.value - maleCount.value)
const dormitoryCount = computed(() => dormitories.value.length)

const dormitories = computed(() => {
  const dorms = [...new Set(students.value.map(s => s.dormitory).filter(Boolean))]
  return dorms.sort()
})

// 方法
const showStudentDetail = (student) => {
  selectedStudent.value = student
  detailDialogVisible.value = true
}

const loadStudents = async () => {
  loading.value = true
  try {
    const response = await api.users.getAll()
    students.value = response.data.map(user => ({
      ...user,
      is_online: Math.random() > 0.5 // 模拟在线状态，实际应用中应该从后端获取
    }))
  } catch (error) {
    console.error('加载学生数据失败:', error)
    ElMessage.error('加载学生数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStudents()
})
</script>

<style scoped>
.classmates-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
}

.search-and-filter {
  display: flex;
  gap: 16px;
}

.stats-cards {
  margin-bottom: 24px;
}

.stat-card {
  cursor: default;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-icon.male {
  background: #67c23a;
}

.stat-icon.female {
  background: #f56c6c;
}

.stat-number {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
  margin-top: 4px;
}

.classmates-card {
  min-height: 400px;
}

.classmates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.student-card {
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  padding: 20px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.student-card:hover {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
  transform: translateY(-2px);
}

.student-avatar {
  position: relative;
  text-align: center;
  margin-bottom: 16px;
}

.avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.online-status {
  position: absolute;
  bottom: 4px;
  right: calc(50% - 34px);
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ddd;
  border: 2px solid white;
}

.online-status.online {
  background: #67c23a;
}

.student-info {
  text-align: center;
}

.student-name {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.student-id,
.student-dormitory {
  margin: 4px 0;
  font-size: 14px;
  color: #7f8c8d;
}

.student-tags {
  margin: 12px 0;
  display: flex;
  justify-content: center;
  gap: 6px;
  flex-wrap: wrap;
}

.contact-icons {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 12px;
}

.contact-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.contact-icon.qq {
  background: #0099ff;
  color: white;
}

.contact-icon.wechat {
  background: #07c160;
  color: white;
}

.contact-icon.phone {
  background: #ff6b35;
  color: white;
}

.contact-icon:hover {
  transform: scale(1.1);
}

.empty-state {
  padding: 60px 0;
}

.student-detail {
  text-align: center;
}

.detail-avatar {
  margin-bottom: 24px;
}

.detail-avatar .el-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.detail-info {
  text-align: left;
}

@media (max-width: 768px) {
  .header-actions {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .search-and-filter {
    flex-direction: column;
  }

  .classmates-grid {
    grid-template-columns: 1fr;
  }
}
</style>
