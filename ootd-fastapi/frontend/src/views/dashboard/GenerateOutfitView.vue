<template>
  <div class="generate-outfit-view">
    <el-card class="form-card">
      <template #header>
        <h3>AI 生成穿搭</h3>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <!-- Image Selection Section -->
        <el-form-item label="参考图片">
          <div class="image-selection">
            <el-radio-group v-model="imageSource" @change="handleImageSourceChange">
              <el-radio value="none">不使用参考图片</el-radio>
              <el-radio value="avatar" :disabled="!authStore.user?.avatar">使用个人头像</el-radio>
              <el-radio value="upload">上传新图片</el-radio>
            </el-radio-group>
          </div>
        </el-form-item>

        <!-- Show Avatar Preview if Selected -->
        <el-form-item v-if="imageSource === 'avatar' && authStore.user?.avatar" label="当前头像">
          <div class="avatar-preview">
            <el-image
              :src="authStore.user.avatar"
              fit="cover"
              style="width: 150px; height: 150px; border-radius: 8px;"
            />
            <p class="avatar-hint">将使用您当前的头像作为生成参考</p>
          </div>
        </el-form-item>

        <!-- Image Upload Section -->
        <el-form-item v-if="imageSource === 'upload'" label="上传图片">
          <el-upload
            class="image-uploader"
            :show-file-list="false"
            :before-upload="beforeImageUpload"
            :on-change="handleImageChange"
            accept="image/*"
            :auto-upload="false"
          >
            <img v-if="imageUrl" :src="imageUrl" class="uploaded-image" />
            <el-icon v-else class="uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="upload-tip">
            <p>支持 JPG、PNG 格式，文件大小不超过 10MB</p>
            <p v-if="uploadedFile" class="file-info">已选择: {{ uploadedFile.name }}</p>
          </div>
        </el-form-item>

        <el-form-item label="风格" prop="style">
          <el-select v-model="form.style" placeholder="请选择风格" style="width: 100%">
            <el-option label="休闲" value="休闲" />
            <el-option label="正式" value="正式" />
            <el-option label="运动" value="运动" />
            <el-option label="时尚" value="时尚" />
            <el-option label="复古" value="复古" />
            <el-option label="简约" value="简约" />
          </el-select>
        </el-form-item>

        <el-form-item label="场合" prop="occasion">
          <el-select v-model="form.occasion" placeholder="请选择场合" style="width: 100%">
            <el-option label="日常" value="日常" />
            <el-option label="工作" value="工作" />
            <el-option label="约会" value="约会" />
            <el-option label="聚会" value="聚会" />
            <el-option label="运动" value="运动" />
            <el-option label="旅行" value="旅行" />
          </el-select>
        </el-form-item>

        <el-form-item label="季节" prop="season">
          <el-select v-model="form.season" placeholder="请选择季节" style="width: 100%">
            <el-option label="春" value="春" />
            <el-option label="夏" value="夏" />
            <el-option label="秋" value="秋" />
            <el-option label="冬" value="冬" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleGenerate">
            <el-icon><MagicStick /></el-icon>
            生成穿搭
          </el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Result Dialog -->
    <el-dialog
      v-model="showResult"
      title="AI 生成结果"
      width="600px"
      :close-on-click-modal="false"
    >
      <div v-if="result" class="result-content">
        <div v-if="result.result_url" class="result-image">
          <el-image :src="result.result_url" fit="contain" />
        </div>
        <div class="result-info">
          <h4>{{ result.name }}</h4>
          <el-divider />
          <div v-if="result.reasoning" class="result-section">
            <h5>搭配理由</h5>
            <p>{{ result.reasoning }}</p>
          </div>
          <div v-if="result.tips && result.tips.length > 0" class="result-section">
            <h5>穿搭小贴士</h5>
            <ul>
              <li v-for="(tip, index) in result.tips" :key="index">{{ tip }}</li>
            </ul>
          </div>
        </div>
      </div>
      <div v-else class="no-result">
        <el-empty description="生成失败，请稍后重试" />
      </div>
      <template #footer>
        <el-button @click="showResult = false">关闭</el-button>
        <el-button type="primary" @click="handleViewResult">查看详情</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { outfitApi, uploadApi } from '@/api'
