<template>
  <div class="create-outfit-view">
    <el-card class="form-card">
      <template #header>
        <h3>创建穿搭</h3>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="穿搭名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入穿搭名称" />
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

        <el-form-item label="选择衣物" prop="clothing_ids" required>
          <el-select
            v-model="form.clothing_ids"
            multiple
            placeholder="请选择衣物"
            style="width: 100%"
          >
            <el-option
              v-for="item in clothingOptions"
              :key="item.id"
              :label="`${item.name} - ${item.category}`"
              :value="item.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            创建穿搭
          </el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { clothingApi, outfitApi } from '@/api'
import type { Clothing } from '@/api/client'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const clothingOptions = ref<Clothing[]>([])

const form = reactive({
  name: '',
  style: '',
  occasion: '',
  season: '',
  clothing_ids: [] as string[]
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入穿搭名称', trigger: 'blur' }],
  style: [{ required: true, message: '请选择风格', trigger: 'change' }],
  clothing_ids: [
    { required: true, message: '请至少选择一件衣物', trigger: 'change' }
  ]
}

async function loadClothing() {
  try {
    const response = await clothingApi.getList()
    clothingOptions.value = response.data
  } catch (error) {
    console.error('加载衣物失败:', error)
  }
}

async function handleSubmit() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await outfitApi.create(form)
      ElMessage.success('创建成功')
      router.push('/dashboard/outfits')
    } catch {
      ElMessage.error('创建失败')
    } finally {
      loading.value = false
    }
  })
}

onMounted(() => {
  loadClothing()
})
</script>

<style scoped>
.create-outfit-view {
  max-width: 600px;
  margin: 0 auto;
}

.form-card {
  margin-top: 24px;
}

.form-card h3 {
  margin: 0;
}
</style>
