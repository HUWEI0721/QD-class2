<template>
  <div class="activities-view">
    <div class="header-actions">
      <h2 class="page-title">班级活动</h2>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        创建活动
      </el-button>
    </div>

    <!-- 活动统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon"><Calendar /></el-icon>
            <div class="stat-info">
              <div class="stat-number">{{ activities.length }}</div>
              <div class="stat-label">总活动数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon upcoming"><Clock /></el-icon>
            <div class="stat-info">
              <div class="stat-number">{{ upcomingActivities.length }}</div>
              <div class="stat-label">即将开始</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon completed"><Check /></el-icon>
            <div class="stat-info">
              <div class="stat-number">{{ completedActivities.length }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 活动筛选 -->
    <el-card class="filter-card">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-select v-model="filterStatus" placeholder="活动状态" clearable>
            <el-option label="全部" value="" />
            <el-option label="即将开始" value="upcoming" />
            <el-option label="进行中" value="ongoing" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="filterDate"
            type="month"
            placeholder="选择月份"
            clearable
          />
        </el-col>
        <el-col :span="12">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索活动标题或描述..."
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
      </el-row>
    </el-card>

    <!-- 活动列表 -->
    <div class="activities-container">
      <div v-if="filteredActivities.length === 0" class="empty-state">
        <el-empty description="暂无活动" />
      </div>
      
      <div v-else class="activities-grid">
        <el-card
          v-for="activity in filteredActivities"
          :key="activity.id"
          class="activity-card"
          shadow="hover"
        >
          <div class="activity-header">
            <div class="activity-status" :class="getActivityStatus(activity)">
              {{ getActivityStatusText(activity) }}
            </div>
            <el-dropdown @command="(command) => handleActivityAction(command, activity)">
              <el-icon class="activity-menu"><MoreFilled /></el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="edit">编辑</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>

          <div class="activity-content">
            <h3 class="activity-title">{{ activity.title }}</h3>
            <p class="activity-description">{{ activity.description }}</p>
            
            <div class="activity-meta">
              <div class="meta-item">
                <el-icon><Calendar /></el-icon>
                <span>{{ formatDate(activity.activity_date) }}</span>
              </div>
              <div class="meta-item" v-if="activity.location">
                <el-icon><Location /></el-icon>
                <span>{{ activity.location }}</span>
              </div>
              <div class="meta-item">
                <el-icon><User /></el-icon>
                <span>{{ activity.creator?.full_name }}</span>
              </div>
            </div>

            <div class="activity-actions">
              <el-button size="small" @click="viewActivityDetail(activity)">
                查看详情
              </el-button>
              <el-button size="small" type="primary" @click="viewActivityPhotos(activity)">
                查看照片
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 创建/编辑活动弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingActivity ? '编辑活动' : '创建活动'"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="activityFormRef"
        :model="activityForm"
        :rules="activityRules"
        label-width="80px"
      >
        <el-form-item label="活动标题" prop="title">
          <el-input v-model="activityForm.title" placeholder="请输入活动标题" />
        </el-form-item>
        
        <el-form-item label="活动描述" prop="description">
          <el-input
            v-model="activityForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入活动描述"
          />
        </el-form-item>
        
        <el-form-item label="活动时间" prop="activity_date">
          <el-date-picker
            v-model="activityForm.activity_date"
            type="datetime"
            placeholder="选择活动时间"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="活动地点" prop="location">
          <el-input v-model="activityForm.location" placeholder="请输入活动地点" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitLoading" @click="submitActivity">
            {{ editingActivity ? '更新' : '创建' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { api } from '@/api'
import dayjs from 'dayjs'

const router = useRouter()

// 响应式数据
const activities = ref([])
const dialogVisible = ref(false)
const editingActivity = ref(null)
const submitLoading = ref(false)
const activityFormRef = ref()
const loading = ref(false)

const filterStatus = ref('')
const filterDate = ref('')
const searchKeyword = ref('')

// 活动表单数据
const activityForm = reactive({
  title: '',
  description: '',
  activity_date: '',
  location: ''
})

// 表单验证规则
const activityRules = {
  title: [
    { required: true, message: '请输入活动标题', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入活动描述', trigger: 'blur' }
  ],
  activity_date: [
    { required: true, message: '请选择活动时间', trigger: 'change' }
  ]
}



// 计算属性
const upcomingActivities = computed(() => {
  const now = new Date()
  return activities.value.filter(activity => new Date(activity.activity_date) > now)
})

const completedActivities = computed(() => {
  const now = new Date()
  return activities.value.filter(activity => new Date(activity.activity_date) <= now)
})

const filteredActivities = computed(() => {
  let filtered = activities.value

  // 状态筛选
  if (filterStatus.value) {
    const now = new Date()
    filtered = filtered.filter(activity => {
      const activityDate = new Date(activity.activity_date)
      switch (filterStatus.value) {
        case 'upcoming':
          return activityDate > now
        case 'completed':
          return activityDate <= now
        case 'ongoing':
          // 假设活动持续2小时
          const endTime = new Date(activityDate.getTime() + 2 * 60 * 60 * 1000)
          return activityDate <= now && now <= endTime
        default:
          return true
      }
    })
  }

  // 日期筛选
  if (filterDate.value) {
    const filterMonth = dayjs(filterDate.value).format('YYYY-MM')
    filtered = filtered.filter(activity =>
      dayjs(activity.activity_date).format('YYYY-MM') === filterMonth
    )
  }

  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(activity =>
      activity.title.toLowerCase().includes(keyword) ||
      activity.description.toLowerCase().includes(keyword)
    )
  }

  return filtered.sort((a, b) => new Date(b.activity_date) - new Date(a.activity_date))
})

// 方法
const formatDate = (date) => {
  return dayjs(date).format('YYYY年MM月DD日 HH:mm')
}

const getActivityStatus = (activity) => {
  const now = new Date()
  const activityDate = new Date(activity.activity_date)
  const endTime = new Date(activityDate.getTime() + 2 * 60 * 60 * 1000)

  if (activityDate > now) {
    return 'upcoming'
  } else if (activityDate <= now && now <= endTime) {
    return 'ongoing'
  } else {
    return 'completed'
  }
}

const getActivityStatusText = (activity) => {
  const status = getActivityStatus(activity)
  const statusMap = {
    upcoming: '即将开始',
    ongoing: '进行中',
    completed: '已完成'
  }
  return statusMap[status]
}

const showCreateDialog = () => {
  editingActivity.value = null
  Object.assign(activityForm, {
    title: '',
    description: '',
    activity_date: '',
    location: ''
  })
  dialogVisible.value = true
}

const handleActivityAction = async (command, activity) => {
  switch (command) {
    case 'edit':
      editingActivity.value = activity
      Object.assign(activityForm, {
        title: activity.title,
        description: activity.description,
        activity_date: activity.activity_date,
        location: activity.location
      })
      dialogVisible.value = true
      break
    case 'delete':
      try {
        await ElMessageBox.confirm('确定要删除这个活动吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        // 这里应该调用API删除活动
        const index = activities.value.findIndex(a => a.id === activity.id)
        if (index > -1) {
          activities.value.splice(index, 1)
          ElMessage.success('活动删除成功')
        }
      } catch {
        // 用户取消删除
      }
      break
  }
}

const submitActivity = async () => {
  if (!activityFormRef.value) return

  await activityFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (editingActivity.value) {
          // 更新活动
          await api.activities.update(editingActivity.value.id, activityForm)
          ElMessage.success('活动更新成功')
        } else {
          // 创建新活动
          await api.activities.create(activityForm)
          ElMessage.success('活动创建成功')
        }
        dialogVisible.value = false
        loadActivities() // 重新加载活动列表
      } catch (error) {
        console.error('操作失败:', error)
        ElMessage.error('操作失败，请重试')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

const viewActivityDetail = (activity) => {
  ElMessage.info('查看活动详情功能开发中...')
}

const viewActivityPhotos = (activity) => {
  router.push(`/photos?activity=${activity.id}`)
}

const loadActivities = async () => {
  loading.value = true
  try {
    const response = await api.activities.getAll()
    activities.value = response.data
  } catch (error) {
    console.error('加载活动数据失败:', error)
    ElMessage.error('加载活动数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadActivities()
})
</script>

<style scoped>
.activities-view {
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

.stats-row {
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

.stat-icon.upcoming {
  background: #e6a23c;
}

.stat-icon.completed {
  background: #67c23a;
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

.filter-card {
  margin-bottom: 24px;
}

.activities-container {
  min-height: 400px;
}

.activities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.activity-card {
  transition: all 0.3s ease;
}

.activity-card:hover {
  transform: translateY(-2px);
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.activity-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.activity-status.upcoming {
  background: #ecf5ff;
  color: #409eff;
}

.activity-status.ongoing {
  background: #fdf6ec;
  color: #e6a23c;
}

.activity-status.completed {
  background: #f0f9ff;
  color: #67c23a;
}

.activity-menu {
  cursor: pointer;
  color: #909399;
  transition: color 0.3s ease;
}

.activity-menu:hover {
  color: #409eff;
}

.activity-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.4;
}

.activity-description {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #7f8c8d;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.activity-meta {
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}

.meta-item:last-child {
  margin-bottom: 0;
}

.activity-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  padding: 60px 0;
  text-align: center;
}

.dialog-footer {
  text-align: right;
}

@media (max-width: 768px) {
  .header-actions {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .activities-grid {
    grid-template-columns: 1fr;
  }
}
</style>
