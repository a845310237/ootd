<template>
  <div class="profile-container">
    <div class="page-header">
      <h1>个人资料</h1>
      <p>完善您的身体信息，帮助我们提供更精准的穿搭建议</p>
    </div>

    <div class="content">
      <el-form
        ref="formRef"
        :model="form"
        label-width="100px"
        size="large"
        class="profile-form"
      >
        <!-- Account Info -->
        <div class="form-section">
          <h2>账号信息</h2>
          <el-form-item label="邮箱">
            <el-input v-model="authStore.user!.email" disabled />
          </el-form-item>
          <el-form-item label="昵称">
            <el-input v-model="form.name" placeholder="请输入昵称" maxlength="30" />
          </el-form-item>
        </div>

        <!-- Body Info -->
        <div class="form-section">
          <h2>身体信息</h2>
          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item label="身高 (cm)">
                <el-input-number
                  v-model="form.height"
                  :min="100"
                  :max="250"
                  placeholder="身高"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="体重 (kg)">
                <el-input-number
                  v-model="form.weight"
                  :min="30"
                  :max="200"
                  placeholder="体重"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item label="体型">
                <el-select v-model="form.bodyType" placeholder="选择体型" style="width: 100%">
                  <el-option label="苗条" value="苗条" />
                  <el-option label="标准" value="标准" />
                  <el-option label="丰满" value="丰满" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="肤色">
                <el-select v-model="form.skinTone" placeholder="选择肤色" style="width: 100%">
                  <el-option label="白皙" value="白皙" />
                  <el-option label="中性" value="中性" />
                  <el-option label="偏黑" value="偏黑" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- Avatar -->
        <div class="form-section">
          <h2>头像</h2>
          <el-form-item label="头像">
            <el-upload
              class="avatar-uploader"
              :show-file-list="false"
              :before-upload="handleAvatarUpload"
              accept="image/*"
            >
              <img v-if="form.avatar" :src="form.avatar" class="avatar" />
              <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
          </el-form-item>
        </div>

        <!-- Actions -->
        <div class="form-actions">
          <el-button @click="handleReset">重置</el-button>
          <el-button type="primary" :loading="loading" @click="handleSave">
            保存
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type UploadRawFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import apiClient from '@/api/client'

const authStore = useAuthStore()
const userStore = useUserStore()

const loading = ref(false)

const form = reactive({
  name: '',
  height: null as number | null,
  weight: null as number | null,
  bodyType: '',
  skinTone: '',
  avatar: ''
})

onMounted(async () => {
  // Initialize form with auth store user data
  if (authStore.user) {
    form.name = authStore.user.name || ''
    form.height = authStore.user.height || null
    form.weight = authStore.user.weight || null
    form.bodyType = authStore.user.bodyType || ''
    form.skinTone = authStore.user.skinTone || ''
    form.avatar = authStore.user.avatar || ''
  }
})

async function handleAvatarUpload(file: UploadRawFile) {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }

  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }

  const formData = new FormData()
  formData.append('file', file)

  try {
    loading.value = true
    const response = await apiClient.post<{ success: boolean; url: string }>('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (response.data.success && response.data.url) {
      form.avatar = response.data.url
      ElMessage.success('头像上传成功')
    }
  } catch (error: any) {
    ElMessage.error(error.response?.data?.error || '头像上传失败')
  } finally {
    loading.value = false
  }

  return false
}

async function handleSave() {
  loading.value = true
  try {
    const result = await userStore.updateProfile({
      name: form.name || undefined,
      height: form.height || undefined,
      weight: form.weight || undefined,
      bodyType: form.bodyType || undefined,
      skinTone: form.skinTone || undefined,
      avatar: form.avatar || undefined
    })

    if (result.success) {
      ElMessage.success('保存成功')
      // Update auth store user
      await authStore.fetchCurrentUser()
    } else {
      ElMessage.error(result.error || '保存失败')
    }
  } finally {
    loading.value = false
  }
}

function handleReset() {
  if (authStore.user) {
    form.name = authStore.user.name || ''
    form.height = authStore.user.height || null
    form.weight = authStore.user.weight || null
    form.bodyType = authStore.user.bodyType || ''
    form.skinTone = authStore.user.skinTone || ''
    form.avatar = authStore.user.avatar || ''
  }
}
</script>

<style scoped>
.profile-container {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
}

.page-header p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.content {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.form-section {
  margin-bottom: 32px;
}

.form-section:last-of-type {
  margin-bottom: 24px;
}

.form-section h2 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.avatar-uploader {
  display: inline-block;
}

.avatar-uploader .avatar {
  width: 120px;
  height: 120px;
  display: block;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-uploader :deep(.el-upload) {
  width: 120px;
  height: 120px;
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.avatar-uploader :deep(.el-upload:hover) {
  border-color: #667eea;
}

.avatar-uploader-icon {
  width: 120px;
  height: 120px;
  font-size: 28px;
  color: #8c939d;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #eee;
}
</style>
