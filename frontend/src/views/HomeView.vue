<template>
  <div class="home-view">
    <!-- 欢迎卡片 -->
    <el-card class="welcome-card" shadow="hover">
      <div class="welcome-content">
        <div class="welcome-text">
          <h1>欢迎回来，{{ authStore.user?.full_name }}！</h1>
          <p>这里是我们班级的数字家园，记录美好时光，分享精彩瞬间</p>
        </div>
        <div class="welcome-stats">
          <div class="stat-item">
            <el-icon class="stat-icon"><User /></el-icon>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalStudents }}</div>
              <div class="stat-label">班级成员</div>
            </div>
          </div>
          <div class="stat-item">
            <el-icon class="stat-icon"><Calendar /></el-icon>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalActivities }}</div>
              <div class="stat-label">班级活动</div>
            </div>
          </div>
          <div class="stat-item">
            <el-icon class="stat-icon"><Picture /></el-icon>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalPhotos }}</div>
              <div class="stat-label">照片视频</div>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 功能快捷入口 -->
    <div class="quick-actions">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="action-card" shadow="hover" @click="$router.push('/classmates')">
            <div class="action-content">
              <el-icon class="action-icon"><User /></el-icon>
              <h3>班级同学</h3>
              <p>查看班级成员信息</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="action-card" shadow="hover" @click="$router.push('/activities')">
            <div class="action-content">
              <el-icon class="action-icon"><Calendar /></el-icon>
              <h3>班级活动</h3>
              <p>浏览班级活动安排</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="action-card" shadow="hover" @click="$router.push('/photos')">
            <div class="action-content">
              <el-icon class="action-icon"><Picture /></el-icon>
              <h3>照片视频</h3>
              <p>分享美好回忆</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="action-card" shadow="hover" @click="$router.push('/profile')">
            <div class="action-content">
              <el-icon class="action-icon"><Setting /></el-icon>
              <h3>个人资料</h3>
              <p>管理个人信息</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 最新活动 -->
    <el-card class="recent-activities" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="card-title">最新活动</span>
          <router-link to="/activities" class="more-link">查看更多</router-link>
        </div>
      </template>
      
      <div v-if="recentActivities.length === 0" class="empty-state">
        <el-empty description="暂无活动记录" />
      </div>
      
      <div v-else class="activities-list">
        <div
          v-for="activity in recentActivities"
          :key="activity.id"
          class="activity-item"
        >
          <div class="activity-date">
            <div class="date-day">{{ formatDate(activity.activity_date, 'DD') }}</div>
            <div class="date-month">{{ formatDate(activity.activity_date, 'MMM') }}</div>
          </div>
          <div class="activity-content">
            <h4>{{ activity.title }}</h4>
            <p>{{ activity.description }}</p>
            <div class="activity-meta">
              <span><el-icon><Location /></el-icon>{{ activity.location || '待定' }}</span>
              <span><el-icon><User /></el-icon>{{ activity.creator?.full_name }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 班级动态 -->
    <el-card class="class-news" shadow="hover">
      <template #header>
        <div class="card-header">
          <span class="card-title">班级动态</span>
        </div>
      </template>
      
      <div class="news-list">
        <div class="news-item">
          <el-icon class="news-icon"><Star /></el-icon>
          <div class="news-content">
            <span class="news-text">欢迎使用班级建设网站！</span>
            <span class="news-time">刚刚</span>
          </div>
        </div>
        <div class="news-item">
          <el-icon class="news-icon"><Bell /></el-icon>
          <div class="news-content">
            <span class="news-text">系统已为您开启消息通知</span>
            <span class="news-time">1分钟前</span>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/api'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const authStore = useAuthStore()

// 统计数据
const stats = reactive({
  totalStudents: 0,
  totalActivities: 0,
  totalPhotos: 0
})

// 最新活动
const recentActivities = ref([])
const loading = ref(false)

// 格式化日期
const formatDate = (date, format = 'YYYY-MM-DD') => {
  return dayjs(date).format(format)
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 并行加载所有统计数据
    const [userStats, activityStats, mediaStats, activities] = await Promise.all([
      api.users.getStats(),
      api.activities.getStats(),
      api.media.getStats(),
      api.activities.getAll({ limit: 5 })
    ])

    // 更新统计数据
    stats.totalStudents = userStats.data.total_users
    stats.totalActivities = activityStats.data.total_activities
    stats.totalPhotos = mediaStats.data.total_photos

    // 更新最新活动
    recentActivities.value = activities.data
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败，请刷新页面重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-card {
  margin-bottom: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.welcome-card :deep(.el-card__body) {
  padding: 40px;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-text h1 {
  margin: 0 0 12px 0;
  font-size: 32px;
  font-weight: 600;
}

.welcome-text p {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.welcome-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  font-size: 24px;
  opacity: 0.8;
}

.stat-number {
  font-size: 28px;
  font-weight: 600;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.quick-actions {
  margin-bottom: 24px;
}

.action-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 140px;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.action-content {
  text-align: center;
  padding: 20px;
}

.action-icon {
  font-size: 36px;
  color: #409eff;
  margin-bottom: 12px;
}

.action-content h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #2c3e50;
}

.action-content p {
  margin: 0;
  font-size: 14px;
  color: #7f8c8d;
}

.recent-activities,
.class-news {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.more-link {
  color: #409eff;
  text-decoration: none;
  font-size: 14px;
}

.more-link:hover {
  color: #66b1ff;
}

.activities-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.activity-item:hover {
  background: #e9ecef;
}

.activity-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  background: #409eff;
  color: white;
  border-radius: 8px;
  padding: 8px;
}

.date-day {
  font-size: 20px;
  font-weight: 600;
  line-height: 1;
}

.date-month {
  font-size: 12px;
  text-transform: uppercase;
}

.activity-content h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #2c3e50;
}

.activity-content p {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #7f8c8d;
}

.activity-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #95a5a6;
}

.activity-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.news-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.news-item:hover {
  background: #f8f9fa;
}

.news-icon {
  font-size: 16px;
  color: #409eff;
}

.news-content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.news-text {
  font-size: 14px;
  color: #2c3e50;
}

.news-time {
  font-size: 12px;
  color: #95a5a6;
}

.empty-state {
  padding: 40px 0;
}

@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
  }
  
  .welcome-stats {
    gap: 20px;
  }
  
  .action-card {
    height: auto;
  }
}
</style>
