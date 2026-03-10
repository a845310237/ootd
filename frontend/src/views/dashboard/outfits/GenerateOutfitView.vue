<template>
  <div class="generate-outfit-container">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="goBack">返回</el-button>
        <h1>AI生成搭配</h1>
      </div>
    </div>

    <!-- Check if user has clothes -->
    <div v-if="hasNoClothes" class="empty-state">
      <el-empty description="您还没有添加衣物">
        <p>请先添加衣物到衣柜，AI才能为您生成搭配</p>
        <el-button type="primary" @click="goToWardrobe">
          添加衣物
        </el-button>
      </el-empty>
    </div>

    <div v-else class="content">
      <!-- Generation Form -->
      <div class="form-section">
        <h2>穿搭需求</h2>
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="100px"
          size="large"
        >
          <el-form-item label="风格" prop="style">
            <el-select v-model="form.style" placeholder="选择风格" style="width: 100%">
              <el-option label="休闲" value="休闲" />
              <el-option label="运动" value="运动" />
              <el-option label="正式" value="正式" />
              <el-option label="商务" value="商务" />
              <el-option label="复古" value="复古" />
              <el-option label="简约" value="简约" />
              <el-option label="时尚" value="时尚" />
              <el-option label="街头" value="街头" />
            </el-select>
          </el-form-item>

          <el-form-item label="场合" prop="occasion">
            <el-select v-model="form.occasion" placeholder="选择场合" style="width: 100%">
              <el-option label="日常" value="日常" />
              <el-option label="工作" value="工作" />
              <el-option label="约会" value="约会" />
              <el-option label="运动" value="运动" />
              <el-option label="聚会" value="聚会" />
              <el-option label="旅行" value="旅行" />
              <el-option label="正式场合" value="正式场合" />
            </el-select>
          </el-form-item>

          <el-form-item label="季节" prop="season">
            <el-select v-model="form.season" placeholder="选择季节" style="width: 100%">
              <el-option label="春" value="春" />
              <el-option label="夏" value="夏" />
              <el-option label="秋" value="秋" />
              <el-option label="冬" value="冬" />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="generating"
              :icon="MagicStick"
              @click="handleGenerate"
            >
              {{ generating ? '生成中...' : '生成搭配' }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- Generated Result -->
      <div v-if="generatedOutfit" class="result-section">
        <div class="result-header">
          <h2>生成结果</h2>
          <div class="result-actions">
            <el-button @click="handleRegenerate">
              <el-icon><Refresh /></el-icon>
              重新生成
            </el-button>
            <el-button type="primary" @click="showSaveDialog">
              保存搭配
            </el-button>
          </div>
        </div>

        <!-- Selected Items -->
        <div class="selected-items">
          <h3>推荐单品</h3>
          <div class="items-grid">
            <div
              v-for="item in generatedOutfit.selected_items"
              :key="item.id"
              class="item-card"
            >
              <img :src="item.imageUrl" :alt="item.name" />
              <div class="item-info">
                <p class="item-name">{{ item.name }}</p>
                <p class="item-category">{{ item.category }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Reasoning -->
        <div v-if="generatedOutfit.reasoning" class="reasoning">
          <h3>搭配理由</h3>
          <p>{{ generatedOutfit.reasoning }}</p>
        </div>

        <!-- Tips -->
        <div v-if="generatedOutfit.tips?.length" class="tips">
          <h3>穿搭小贴士</h3>
          <ul>
            <li v-for="(tip, index) in generatedOutfit.tips" :key="index">
              {{ tip }}
            </li>
          </ul>
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
import { ArrowLeft, MagicStick, Refresh } from '@element-plus/icons-vue'
import { useOutfitsStore } from '@/stores/outfits'
import { useWardrobeStore } from '@/stores/wardrobe'

const router = useRouter()
const outfitsStore = useOutfitsStore()
const wardrobeStore = useWardrobeStore()

const formRef = ref<FormInstance>()
const saveFormRef = ref<FormInstance>()
const generating = ref(false)
const saving = ref(false)
const saveDialogVisible = ref(false)

const form = reactive({
  style: '休闲',
  occasion: '日常',
  season: '春'
})

const saveForm = reactive({
  name: ''
})

const rules: FormRules = {
  style: [{ required: true, message: '请选择风格', trigger: 'change' }],
  occasion: [{ required: true, message: '请选择场合', trigger: 'change' }],
  season: [{ required: true, message: '请选择季节', trigger: 'change' }]
}

const saveRules: FormRules = {
  name: [{ required: true, message: '请输入搭配名称', trigger: 'blur' }]
}

const hasNoClothes = computed(() => wardrobeStore.items.length === 0)
const generatedOutfit = computed(() => outfitsStore.generatedOutfit)

onMounted(async () => {
  await wardrobeStore.fetchItems()
})

async function handleGenerate() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      generating.value = true
      try {
        const result = await outfitsStore.generateOutfit({
          style: form.style,
          occasion: form.occasion,
          season: form.season
        })

        if (result.success) {
          ElMessage.success('搭配生成成功')
          // Auto-generate a name
          saveForm.name = `${form.style}风${form.season}季${form.occasion}搭配`
        } else {
          ElMessage.error(result.error || '生成失败')
        }
      } finally {
        generating.value = false
      }
    }
  })
}

function handleRegenerate() {
  handleGenerate()
}

function showSaveDialog() {
  saveDialogVisible.value = true
}

async function handleSave() {
  if (!saveFormRef.value || !generatedOutfit.value) return

  await saveFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        const result = await outfitsStore.saveGeneratedOutfit({
          name: saveForm.name,
          style: generatedOutfit.value.requirements.style,
          occasion: generatedOutfit.value.requirements.occasion,
          season: generatedOutfit.value.requirements.season,
          itemIds: generatedOutfit.value.selected_items.map(item => item.id),
          reasoning: generatedOutfit.value.reasoning,
          tips: generatedOutfit.value.tips
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

function goToWardrobe() {
  router.push('/dashboard/wardrobe')
}
</script>

<style scoped>
.generate-outfit-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.content {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 32px;
  align-items: start;
}

@media (max-width: 1024px) {
  .content {
    grid-template-columns: 1fr;
  }
}

.form-section,
.result-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.form-section h2,
.result-section h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 20px 0;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.result-actions {
  display: flex;
  gap: 8px;
}

.selected-items {
  margin-bottom: 24px;
}

.selected-items h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 12px 0;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
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
  padding: 8px;
}

.item-name {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin: 0 0 2px 0;
}

.item-category {
  font-size: 11px;
  color: #999;
  margin: 0;
}

.reasoning,
.tips {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 16px;
}

.reasoning h3,
.tips h3 {
  font-size: 14px;
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
  margin: 0;
}

.tips li {
  margin-bottom: 4px;
}
</style>
