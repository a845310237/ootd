<template>
  <div class="wardrobe-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1>我的衣柜</h1>
        <p>管理您的衣物</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" :icon="Plus" @click="goToAdd">
          添加衣物
        </el-button>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <el-radio-group v-model="selectedCategory" @change="handleCategoryChange">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button
          v-for="category in wardrobeStore.categories"
          :key="category"
          :label="category"
        >
          {{ category }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <!-- Loading State -->
    <div v-if="wardrobeStore.loading && wardrobeStore.items.length === 0" class="loading-state">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredItems.length === 0" class="empty-state">
      <el-empty description="还没有添加衣物">
        <el-button type="primary" @click="goToAdd">添加第一件衣物</el-button>
      </el-empty>
    </div>

    <!-- Clothing Grid -->
    <div v-else class="clothing-grid">
      <div
        v-for="item in filteredItems"
        :key="item.id"
        class="clothing-card"
        @click="viewItem(item)"
      >
        <div class="clothing-image">
          <img :src="item.imageUrl" :alt="item.name" />
          <div class="clothing-overlay">
            <el-button
              type="primary"
              size="small"
              :icon="Edit"
              @click.stop="editItem(item)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              @click.stop="confirmDelete(item)"
            >
              删除
            </el-button>
          </div>
        </div>
        <div class="clothing-info">
          <h3>{{ item.name }}</h3>
          <p class="category">{{ item.category }}</p>
          <div class="tags">
            <el-tag
              v-for="color in item.color"
              :key="color"
              size="small"
              type="info"
            >
              {{ color }}
            </el-tag>
            <el-tag
              v-for="style in item.style"
              :key="style"
              size="small"
            >
              {{ style }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { useWardrobeStore } from '@/stores/wardrobe'
import type { Clothing } from '@/api/client'

const router = useRouter()
const wardrobeStore = useWardrobeStore()

const selectedCategory = ref('')

const filteredItems = computed(() => {
  if (!selectedCategory.value) {
    return wardrobeStore.items
  }
  return wardrobeStore.items.filter(item => item.category === selectedCategory.value)
})

onMounted(async () => {
  await wardrobeStore.fetchItems()
})

function handleCategoryChange() {
  wardrobeStore.setCategory(selectedCategory.value || null)
}

function goToAdd() {
  router.push('/dashboard/wardrobe/add')
}

function viewItem(item: Clothing) {
  // Could show a detail dialog
  router.push(`/dashboard/wardrobe/edit/${item.id}`)
}

function editItem(item: Clothing) {
  router.push(`/dashboard/wardrobe/edit/${item.id}`)
}

async function confirmDelete(item: Clothing) {
  try {
    await ElMessageBox.confirm(
      `确定要删除 "${item.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const result = await wardrobeStore.deleteItem(item.id)
    if (result.success) {
      ElMessage.success('删除成功')
    } else {
      ElMessage.error(result.error || '删除失败')
    }
  } catch {
    // User cancelled
  }
}
</script>

<style scoped>
.wardrobe-container {
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

.filters-bar {
  margin-bottom: 24px;
  overflow-x: auto;
}

.loading-state,
.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.clothing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.clothing-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.clothing-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.clothing-image {
  position: relative;
  width: 100%;
  padding-top: 100%; /* Square aspect ratio */
  overflow: hidden;
  background: #f5f7fa;
}

.clothing-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.clothing-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}

.clothing-card:hover .clothing-overlay {
  opacity: 1;
}

.clothing-info {
  padding: 16px;
}

.clothing-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.clothing-info .category {
  font-size: 12px;
  color: #999;
  margin: 0 0 8px 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>
