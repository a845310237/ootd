<template>
  <div class="add-clothing-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="goBack">返回</el-button>
        <h1>添加衣物</h1>
      </div>
      <div class="header-actions">
        <el-button @click="goBack">取消</el-button>
        <el-button type="primary" :loading="loading" @click="handleSave">
          保存
        </el-button>
      </div>
    </div>

    <!-- Form -->
    <div class="form-container">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        size="large"
      >
        <!-- Image Upload -->
        <el-form-item label="衣物照片" prop="imageUrl" required>
          <div class="image-upload">
            <el-upload
              class="upload-area"
              :show-file-list="false"
              :before-upload="handleImageUpload"
              accept="image/*"
              drag
            >
              <img v-if="form.imageUrl" :src="form.imageUrl" class="uploaded-image" />
              <div v-else class="upload-placeholder">
                <el-icon :size="48"><Plus /></el-icon>
                <p>点击或拖拽上传图片</p>
                <p class="upload-hint">支持 JPG、PNG、WEBP 格式，最大 10MB</p>
              </div>
            </el-upload>
          </div>
        </el-form-item>

        <!-- Basic Info -->
        <el-form-item label="衣物名称" prop="name" required>
          <el-input
            v-model="form.name"
            placeholder="例如：白色T恤"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="分类" prop="category" required>
          <el-select v-model="form.category" placeholder="选择分类" style="width: 100%">
            <el-option label="上衣" value="上衣" />
            <el-option label="裤子" value="裤子" />
            <el-option label="裙子" value="裙子" />
            <el-option label="外套" value="外套" />
            <el-option label="鞋子" value="鞋子" />
            <el-option label="配饰" value="配饰" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>

        <el-form-item label="颜色">
          <el-checkbox-group v-model="form.color">
            <el-checkbox-button label="黑色" />
            <el-checkbox-button label="白色" />
            <el-checkbox-button label="灰色" />
            <el-checkbox-button label="红色" />
            <el-checkbox-button label="蓝色" />
            <el-checkbox-button label="绿色" />
            <el-checkbox-button label="黄色" />
            <el-checkbox-button label="棕色" />
            <el-checkbox-button label="粉色" />
            <el-checkbox-button label="紫色" />
            <el-checkbox-button label="米色" />
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="风格">
          <el-checkbox-group v-model="form.style">
            <el-checkbox-button label="休闲" />
            <el-checkbox-button label="运动" />
            <el-checkbox-button label="正式" />
            <el-checkbox-button label="商务" />
            <el-checkbox-button label="复古" />
            <el-checkbox-button label="简约" />
            <el-checkbox-button label="时尚" />
            <el-checkbox-button label="街头" />
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="季节">
          <el-checkbox-group v-model="form.season">
            <el-checkbox-button label="春" />
            <el-checkbox-button label="夏" />
            <el-checkbox-button label="秋" />
            <el-checkbox-button label="冬" />
          </el-checkbox-group>
        </el-form-item>

        <el-divider>详细信息（可选）</el-divider>

        <el-form-item label="品牌">
          <el-input v-model="form.brand" placeholder="例如：优衣库" />
        </el-form-item>

        <el-form-item label="尺码">
          <el-input v-model="form.size" placeholder="例如：M、38、均码" />
        </el-form-item>

        <el-form-item label="材质">
          <el-input v-model="form.material" placeholder="例如：纯棉" />
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules, type UploadRawFile } from 'element-plus'
import { ArrowLeft, Plus } from '@element-plus/icons-vue'
import { useWardrobeStore } from '@/stores/wardrobe'
import apiClient from '@/api/client'

const router = useRouter()
const wardrobeStore = useWardrobeStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  name: '',
  category: '',
  color: [] as string[],
  style: [] as string[],
  season: [] as string[],
  brand: '',
  size: '',
  material: '',
  imageUrl: ''
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入衣物名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  imageUrl: [{ required: true, message: '请上传衣物照片', trigger: 'change' }]
}

async function handleImageUpload(file: UploadRawFile) {
  // Validate file type
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }

  // Validate file size (10MB)
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB')
    return false
  }

  // Upload image
  const formData = new FormData()
  formData.append('file', file)

  try {
    loading.value = true
    const response = await apiClient.post<{ success: boolean; url: string }>('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (response.data.success && response.data.url) {
      form.imageUrl = response.data.url
      ElMessage.success('图片上传成功')
    } else {
      ElMessage.error('图片上传失败')
    }
  } catch (error: any) {
    ElMessage.error(error.response?.data?.error || '图片上传失败')
  } finally {
    loading.value = false
  }

  return false // Prevent auto upload
}

async function handleSave() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const result = await wardrobeStore.addItem({
          name: form.name,
          category: form.category,
          color: form.color,
          style: form.style,
          season: form.season,
          brand: form.brand || undefined,
          size: form.size || undefined,
          material: form.material || undefined,
          imageUrl: form.imageUrl
        })

        if (result.success) {
          ElMessage.success('添加成功')
          goBack()
        } else {
          ElMessage.error(result.error || '添加失败')
        }
      } finally {
        loading.value = false
      }
    }
  })
}

function goBack() {
  router.push('/dashboard/wardrobe')
}
</script>

<style scoped>
.add-clothing-container {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.form-container {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.image-upload {
  width: 100%;
}

.upload-area {
  width: 100%;
}

.uploaded-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-placeholder {
  padding: 40px 20px;
  text-align: center;
}

.upload-placeholder p {
  margin: 12px 0 0 0;
  color: #606266;
}

.upload-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 4px !important;
}

:deep(.el-upload-dragger) {
  width: 100%;
  min-height: 300px;
}
</style>