import type { Outfit } from '@/api/client'
import { ElMessage, type FormInstance, type FormRules, type UploadFile } from 'element-plus'
import { MagicStick, Plus } from '@element-plus/icons-vue'
import type { AxiosProgressEvent } from 'axios'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const showResult = ref(false)
const result = ref<Outfit | null>(null)

// Image handling
const imageSource = ref<'none' | 'avatar' | 'upload'>('none')
const uploadedFile = ref<File | null>(null)
const imageUrl = ref('')
const uploadedImageUrl = ref('')

const form = reactive({
  style: '',
  occasion: '',
  season: ''
})

const rules: FormRules = {
  style: [{ required: true, message: '请选择风格', trigger: 'change' }],
  occasion: [{ required: true, message: '请选择场合', trigger: 'change' }],
  season: [{ required: true, message: '请选择季节', trigger: 'change' }]
}

function handleImageSourceChange(value: 'none' | 'avatar' | 'upload') {
  imageSource.value = value
  if (value !== 'upload') {
    uploadedFile.value = null
    imageUrl.value = ''
    uploadedImageUrl.value = ''
  }
}

function beforeImageUpload(file: File) {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB!')
    return false
  }
  return true
}

function handleImageChange(file: UploadFile) {
  if (file.raw) {
    uploadedFile.value = file.raw
    imageUrl.value = URL.createObjectURL(file.raw)
  }
}

async function uploadReferenceImage() {
  if (imageSource.value === 'upload' && uploadedFile.value) {
    try {
      loading.value = true
      const response = await uploadApi.uploadImage(uploadedFile.value)
      uploadedImageUrl.value = response.data.url
      ElMessage.success('图片上传成功')
      return response.data.url
    } catch (error) {
      ElMessage.error('图片上传失败')
      return null
    }
  } else if (imageSource.value === 'avatar' && authStore.user?.avatar) {
    return authStore.user.avatar
  }
  return null
}

async function handleGenerate() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    // Handle avatar radio being selected but no avatar available
    if (imageSource.value === 'avatar' && !authStore.user?.avatar) {
      ElMessage.warning('您还没有设置个人头像，请先上传头像或选择其他选项')
      return
    }

    loading.value = true
    try {
      // Upload image if needed
      const refImageUrl = await uploadReferenceImage()

      const requestData = {
        ...form,
        reference_image: refImageUrl
      }

      const response = await outfitApi.generate(requestData)
      result.value = response.data
      showResult.value = true
      ElMessage.success('生成成功')
    } catch {
      ElMessage.error('生成失败，请稍后重试')
    } finally {
      loading.value = false
    }
  })
}

function handleViewResult() {
  showResult.value = false
  if (result.value) {
    router.push(`/dashboard/outfits`)
  }
}
</script>

<style scoped>
.generate-outfit-view {
  max-width: 600px;
  margin: 0 auto;
}

.form-card {
  margin-top: 24px;
}

.form-card h3 {
  margin: 0;
}

.image-selection {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.avatar-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.avatar-hint {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.image-uploader {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.uploaded-image {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  object-fit: cover;
}

.uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 200px;
  height: 200px;
  text-align: center;
  line-height: 200px;
  border: 1px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.3s;
}

.uploader-icon:hover {
  border-color: #409eff;
}

.upload-tip {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.upload-tip p {
  margin: 4px 0;
}

.file-info {
  color: #67c23a;
  font-weight: 500;
}

.result-content {
  text-align: center;
}

.result-image {
  margin-bottom: 20px;
}

.result-image :deep(.el-image) {
  max-height: 400px;
}

.result-info {
  text-align: left;
}

.result-info h4 {
  margin: 0 0 16px;
  font-size: 18px;
}

.result-section {
  margin-top: 16px;
}

.result-section h5 {
  margin: 0 0 8px;
  font-size: 14px;
  font-weight: 500;
}

.result-section p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}

.result-section ul {
  margin: 0;
  padding-left: 20px;
}

.result-section li {
  color: #606266;
  line-height: 1.8;
}

.no-result {
  text-align: center;
}
</style>
