<template>
  <div class="profile-view">
    <el-card class="profile-card">
      <template #header>
        <h3>个人中心</h3>
      </template>

      <div class="profile-header">
        <el-avatar :size="80" :src="authStore.user?.avatar">
          {{ authStore.user?.name?.[0] || authStore.user?.email[0] }}
        </el-avatar>
        <div class="user-info">
          <h2>{{ authStore.user?.name || '未设置昵称' }}</h2>
          <p>{{ authStore.user?.email }}</p>
        </div>
      </div>

      <el-divider />

      <el-form
        ref="formRef"
        :model="form"
        label-width="100px"
        class="profile-form"
      >
        <el-form-item label="身高">
          <el-input-number
            v-model="form.height"
            :min="100"
            :max="250"
            :step="1"
            placeholder="请输入身高"
          />
          <span class="unit">cm</span>
        </el-form-item>

        <el-form-item label="体重">
          <el-input-number
            v-model="form.weight"
            :min="30"
            :max="200"
            :step="1"
            placeholder="请输入体重"
          />
          <span class="unit">kg</span>
        </el-form-item>

        <el-form-item label="体型">
          <el-select v-model="form.body_type" placeholder="请选择体型" style="width: 200px">
            <el-option label="苗条" value="苗条" />
            <el-option label="标准" value="标准" />
            <el-option label="丰满" value="丰满" />
          </el-select>
        </el-form-item>

        <el-form-item label="肤色">
          <el-select v-model="form.skin_tone" placeholder="请选择肤色" style="width: 200px">
            <el-option label="白皙" value="白皙" />
            <el-option label="小麦" value="小麦" />
            <el-option label="健康" value="健康" />
            <el-option label="深色" value="深色" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSave">
            保存
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { userApi } from '@/api'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const loading = ref(false)

const form = reactive({
  height: undefined as number | undefined,
  weight: undefined as number | undefined,
  body_type: '',
  skin_tone: ''
})

async function loadProfile() {
  try {
    const response = await userApi.getMe()
    form.height = response.data.height || undefined
    form.weight = response.data.weight || undefined
    form.body_type = response.data.body_type || ''
    form.skin_tone = response.data.skin_tone || ''
  } catch (error) {
    console.error('加载用户信息失败:', error)
  }
}

async function handleSave() {
  loading.value = true
  try {
    await userApi.updateMe(form)
    await authStore.init()
    ElMessage.success('保存成功')
  } catch {
    ElMessage.error('保存失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (authStore.user) {
    form.height = authStore.user.height || undefined
    form.weight = authStore.user.weight || undefined
    form.body_type = authStore.user.body_type || ''
    form.skin_tone = authStore.user.skin_tone || ''
  }
  loadProfile()
})
</script>

<style scoped>
.profile-view {
  max-width: 600px;
  margin: 0 auto;
}

.profile-card h3 {
  margin: 0;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px 0;
}

.user-info h2 {
  margin: 0 0 4px;
  font-size: 20px;
}

.user-info p {
  margin: 0;
  color: #909399;
}

.profile-form {
  margin-top: 20px;
}

.unit {
  margin-left: 8px;
  color: #909399;
}
</style>
