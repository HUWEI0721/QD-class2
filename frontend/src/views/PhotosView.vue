<template>
  <div class="photos-view">
    <div class="header-actions">
      <h2 class="page-title">照片视频</h2>
      <el-button type="primary" @click="showUploadDialog">
        <el-icon><Upload /></el-icon>
        上传文件
      </el-button>
    </div>

    <!-- 筛选器 -->
    <el-card class="filter-card">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-select v-model="selectedActivity" placeholder="选择活动" clearable>
            <el-option
              v-for="activity in activities"
              :key="activity.id"
              :label="activity.title"
              :value="activity.id"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="mediaType" placeholder="文件类型" clearable>
            <el-option label="全部" value="" />
            <el-option label="照片" value="photo" />
            <el-option label="视频" value="video" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="sortBy" placeholder="排序方式">
            <el-option label="最新上传" value="upload_time" />
            <el-option label="文件名" value="filename" />
            <el-option label="浏览次数" value="views" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索文件..."
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
      </el-row>
    </el-card>

    <!-- 媒体统计 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon"><Picture /></el-icon>
            <div class="stat-info">
              <div class="stat-number">{{ totalPhotos }}</div>
              <div class="stat-label">照片</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon video"><VideoPlay /></el-icon>
            <div class="stat-info">
              <div class="stat-number">{{ totalVideos }}</div>
              <div class="stat-label">视频</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon views"><View /></el-icon>
            <div class="stat-info">
              <div class="stat-number">{{ totalViews }}</div>
              <div class="stat-label">总浏览</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 媒体网格 -->
    <div class="media-container">
      <div v-if="filteredMedia.length === 0" class="empty-state">
        <el-empty description="暂无媒体文件" />
      </div>
      
      <div v-else class="media-grid">
        <div
          v-for="item in filteredMedia"
          :key="item.id"
          class="media-item"
          @click="viewMedia(item)"
        >
          <div class="media-preview">
            <img
              v-if="item.media_type === 'photo'"
              :src="getMediaUrl(item.file_path)"
              :alt="item.title"
              class="media-image"
              @error="$event.target.src = '/api/placeholder/300/200'"
            />
            <div v-else class="video-preview">
              <el-icon class="video-icon"><VideoPlay /></el-icon>
              <img
                :src="getMediaUrl(item.file_path)"
                :alt="item.title"
                class="media-image"
                @error="$event.target.src = '/api/placeholder/300/200'"
              />
            </div>
            
            <div class="media-overlay">
              <div class="overlay-actions">
                <el-button circle size="small" @click.stop="downloadMedia(item)">
                  <el-icon><Download /></el-icon>
                </el-button>
                <el-button circle size="small" @click.stop="shareMedia(item)">
                  <el-icon><Share /></el-icon>
                </el-button>
                <el-button circle size="small" type="danger" @click.stop="deleteMedia(item)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
          
          <div class="media-info">
            <h4 class="media-title">{{ item.title || item.original_filename }}</h4>
            <div class="media-meta">
              <span class="meta-item">
                <el-icon><Calendar /></el-icon>
                {{ formatDate(item.upload_time) }}
              </span>
              <span class="meta-item">
                <el-icon><User /></el-icon>
                {{ item.uploader?.full_name }}
              </span>
              <span class="meta-item">
                <el-icon><View /></el-icon>
                {{ item.views_count }}
              </span>
            </div>
            <div class="activity-tag" v-if="item.activity">
              <el-tag size="small">{{ item.activity.title }}</el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 上传文件弹窗 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传文件"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="uploadFormRef"
        :model="uploadForm"
        :rules="uploadRules"
        label-width="80px"
      >
        <el-form-item label="选择活动" prop="activity_id">
          <el-select v-model="uploadForm.activity_id" placeholder="请选择活动" style="width: 100%">
            <el-option
              v-for="activity in activities"
              :key="activity.id"
              :label="activity.title"
              :value="activity.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="文件标题" prop="title">
          <el-input v-model="uploadForm.title" placeholder="为文件起个标题" />
        </el-form-item>
        
        <el-form-item label="文件描述">
          <el-input
            v-model="uploadForm.description"
            type="textarea"
            :rows="3"
            placeholder="描述一下这个文件..."
          />
        </el-form-item>
        
        <el-form-item label="选择文件" prop="files">
          <el-upload
            ref="uploadRef"
            class="upload-area"
            drag
            :auto-upload="false"
            :on-change="handleFileChange"
            :before-upload="beforeUpload"
            multiple
            accept="image/*,video/*"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 jpg/png/gif/mp4/mov 格式，单个文件不超过 10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <div v-if="uploadFiles.length > 0" class="file-list">
          <div v-for="(file, index) in uploadFiles" :key="index" class="file-item">
            <div class="file-info">
              <el-icon class="file-icon">
                <Picture v-if="file.type.startsWith('image/')" />
                <VideoPlay v-else />
              </el-icon>
              <span class="file-name">{{ file.name }}</span>
              <span class="file-size">{{ formatFileSize(file.size) }}</span>
            </div>
            <el-button size="small" text @click="removeFile(index)">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
        </div>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="uploading"
            :disabled="uploadFiles.length === 0"
            @click="submitUpload"
          >
            上传 ({{ uploadFiles.length }})
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 媒体预览弹窗 -->
    <el-dialog
      v-model="previewDialogVisible"
      :title="selectedMedia?.title || selectedMedia?.original_filename"
      width="80%"
      destroy-on-close
    >
      <div v-if="selectedMedia" class="media-preview-container">
        <div class="media-display">
          <img
            v-if="selectedMedia.media_type === 'photo'"
            :src="getMediaUrl(selectedMedia.file_path)"
            :alt="selectedMedia.title"
            class="preview-image"
            @error="$event.target.src = '/api/placeholder/800/600'"
          />
          <video
            v-else
            :src="getMediaUrl(selectedMedia.file_path)"
            controls
            class="preview-video"
          />
        </div>
        
        <div class="media-details">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="文件名">
              {{ selectedMedia.original_filename }}
            </el-descriptions-item>
            <el-descriptions-item label="大小">
              {{ formatFileSize(selectedMedia.file_size) }}
            </el-descriptions-item>
            <el-descriptions-item label="上传者">
              {{ selectedMedia.uploader?.full_name }}
            </el-descriptions-item>
            <el-descriptions-item label="上传时间">
              {{ formatDate(selectedMedia.upload_time) }}
            </el-descriptions-item>
            <el-descriptions-item label="所属活动">
              {{ selectedMedia.activity?.title }}
            </el-descriptions-item>
            <el-descriptions-item label="浏览次数">
              {{ selectedMedia.views_count }}
            </el-descriptions-item>
            <el-descriptions-item label="描述" :span="2">
              {{ selectedMedia.description || '暂无描述' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
        
        <!-- 评论区域 -->
        <div class="comments-section">
          <h4>评论 ({{ selectedMedia.comments?.length || 0 }})</h4>
          
          <div class="comment-input">
            <el-input
              v-model="newComment"
              type="textarea"
              :rows="2"
              placeholder="写下你的评论..."
              style="margin-bottom: 10px"
            />
            <el-button type="primary" size="small" @click="addComment">发表评论</el-button>
          </div>
          
          <div class="comments-list">
            <div
              v-for="comment in selectedMedia.comments || []"
              :key="comment.id"
              class="comment-item"
            >
              <el-avatar :size="32" class="comment-avatar">
                {{ comment.author?.full_name?.charAt(0) }}
              </el-avatar>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.author?.full_name }}</span>
                  <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                </div>
                <div class="comment-text">{{ comment.content }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute } from 'vue-router'
