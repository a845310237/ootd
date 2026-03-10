<template>
  <div class="diy-outfit-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="goBack">返回</el-button>
        <h1>DIY搭配</h1>
      </div>
      <div class="header-actions">
        <el-button @click="handleClear">清空</el-button>
        <el-button
          type="primary"
          :disabled="selectedItems.length === 0"
          @click="showSaveDialog"
        >
          保存搭配 ({{ selectedItems.length }})
        </el-button>
      </div>
    </div>

    <div class="content">
      <!-- Left: Available Clothes -->
      <div class="clothes-section">
        <h2>选择衣物</h2>

        <!-- Category Filter -->
        <el-tabs v-model="activeCategory" @tab-change="handleCategoryChange">
          <el-tab-pane label="全部" name="" />
          <el-tab-pane
            v-for="category in wardrobeStore.categories"
            :key="category"
            :label="category"
            :name="category"
          />
        </el-tabs>

        <!-- Clothes Grid -->
        <div v-if="filteredClothes.length === 0" class="empty-clothes">
          <el-empty description="没有可用的衣物" />
        </div>
        <div v-else class="clothes-grid">
          <div
            v-for="item in filteredClothes"
            :key="item.id"
            class="clothing-item"
            :class="{ selected: isSelected(item.id) }"
            @click="toggleItem(item)"
          >
            <img :src="item.imageUrl" :alt="item.name" />
            <div class="item-checkbox">
              <el-icon v-if="isSelected(item.id)"><Check /></el-icon>
            </div>
            <p class="item-name">{{ item.name }}</p>
          </div>
        </div>
      </div>

      <!-- Right: Selected Items Preview -->
      <div class="preview-section">
        <h2>已选单品</h2>

        <div v-if="selectedItems.length === 0" class="empty-selection">
          <el-empty description="请从左侧选择衣物">
            <p class="hint">可以自由组合不同类别的衣物创建搭配</p>
          </el-empty>
        </div>

        <div v-else class="selected-items">
          <div
            v-for="item in selectedItems"
            :key="item.id"
            class="selected-item"
          >
            <img :src="item.imageUrl" :alt="item.name" />
            <div class="item-details">
              <p class="item-name">{{ item.name }}</p>
              <p class="item-meta">{{ item.category }}</p>
            </div>
            <el-button
              type="danger"
              size="small"
              :icon="Close"
              circle
              @click="removeItem(item.id)"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Save Dialog -->
    <el-dialog
      v-model="saveDialogVisible"
      title="保存搭配"
      width="500px"
    >
      <el-form
        ref="saveFormRef"
        :model="saveForm"
        :rules="saveRules"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input
            v-model="saveForm.name"
            placeholder="给这个搭配起个名字"
            maxlength="30"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="风格" prop="style">
          <el-input v-model="saveForm.style" placeholder="例如：休闲、正式" />
        </el-form-item>

        <el-form-item label="场合">
          <el-select v-model="saveForm.occasion" placeholder="选择场合" style="width: 100%">
            <el-option label="日常" value="日常" />
            <el-option label="工作" value="工作" />
            <el-option label="约会" value="约会" />
            <el-option label="运动" value="运动" />
            <el-option label="聚会" value="聚会" />
            <el-option label="正式场合" value="正式场合" />
          </el-select>
        </el-form-item>

        <el-form-item label="季节">
          <el-select v-model="saveForm.season" placeholder="选择季节" style="width: 100%">
            <el-option label="春" value="春" />
            <el-option label="夏" value="夏" />
            <el-option label="秋" value="秋" />
            <el-option label="冬" value="冬" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="saveDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { ArrowLeft, Check, Close } from '@element-plus/icons-vue'
import { useOutfitsStore } from '@/stores/outfits'
import { useWardrobeStore } from '@/stores/wardrobe'
import type { Clothing } from '@/api/client'

const router = useRouter()
const outfitsStore = useOutfitsStore()
const wardrobeStore = useWardrobeStore()

const saveFormRef = ref<FormInstance>()
const activeCategory = ref('')
const selectedItemIds = ref<string[]>([])
const saveDialogVisible = ref(false)
const saving = ref(false)

const saveForm = reactive({
  name: '',
  style: '',
  occasion: '',
  season: ''
})

const saveRules: FormRules = {
  name: [{ required: true, message: '请输入搭配名称', trigger: 'blur' }]
}

const filteredClothes = computed(() => {
  if (!activeCategory.value) {
    return wardrobeStore.items
  }
  return wardrobeStore.items.filter(item => item.category === activeCategory.value)
})

const selectedItems = computed(() => {
  return wardrobeStore.items.filter(item => selectedItemIds.value.includes(item.id))
})

onMounted(async () => {
  await wardrobeStore.fetchItems()
})

function handleCategoryChange() {
  // Category change handled by computed
}

function isSelected(id: string) {
  return selectedItemIds.value.includes(id)
}

function toggleItem(item: Clothing) {
  const index = selectedItemIds.value.indexOf(item.id)
  if (index > -1) {
    selectedItemIds.value.splice(index, 1)
  } else {
    selectedItemIds.value.push(item.id)
  }
}

function removeItem(id: string) {
  const index = selectedItemIds.value.indexOf(id)
  if (index > -1) {
    selectedItemIds.value.splice(index, 1)
  }
}

function handleClear() {
  selectedItemIds.value = []
}

function showSaveDialog() {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请至少选择一件衣物')
    return
  }

  // Auto-generate name
  const categories = selectedItems.value.map(item => item.category)
  const uniqueCategories = [...new Set(categories)]
  saveForm.name = uniqueCategories.join('+') + '搭配'

  saveDialogVisible.value = true
}

async function handleSave() {
  if (!saveFormRef.value) return

  await saveFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        const result = await outfitsStore.createOutfit({
          name: saveForm.name,
          style: saveForm.style,
          occasion: saveForm.occasion || undefined,
          season: saveForm.season || undefined,
          itemIds: selectedItemIds.value
        })

        if (result.success) {
          ElMessage.success('保存成功')
          saveDialogVisible.value = false
          goBack()
        } else {
          ElMessage.error(result.error || '保存失败')
        }
      } finally {
        saving.value = false
      }
    }
  })
}

function goBack() {
  router.push('/dashboard/outfits')
}
</script>

<style scoped>
.diy-outfit-container {
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

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
  align-items: start;
}

@media (max-width: 1024px) {
  .content {
    grid-template-columns: 1fr;
  }
}

.clothes-section,
.preview-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.clothes-section h2,
.preview-section h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.empty-clothes,
.empty-selection {
  padding: 40px 20px;
  text-align: center;
}

.hint {
  font-size: 13px;
  color: #999;
  margin: 8px 0 0 0;
}

.clothes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.clothing-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.clothing-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.clothing-item.selected {
  border-color: #667eea;
}

.clothing-item img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.item-checkbox {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  background: rgba(102, 126, 234, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.item-name {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 6px 8px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 11px;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.selected-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.selected-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.selected-item img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
}

.item-details {
  flex: 1;
}

.item-details .item-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0 0 2px 0;
}

.item-meta {
  font-size: 12px;
  color: #999;
  margin: 0;
}
</style>
