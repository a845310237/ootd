<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>注册账号</h1>
        <p>开始您的智能穿搭之旅</p>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        size="large"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="form.email"
            type="email"
            placeholder="请输入邮箱"
            :prefix-icon="Message"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码（至少6位）"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="handleRegister"
          />
        </el-form-item>

        <el-form-item label="昵称（可选）" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入昵称"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-divider>身体信息（可稍后完善）</el-divider>

        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="身高（cm）" prop="height">
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
            <el-form-item label="体重（kg）" prop="weight">
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
            <el-form-item label="体型" prop="bodyType">
              <el-select v-model="form.bodyType" placeholder="选择体型" style="width: 100%">
                <el-option label="苗条" value="苗条" />
                <el-option label="标准" value="标准" />
                <el-option label="丰满" value="丰满" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="肤色" prop="skinTone">
              <el-select v-model="form.skinTone" placeholder="选择肤色" style="width: 100%">
                <el-option label="白皙" value="白皙" />
                <el-option label="中性" value="中性" />
                <el-option label="偏黑" value="偏黑" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button
            type="primary"
            :loading="authStore.loading"
            style="width: 100%"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>

        <div class="auth-footer">
          <span>已有账号？</span>
          <el-link type="primary" @click="goToLogin">立即登录</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Message, Lock, User } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref<FormInstance>()
const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  name: '',
  height: null as number | null,
  weight: null as number | null,
  bodyType: '',
  skinTone: ''
})

const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

async function handleRegister() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      const result = await authStore.register({
        email: form.email,
        password: form.password,
        name: form.name || undefined,
        height: form.height || undefined,
        weight: form.weight || undefined,
        bodyType: form.bodyType || undefined,
        skinTone: form.skinTone || undefined
      })

      if (result.success) {
        ElMessage.success('注册成功，请登录')
        router.push('/auth/login')
      } else {
        ElMessage.error(result.error || '注册失败')
      }
    }
  })
}

function goToLogin() {
  router.push('/auth/login')
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  overflow-y: auto;
}

.auth-card {
  width: 100%;
  max-width: 480px;
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.auth-header p {
  font-size: 14px;
  color: #666;
}

.auth-footer {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #666;
}

.auth-footer .el-link {
  margin-left: 8px;
}
</style>
