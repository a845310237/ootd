<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">穿搭AI</h1>
        <p class="hero-subtitle">智能穿搭推荐，让每一天都精彩</p>
        <p class="hero-description">
          基于AI技术，根据您的身材特点、风格偏好和场合需求，为您推荐最合适的穿搭组合
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="goToLogin">
            立即开始
          </el-button>
          <el-button size="large" @click="learnMore">
            了解更多
          </el-button>
        </div>
      </div>
    </div>

    <div class="features-section">
      <div class="features-container">
        <h2 class="section-title">核心功能</h2>
        <el-row :gutter="32" class="features-grid">
          <el-col :xs="24" :sm="8">
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon :size="40"><Camera /></el-icon>
              </div>
              <h3>智能衣柜</h3>
              <p>数字化管理您的衣物，支持分类、标签和图片上传</p>
            </div>
          </el-col>
          <el-col :xs="24" :sm="8">
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon :size="40"><MagicStick /></el-icon>
              </div>
              <h3>AI搭配推荐</h3>
              <p>基于通义万相AI，根据需求自动生成穿搭建议</p>
            </div>
          </el-col>
          <el-col :xs="24" :sm="8">
            <div class="feature-card">
              <div class="feature-icon">
                <el-icon :size="40"><Edit /></el-icon>
              </div>
              <h3>DIY搭配</h3>
              <p>自由组合衣物，创建专属您的个性化穿搭</p>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>

    <footer class="home-footer">
      <p>&copy; 2024 穿搭AI. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Camera, MagicStick, Edit } from '@element-plus/icons-vue'

const router = useRouter()

function goToLogin() {
  router.push('/auth/login')
}

function learnMore() {
  // Could scroll to features or show a modal
  document.querySelector('.features-section')?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  padding: 60px 20px;
}

.hero-content {
  max-width: 800px;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 24px;
  margin-bottom: 16px;
  opacity: 0.95;
}

.hero-description {
  font-size: 16px;
  margin-bottom: 32px;
  opacity: 0.9;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.features-section {
  padding: 80px 20px;
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 32px;
  font-weight: 600;
  color: #333;
  margin-bottom: 48px;
}

.features-grid {
  margin-top: 32px;
}

.feature-card {
  text-align: center;
  padding: 32px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-bottom: 16px;
}

.feature-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.feature-card p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.home-footer {
  text-align: center;
  padding: 32px 20px;
  background: #fff;
  color: #999;
  font-size: 14px;
}
</style>
