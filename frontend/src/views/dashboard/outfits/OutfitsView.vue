<template>
  <div class="outfits-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1>我的搭配</h1>
        <p>管理和查看您的穿搭搭配</p>
      </div>
      <div class="header-actions">
        <el-button :icon="MagicStick" @click="goToGenerate">
          AI生成
        </el-button>
        <el-button type="primary" :icon="Plus" @click="goToDIY">
          DIY搭配
        </el-button>
      </div>
    </div>

    <!-- Tabs -->
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="全部" name="all" />
      <el-tab-pane label="AI生成" name="ai" />
      <el-tab-pane label="手动创建" name="manual" />
    </el-tabs>

    <!-- Loading State -->
    <div v-if="loading && items.length === 0" class="loading-state">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- Empty State -->
    <div v-else-if="items.length === 0" class="empty-state">
      <el-empty :description="emptyText">
        <el-button type="primary" @click="goToGenerate">
          创建第一个搭配
        </el-button>
      </el-empty>
    </div>

    <!-- Outfits Grid -->
    <div v-else class="outfits-grid">
      <div
        v-for="outfit in items"
        :key="outfit.id"
        class="outfit-card"
        @click="viewOutfit(outfit)"
      >
        <div class="outfit-preview">
          <div class="outfit-images">
            <img
              v-for="(item, index) in outfit.items?.slice(0, 4)"
              :key="index"
              :src="item.imageUrl"
              :alt="item.name"
            />
          </div>
          <div v-if="outfit.aiGenerated" class="ai-badge">
            <el-icon><MagicStick /></el-icon>
            AI
          </div>
        </div>
        <div class="outfit-info">
          <h3>{{ outfit.name }}</h3>
          <p class="outfit-meta">
            {{ outfit.style }}
            <span v-if="outfit.occasion"> · {{ outfit.occasion }}</span>
            <span v-if="outfit.season"> · {{ outfit.season }}</span>
          </p>
          <p class="outfit-count">{{ outfit.items?.length || 0 }} 件单品</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, MagicStick } from '@element-plus/icons-vue'
import { useOutfitsStore } from '@/stores/outfits'
import type { Outfit } from '@/api/client'

const router = useRouter()
const outfitsStore = useOutfitsStore()

const activeTab = ref('all')
const loading = ref(false)

const items = computed(() => {
  let filtered = outfitsStore.items

  if (activeTab.value === 'ai') {
    filtered = outfitsStore.aiGeneratedOutfits
  } else if (activeTab.value === 'manual') {
    filtered = outfitsStore.manualOutfits
  }

  return filtered
})

const emptyText = computed(() => {
  if (activeTab.value === 'ai') return '还没有AI生成的搭配'
  if (activeTab.value === 'manual') return '还没有手动创建的搭配'
  return '还没有任何搭配'
})

onMounted(async () => {
  loading.value = true
  await outfitsStore.fetchOutfits()
  loading.value = false
})

function handleTabChange() {
  // Tab change is handled by computed property
}

function goToGenerate() {
  router.push('/dashboard/outfits/generate')
}

function goToDIY() {
  router.push('/dashboard/outfits/diy')
}

function viewOutfit(outfit: Outfit) {
  router.push(`/dashboard/outfits/${outfit.id}`)
}
</script>

<style scoped>
.outfits-container {
  padding: 24px;
  max-width: 1400px;
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

.header-left h1 {
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
}

.header-left p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.loading-state,
.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.outfits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.outfit-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.outfit-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.outfit-preview {
  position: relative;
  width: 100%;
  padding-top: 75%;
  background: #f5f7fa;
}

.outfit-images {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 2px;
}

.outfit-images img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ai-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.outfit-info {
  padding: 16px;
}

.outfit-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.outfit-meta {
  font-size: 13px;
  color: #666;
  margin: 0 0 4px 0;
}

.outfit-count {
  font-size: 12px;
  color: #999;
  margin: 0;
}
</style>