import { api } from '@/api'
import config from '@/config'
import dayjs from 'dayjs'

const route = useRoute()

// 响应式数据
const mediaItems = ref([])
const activities = ref([])
const uploadDialogVisible = ref(false)
const previewDialogVisible = ref(false)
const selectedMedia = ref(null)
const uploading = ref(false)
const uploadFormRef = ref()
const uploadRef = ref()
const loading = ref(false)

const selectedActivity = ref('')
const mediaType = ref('')
const sortBy = ref('upload_time')
const searchKeyword = ref('')
const newComment = ref('')
const uploadFiles = ref([])

// 上传表单数据
const uploadForm = reactive({
  activity_id: '',
  title: '',
  description: ''
})

// 表单验证规则
const uploadRules = {
  activity_id: [
    { required: true, message: '请选择活动', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入文件标题', trigger: 'blur' }
  ]
}



// 计算属性
const filteredMedia = computed(() => {
  let filtered = mediaItems.value

  // 活动筛选
  if (selectedActivity.value) {
    filtered = filtered.filter(item => item.activity_id === selectedActivity.value)
  }

  // 媒体类型筛选
  if (mediaType.value) {
    filtered = filtered.filter(item => item.media_type === mediaType.value)
  }

  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(item =>
      (item.title && item.title.toLowerCase().includes(keyword)) ||
      item.original_filename.toLowerCase().includes(keyword) ||
      (item.description && item.description.toLowerCase().includes(keyword))
    )
  }

  // 排序
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'filename':
        return a.original_filename.localeCompare(b.original_filename)
      case 'views':
        return b.views_count - a.views_count
      default: // upload_time
        return new Date(b.upload_time) - new Date(a.upload_time)
    }
  })

  return filtered
})

