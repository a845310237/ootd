<template>
  <div class="add-clothing-view">
    <el-card class="form-card">
      <template #header>
        <h3>添加衣物</h3>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="衣物名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入衣物名称" />
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="上衣" value="上衣" />
            <el-option label="裤子" value="裤子" />
            <el-option label="裙子" value="裙子" />
            <el-option label="鞋子" value="鞋子" />
            <el-option label="配饰" value="配饰" />
          </el-select>
        </el-form-item>

        <el-form-item label="颜色" prop="color">
          <el-select
            v-model="form.color"
            multiple
            placeholder="请选择颜色"
            style="width: 100%"
          >
            <el-option label="黑色" value="黑色" />
            <el-option label="白色" value="白色" />
            <el-option label="灰色" value="灰色" />
            <el-option label="红色" value="红色" />
            <el-option label="蓝色" value="蓝色" />
            <el-option label="绿色" value="绿色" />
            <el-option label="黄色" value="黄色" />
            <el-option label="棕色" value="棕色" />
            <el-option label="粉色" value="粉色" />
            <el-option label="紫色" value="紫色" />
          </el-select>
        </el-form-item>

        <el-form-item label="风格" prop="style">
          <el-select
            v-model="form.style"
            multiple
            placeholder="请选择风格"
            style="width: 100%"
          >
            <el-option label="休闲" value="休闲" />
            <el-option label="正式" value="正式" />
            <el-option label="运动" value="运动" />
            <el-option label="时尚" value="时尚" />
            <el-option label="复古" value="复古" />
            <el-option label="简约" value="简约" />
          </el-select>
        </el-form-item>

        <el-form-item label="季节" prop="season">
          <el-select
            v-model="form.season"
            multiple
            placeholder="请选择季节"
            style="width: 100%"
          >
            <el-option label="春" value="春" />
            <el-option label="夏" value="夏" />
            <el-option label="秋" value="秋" />
            <el-option label="冬" value="冬" />
          </el-select>
        </el-form-item>

        <el-form-item label="品牌" prop="brand">
          <el-input v-model="form.brand" placeholder="请输入品牌（可选）" />
        </el-form-item>

        <el-form-item label="尺码" prop="size">
          <el-input v-model="form.size" placeholder="请输入尺码（可选）" />
        </el-form-item>

        <el-form-item label="材质" prop="material">
          <el-input v-model="form.material" placeholder="请输入材质（可选）" />
        </el-form-item>

        <el-form-item label="图片" prop="image_url" required>
          <el-upload
            class="upload-demo"
            :action="uploadAction"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <el-button type="primary">
              <el-icon><Upload /></el-icon>
              上传图片
            </el-button>
          </el-upload>
          <div v-if="form.image_url" class="image-preview">
            <el-image
              :src="form.image_url"
              fit="cover"
              style="width: 200px; height: 200px"
            />
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            添加衣物
          </el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { clothingApi } from '@/api'
import { ElMessage, type FormInstance, type FormRules, type UploadProps } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'

const router = useRouter()
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
  image_url: ''
})

const uploadAction = '/api/upload/image'
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${localStorage.getItem('access_token')}`
}))

const rules: FormRules = {
  name: [{ required: true, message: '请输入衣物名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  image_url: [{ required: true, message: '请上传图片', trigger: 'change' }]
}

const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB')
    return false
  }
  return true
}

function handleUploadSuccess(response: any) {
  form.image_url = response.url
  ElMessage.success('图片上传成功')
}

async function handleSubmit() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await clothingApi.create(form)
      ElMessage.success('添加成功')
      router.push('/dashboard/wardrobe')
    } catch {
      ElMessage.error('添加失败')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.add-clothing-view {
  max-width: 600px;
  margin: 0 auto;
}

.form-card {
  margin-top: 24px;
}

.form-card h3 {
  margin: 0;
}

.image-preview {
  margin-top: 12px;
  display: flex;
  justify-content: center;
}
</style>
