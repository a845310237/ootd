<template>
  <div class="wardrobe-view">
    <div class="toolbar">
      <el-input
        v-model="searchText"
        placeholder="搜索衣物..."
        style="width: 300px"
        clearable
        @change="loadClothing"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="selectedCategory"
        placeholder="选择分类"
        clearable
        style="width: 150px"
        @change="loadClothing"
      >
        <el-option label="全部" value="" />
        <el-option label="上衣" value="上衣" />
        <el-option label="裤子" value="裤子" />
        <el-option label="裙子" value="裙子" />
        <el-option label="鞋子" value="鞋子" />
        <el-option label="配饰" value="配饰" />
      </el-select>

      <el-button type="primary" @click="$router.push('/dashboard/wardrobe/add')">
        <el-icon><Plus /></el-icon>
        添加衣物
      </el-button>
    </div>

    <div v-loading="loading" class="clothing-grid">
      <el-empty v-if="!loading && clothingList.length === 0" description="暂无衣物" />

      <el-card
        v-for="item in clothingList"
        :key="item.id"
        class="clothing-card"
        :body-style="{ padding: '0' }"
      >
        <div class="clothing-image">
          <img :src="item.image_url" :alt="item.name" />
        </div>
        <div class="clothing-info">
          <h4 class="clothing-name">{{ item.name }}</h4>
          <p class="clothing-category">{{ item.category }}</p>
          <div class="clothing-tags">
            <el-tag
              v-for="color in item.color?.slice(0, 2)"
              :key="color"
              size="small"
              type="info"
            >
              {{ color }}
            </el-tag>
            <el-tag
              v-for="style in item.style?.slice(0, 1)"
              :key="style"
              size="small"
            >
              {{ style }}
            </el-tag>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { clothingApi } from '@/api'
import type { Clothing } from '@/api/client'
import { Search, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const clothingList = ref<Clothing[]>([])
const searchText = ref('')
const selectedCategory = ref('')

async function loadClothing() {
  loading.value = true
  try {
    const params: { category?: string; search?: string } = {}
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    if (searchText.value) {
      params.search = searchText.value
    }

    const response = await clothingApi.getList(params)
    clothingList.value = response.data
  } catch (error) {
    ElMessage.error('加载衣物失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadClothing()
})
</script>

<style scoped>
.wardrobe-view {
  max-width: 1200px;
  margin: 0 auto;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.clothing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.clothing-card {
  transition: transform 0.3s, box-shadow 0.3s;
  overflow: hidden;
}

.clothing-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.clothing-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f5f7fa;
}

.clothing-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.clothing-info {
  padding: 12px;
}

.clothing-name {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.clothing-category {
  margin: 0 0 8px;
  font-size: 12px;
  color: #909399;
}

.clothing-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>