const totalPhotos = computed(() => {
  return mediaItems.value.filter(item => item.media_type === 'photo').length
})

const totalVideos = computed(() => {
  return mediaItems.value.filter(item => item.media_type === 'video').length
})

const totalViews = computed(() => {
  return mediaItems.value.reduce((sum, item) => sum + item.views_count, 0)
})

// 方法
const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

const formatFileSize = (size) => {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  return (size / (1024 * 1024)).toFixed(1) + ' MB'
}

// 获取媒体文件的完整URL
const getMediaUrl = (filePath) => {
  if (!filePath) return '/api/placeholder/300/200'
  // 如果已经是完整URL，直接返回
  if (filePath.startsWith('http')) return filePath
  // 否则拼接为后端静态文件URL
  const baseUrl = config.apiBaseUrl.replace('/api', '')
  return `${baseUrl}/uploads/${filePath}`
}

const showUploadDialog = () => {
  uploadForm.activity_id = ''
  uploadForm.title = ''
  uploadForm.description = ''
  uploadFiles.value = []
  uploadDialogVisible.value = true
}

const handleFileChange = (file, fileList) => {
  uploadFiles.value = fileList.map(f => f.raw).filter(Boolean)
}

const beforeUpload = (file) => {
  const isValidType = file.type.startsWith('image/') || file.type.startsWith('video/')
  if (!isValidType) {
    ElMessage.error('只能上传图片或视频文件！')
    return false
  }

  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB！')
    return false
  }

  return true
}

const removeFile = (index) => {
  uploadFiles.value.splice(index, 1)
}

const submitUpload = async () => {
  if (!uploadFormRef.value) return

  await uploadFormRef.value.validate(async (valid) => {
    if (valid && uploadFiles.value.length > 0) {
      uploading.value = true
      try {
        // 逐个上传文件
        for (let i = 0; i < uploadFiles.value.length; i++) {
          const file = uploadFiles.value[i]
          const formData = new FormData()
          formData.append('file', file)
          formData.append('activity_id', uploadForm.activity_id)
          formData.append('title', uploadForm.title + (uploadFiles.value.length > 1 ? ` (${i + 1})` : ''))
          formData.append('description', uploadForm.description || '')

          // 调用真实的上传API
          await api.media.upload(formData)
        }
        
        ElMessage.success(`成功上传 ${uploadFiles.value.length} 个文件`)
        uploadDialogVisible.value = false
        
        // 重新加载媒体列表
        const mediaResponse = await api.media.getAll()
        mediaItems.value = mediaResponse.data
      } catch (error) {
        console.error('上传失败:', error)
        ElMessage.error('上传失败，请重试')
      } finally {
        uploading.value = false
      }
    }
  })
}

