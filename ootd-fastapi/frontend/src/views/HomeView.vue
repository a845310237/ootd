<template>
  <div class="home-container">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1 class="logo">穿搭AI</h1>
          <nav class="nav">
            <router-link to="/" class="nav-link">首页</router-link>
            <template v-if="authStore.isAuthenticated">
              <router-link to="/dashboard/wardrobe" class="nav-link">衣柜</router-link>
              <router-link to="/dashboard/outfits" class="nav-link">穿搭</router-link>
              <router-link to="/dashboard/profile" class="nav-link">个人中心</router-link>
              <el-button @click="handleLogout" type="primary" plain>退出</el-button>
            </template>
            <template v-else>
              <router-link to="/login" class="nav-link">登录</router-link>
              <el-button type="primary" @click="$router.push('/register')">注册</el-button>
            </template>
          </nav>
        </div>
      </el-header>

      <el-main class="main">
        <div class="hero">
          <h1 class="hero-title">智能穿搭助手</h1>
          <p class="hero-subtitle">AI 为你打造个性化穿搭方案</p>

          <div class="features">
            <el-card class="feature-card">
              <el-icon :size="40"><ShoppingBag /></el-icon>
              <h3>衣物管理</h3>
              <p>数字化你的衣物，轻松管理每一件单品</p>
            </el-card>

            <el-card class="feature-card">
              <el-icon :size="40"><MagicStick /></el-icon>
              <h3>AI 智能搭配</h3>
              <p>基于你的身材特征和场合需求，AI 生成专属穿搭建议</p>
            </el-card>

            <el-card class="feature-card">
              <el-icon :size="40"><Edit /></el-icon>
              <h3>DIY 穿搭</h3>
              <p>自由组合衣物，创建属于你的独特风格</p>
            </el-card>
          </div>

          <div class="cta">
            <el-button
              v-if="!authStore.isAuthenticated"
              type="primary"
              size="large"
              @click="$router.push('/register')"
            >
              开始使用
            </el-button>
            <el-button
              v-else
              type="primary"
              size="large"
              @click="$router.push('/dashboard/wardrobe')"
            >
              进入我的衣柜
            </el-button>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ShoppingBag, MagicStick, Edit } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 20px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin: 0;
}

.nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: #606266;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #409eff;
}

.main {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.hero {
  text-align: center;
  max-width: 800px;
}

.hero-title {
  font-size: 48px;
  margin-bottom: 16px;
  color: #303133;
}

.hero-subtitle {
  font-size: 20px;
  color: #606266;
  margin-bottom: 60px;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 60px;
}

.feature-card {
  text-align: center;
  padding: 30px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.feature-card h3 {
  margin: 16px 0 8px;
  color: #303133;
}

.feature-card p {
  color: #909399;
  margin: 0;
}

.cta {
  margin-top: 40px;
}
</style>
