<template>
  <div class="outfits-view">
    <div class="toolbar">
      <el-button type="primary" @click="$router.push('/dashboard/outfits/generate')">
        <el-icon><MagicStick /></el-icon>
        AI 生成穿搭
      </el-button>
      <el-button @click="$router.push('/dashboard/outfits/create')">
        <el-icon><Plus /></el-icon>
        创建穿搭
      </el-button>
    </div>

    <div v-loading="loading" class="outfits-grid">
      <el-empty v-if="!loading && outfitsList.length === 0" description="暂无穿搭" />

      <el-card
        v-for="item in outfitsList"
        :key="item.id"
        class="outfit-card"
        :body-style="{ padding: '0' }"
      >
        <div class="outfit-image">
          <img v-if="item.result_url" :src="item.result_url" :alt="item.name" />
          <div v-else class="outfit-placeholder">
            <el-icon :size="48"><ShoppingBag /></el-icon>
          </div>
          <el-tag v-if="item.ai_generated" class="ai-badge" type="success">
            AI 生成
          </el-tag>
        </div>
        <div class="outfit-info">
          <h4 class="outfit-name">{{ item.name }}</h4>
          <p class="outfit-style">{{ item.style }}</p>
          <div class="outfit-meta">
            <el-tag size="small" type="info">{{ item.occasion || '日常' }}</el-tag>
            <el-tag size="small" type="info">{{ item.season || '四季' }}</el-tag>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { outfitApi } from '@/api'
import type { Outfit } from '@/api/client'
import { MagicStick, Plus, ShoppingBag } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const outfitsList = ref<Outfit[]>([])

async function loadOutfits() {
  loading.value = true
  try {
    const response = await outfitApi.getList()
    outfitsList.value = response.data
  } catch (error) {
    ElMessage.error('加载穿搭失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadOutfits()
})
</script>

<style scoped>
.outfits-view {
  max-width: 1200px;
  margin: 0 auto;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.outfits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.outfit-card {
  transition: transform 0.3s, box-shadow 0.3s;
  overflow: hidden;
}

.outfit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.outfit-image {
  position: relative;
  width: 100%;
  height: 250px;
  overflow: hidden;
  background: #f5f7fa;
}

.outfit-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.outfit-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #c0c4cc;
}

.ai-badge {
  position: absolute;
  top: 8px;
  right: 8px;
}

.outfit-info {
  padding: 12px;
}

.outfit-name {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.outfit-style {
  margin: 0 0 8px;
  font-size: 12px;
  color: #909399;
}

.outfit-meta {
  display: flex;
  gap: 4px;
}
</style>