const viewMedia = async (item) => {
  selectedMedia.value = item
  
  try {
    // 获取媒体详情（会增加浏览量）
    const response = await api.media.getById(item.id)
    selectedMedia.value = response.data
    
    // 获取评论列表
    const commentsResponse = await api.comments.getByMediaId(item.id)
    selectedMedia.value.comments = commentsResponse.data
    
  } catch (error) {
    console.error('加载媒体详情失败:', error)
    selectedMedia.value.comments = []
  }
  
  previewDialogVisible.value = true
}

const downloadMedia = (item) => {
  ElMessage.info('下载功能开发中...')
}

const shareMedia = (item) => {
  ElMessage.info('分享功能开发中...')
}

const deleteMedia = async (item) => {
  try {
    await ElMessageBox.confirm('确定要删除这个文件吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const index = mediaItems.value.findIndex(m => m.id === item.id)
    if (index > -1) {
      mediaItems.value.splice(index, 1)
      ElMessage.success('文件删除成功')
    }
  } catch {
    // 用户取消删除
  }
}

const addComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  
  try {
    const commentData = {
      content: newComment.value,
      media_item_id: selectedMedia.value.id
    }
    
    const response = await api.comments.create(commentData)
    
    // 添加评论到本地列表
    if (!selectedMedia.value.comments) {
      selectedMedia.value.comments = []
    }
    
    selectedMedia.value.comments.unshift(response.data)
    newComment.value = ''
    ElMessage.success('评论发表成功')
  } catch (error) {
    console.error('评论发表失败:', error)
    ElMessage.error('评论发表失败，请重试')
  }
}

const loadData = async () => {
  loading.value = true
  try {
    // 并行加载活动和媒体数据
    const [activitiesResponse, mediaResponse] = await Promise.all([
      api.activities.getAll(),
      api.media.getAll()
    ])
    
    activities.value = activitiesResponse.data
    mediaItems.value = mediaResponse.data
    
    // 如果URL中有activity参数，自动选择对应活动
    const activityParam = route.query.activity
    if (activityParam) {
      selectedActivity.value = parseInt(activityParam)
    }
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.photos-view {
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

.filter-card {
  margin-bottom: 24px;
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

.stat-icon.video {
  background: #e6a23c;
}

.stat-icon.views {
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

.media-container {
  min-height: 400px;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.media-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.media-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.media-preview {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.media-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.media-item:hover .media-image {
  transform: scale(1.05);
}

.video-preview {
  position: relative;
  height: 100%;
}

.video-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 48px;
  color: white;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.media-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.media-item:hover .media-overlay {
  opacity: 1;
}

.overlay-actions {
  display: flex;
  gap: 8px;
}

.media-info {
  padding: 16px;
}

.media-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.media-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.activity-tag {
  margin-top: 8px;
}

.empty-state {
  padding: 60px 0;
  text-align: center;
}

.upload-area {
  width: 100%;
}

.file-list {
  margin-top: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  padding: 12px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f5f7fa;
}

.file-item:last-child {
  border-bottom: none;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-icon {
  color: #409eff;
}

.file-name {
  font-size: 14px;
  color: #2c3e50;
}

.file-size {
  font-size: 12px;
  color: #909399;
}

.media-preview-container {
  max-height: 80vh;
  overflow-y: auto;
}

.media-display {
  text-align: center;
  margin-bottom: 24px;
}

.preview-image,
.preview-video {
  max-width: 100%;
  max-height: 50vh;
  border-radius: 8px;
}

.media-details {
  margin-bottom: 24px;
}

.comments-section {
  border-top: 1px solid #e4e7ed;
  padding-top: 20px;
}

.comments-section h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #2c3e50;
}

.comment-input {
  margin-bottom: 20px;
}

.comments-list {
  max-height: 300px;
  overflow-y: auto;
}

.comment-item {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.comment-avatar {
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.comment-author {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}

.comment-time {
  font-size: 12px;
  color: #909399;
}

.comment-text {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
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

  .media-grid {
    grid-template-columns: 1fr;
  }
}
</style>
