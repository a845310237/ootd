<template>
  <div class="outfit-detail-container">
    <!-- Loading -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <!-- Not Found -->
    <div v-else-if="!outfit" class="error-container">
      <el-empty description="搭配不存在">
        <el-button @click="goBack">返回</el-button>
      </el-empty>
    </div>

    <!-- Detail -->
    <div v-else class="content">
      <!-- Header -->
      <div class="page-header">
        <div class="header-left">
          <el-button :icon="ArrowLeft" @click="goBack">返回</el-button>
          <div>
            <h1>{{ outfit.name }}</h1>
            <p class="outfit-meta">
              {{ outfit.style }}
              <span v-if="outfit.occasion"> · {{ outfit.occasion }}</span>
              <span v-if="outfit.season"> · {{ outfit.season }}</span>
              <el-tag v-if="outfit.aiGenerated" size="small" type="success" style="margin-left: 8px">
                <el-icon><MagicStick /></el-icon>
                AI生成
              </el-tag>
            </p>
          </div>
        </div>
        <div class="header-actions">
          <el-button
            type="danger"
            :icon="Delete"
            @click="confirmDelete"
          >
            删除
          </el-button>
        </div>
      </div>

      <!-- Items Grid -->
      <div class="items-section">
        <h2>搭配单品 ({{ outfit.items?.length || 0 }})</h2>
        <div class="items-grid">
          <div
            v-for="item in outfit.items"
            :key="item.id"
            class="item-card"
          >
            <img :src="item.imageUrl" :alt="item.name" />
            <div class="item-info">
              <p class="item-name">{{ item.name }}</p>
              <p class="item-category">{{ item.category }}</p>
              <div class="item-tags">
                <el-tag
                  v-for="color in item.color"
                  :key="color"
                  size="small"
                  type="info"
                >
                  {{ color }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI Info -->
      <div v-if="outfit.aiGenerated && (outfit.reasoning || outfit.tips?.length)" class="ai-info">
        <div v-if="outfit.reasoning" class="reasoning">
          <h3>搭配理由</h3>
          <p>{{ outfit.reasoning }}</p>
        </div>

        <div v-if="outfit.tips?.length" class="tips">
          <h3>穿搭小贴士</h3>
          <ul>
            <li v-for="(tip, index) in outfit.tips" :key="index">
              {{ tip }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Delete, MagicStick } from '@element-plus/icons-vue'
import { useOutfitsStore } from '@/stores/outfits'

const router = useRouter()
const route = useRoute()
const outfitsStore = useOutfitsStore()

const loading = ref(true)
const outfit = computed(() => outfitsStore.currentOutfit)

onMounted(async () => {
  const id = route.params.id as string
  const result = await outfitsStore.fetchOutfit(id)
  loading.value = false
  if (!result.success) {
    ElMessage.error(result.error || '获取搭配详情失败')
  }
})

function confirmDelete() {
  if (!outfit.value) return

  ElMessageBox.confirm(
    `确定要删除 "${outfit.value.name}" 吗？`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    const result = await outfitsStore.deleteOutfit(outfit.value!.id)
    if (result.success) {
      ElMessage.success('删除成功')
      goBack()
    } else {
      ElMessage.error(result.error || '删除失败')
    }
  }).catch(() => {
    // User cancelled
  })
}

function goBack() {
  router.push('/dashboard/outfits')
}
</script>

<style scoped>
.outfit-detail-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading-container,
.error-container {
  padding: 40px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
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
  margin: 0 0 4px 0;
}

.outfit-meta {
  font-size: 14px;
  color: #666;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 4px;
}

.items-section,
.ai-info {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
}

.items-section h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.item-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.item-card img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.item-info {
  padding: 12px;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
}

.item-category {
  font-size: 12px;
  color: #999;
  margin: 0 0 8px 0;
}

.item-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.ai-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.reasoning,
.tips {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.reasoning h3,
.tips h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.reasoning p,
.tips li {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.tips ul {
  padding-left: 20px;
}

.tips li {
  margin-bottom: 4px;
}
</style>
