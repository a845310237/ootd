<template>
  <el-container class="dashboard-layout">
    <el-aside width="200px" class="sidebar">
      <div class="sidebar-header">
        <h2>穿搭AI</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        router
      >
        <el-menu-item index="/dashboard/wardrobe">
          <el-icon><ShoppingBag /></el-icon>
          <span>我的衣柜</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/outfits">
          <el-icon><MagicStick /></el-icon>
          <span>穿搭管理</span>
        </el-menu-item>
        <el-menu-item index="/dashboard/profile">
          <el-icon><User /></el-icon>
          <span>个人中心</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="dashboard-header">
        <div class="header-left">
          <h2>{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              <el-avatar :size="32" :src="authStore.user?.avatar">
                {{ authStore.user?.name?.[0] || authStore.user?.email[0] }}
              </el-avatar>
              <span class="username">{{ authStore.user?.name || authStore.user?.email }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="dashboard-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ShoppingBag, MagicStick, User } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/dashboard/wardrobe': '我的衣柜',
    '/dashboard/wardrobe/add': '添加衣物',
    '/dashboard/outfits': '穿搭管理',
    '/dashboard/outfits/generate': 'AI 生成穿搭',
    '/dashboard/outfits/create': '创建穿搭',
    '/dashboard/profile': '个人中心'
  }
  return titles[route.path] || '穿搭AI'
})

function handleCommand(command: string) {
  if (command === 'profile') {
    router.push('/dashboard/profile')
  } else if (command === 'logout') {
    authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.dashboard-layout {
  height: 100vh;
}

.sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
}

.sidebar-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #e4e7ed;
}

.sidebar-header h2 {
  margin: 0;
  color: #409eff;
}

.sidebar-menu {
  border-right: none;
}

.dashboard-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
}

.header-left h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #606266;
}

.dashboard-main {
  background: #f5f7fa;
  padding: 24px;
}
</style>
